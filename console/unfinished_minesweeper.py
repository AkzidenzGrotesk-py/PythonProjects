import random, os, copy, keyboard, sys
from dataclasses import dataclass

@dataclass
class v2:
    x: float = 0.0
    y: float = 0.0

    def t(self) -> (float, float):
        return (self.x, self.y)

class Renderer:
    def __init__(self, renderx: int, rendery: int, shiftx: int = 0, shifty: int = 0, empty: str = ' '):
        self.cells = [
            [empty for x in range(renderx)] for y in range(rendery)
        ]
        self.cellcolours = [
            ["\033[0m" for x in range(renderx)] for y in range(rendery)
        ]
        self.shift = (shiftx, shifty)

    def start(self):
        os.system("cls")
        self.reset_cursor()

    def reset_cursor(self):
        print("\033[0;0H\033[?25l", end = '')

    def render(self, space_cells = False):
        final = "\n" * self.shift[1]
        for i, y in enumerate(self.cells):
            final += " " * self.shift[0]
            for j, x in enumerate(y):
                final += self.cellcolours[i][j] + x + "\033[0m" + (" " if space_cells else '')
            final += "\n"
        print(final, end = '')

    def set_cell(self, cellx, celly, char: str = ' ', col: str = '\033[0m'):
        if char != "__":
            self.cells[int(celly)][int(cellx)] = char
        if col != "__":
            self.cellcolours[int(celly)][int(cellx)] = col

    def get_cell(self, cellx, celly):
        return (self.cells[int(cellx)][int(celly)], self.cellcolours[int(celly)][int(cellx)])

class Cursor:
    def __init__(self, edges: v2):
        self.lpos = v2()
        self.pos = v2()
        self.edge = edges

    def mov_up(self):
        self.lpos = v2(self.pos.x, self.pos.y)
        if self.pos.y > 0: self.pos.y -= 1

    def mov_down(self):
        self.lpos = v2(self.pos.x, self.pos.y)
        if self.pos.y < self.edge.y - 1: self.pos.y += 1

    def mov_left(self):
        self.lpos = v2(self.pos.x, self.pos.y)
        if self.pos.x > 0: self.pos.x -= 1

    def mov_right(self):
        self.lpos = v2(self.pos.x, self.pos.y)
        if self.pos.x < self.edge.x - 1: self.pos.x += 1

class Minesweeper:
    def __init__(self, sizex: int, sizey: int, nmines: int):
        self.size = v2(sizex, sizey)
        self.cursor = Cursor(self.size)
        self.renderer = Renderer(*self.size.t(), 4, 2, '.')
        self.values = [
            [0 for x in range(self.size.x)] for y in range(self.size.y)
        ]
        self.active = True
        self.nmines = nmines



    def start(self):
        self.pos = []
        self.flags = []

        for m in range(self.nmines):
            success = False
            while not success:
                p = v2(random.randrange(0, self.size.x), random.randrange(0, self.size.y))
                if p in self.pos: continue
                else:
                    success = True
                    self.pos.append(p)

        for y in range(self.size.y):
            for x in range(self.size.x):
                accum = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if v2(x + i, y + j) in self.pos: accum += 1

                self.values[y][x] = accum

        keyboard.on_press_key("up", lambda e: self.cursor.mov_up())
        keyboard.on_press_key("down", lambda e: self.cursor.mov_down())
        keyboard.on_press_key("left", lambda e: self.cursor.mov_left())
        keyboard.on_press_key("right", lambda e: self.cursor.mov_right())
        keyboard.on_press_key("f", lambda e: self.place_flag())
        keyboard.on_press_key("q", lambda e: sys.exit())

        self.main()

    def place_flag(self):
        cv = self.renderer.get_cell(*self.cursor.pos.t())
        if cv[0] == ".":
            self.renderer.set_cell(*self.cursor.pos.t(), "!", "\033[36m")
            self.flags.append(self.cursor.pos)
        else:
            self.renderer.set_cell(*self.cursor.pos.t(), ".", "\033[0m")
            try: self.flags.remove(self.cursor.pos)
            except ValueError: pass

    def main(self):
        self.renderer.start()
        while self.active:
            self.renderer.reset_cursor()

            self.renderer.set_cell(*self.cursor.lpos.t(), "__", self.renderer.get_cell(*self.cursor.lpos.t())[1] + "\033[40m")
            self.renderer.set_cell(*self.cursor.pos.t(), "__", self.renderer.get_cell(*self.cursor.pos.t())[1] + "\033[43m")

            if keyboard.is_pressed("space"):
                if self.cursor.pos in self.pos:
                    self.active = False
                    for p in self.pos:
                        self.renderer.set_cell(*p.t(), "@", "\033[31m")
                else:
                    self.renderer.set_cell(*self.cursor.pos.t(), str(self.values[int(self.cursor.pos.y)][int(self.cursor.pos.x)]), "__")

            self.renderer.render(True)

            if not self.active: print("\n\033[31mYOU LOSE!\033[0m\n")

            if self.flags == self.pos:
                print("\n\033[36mYOU WIN!\033[0m\n")
                self.active = False

def main():
    d = input("difficulty (beginner, intermediate, expert) > ")
    if int(d) == 1:
        s = int(input("size (8x8, 9x9, 10x10) > "))
        if s == 1: size = v2(8, 8)
        elif s == 2: size = v2(9, 9)
        elif s == 3: size = v2(10, 10)
        else: return
        m = Minesweeper(*size.t(), 10)
    elif int(d) == 2:
        s = int(input("size (13x15, 16x16) > "))
        if s == 1: size = v2(13, 15)
        elif s == 2: size = v2(16, 16)
        else: return
        m = Minesweeper(*size.t(), 40)
    elif int(d) == 3:
        m = Minesweeper(30, 16, 99)
    else: return

    m.start()

if __name__ == "__main__":
    main()
