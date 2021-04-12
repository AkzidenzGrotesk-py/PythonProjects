import ConsoleEngine, json
from ConsoleEngine import FORMAT, PIXEL_TYPE, DEBUG, UI

editor = ConsoleEngine.ConsoleGame()
MAX_WIDTH = 150
MAX_HEIGHT = 113

def clamp(value: int, min: int, max: int) -> int:
    if value < min: return min
    if value > max: return max
    return value

def generate_brushes(self):
    self.BRUSH_CYCLE = [
        PIXEL_TYPE.PIXEL_SOLID,
        PIXEL_TYPE.PIXEL_THREEQUARTERS,
        PIXEL_TYPE.PIXEL_HALF,
        PIXEL_TYPE.PIXEL_QUARTER,
        self.custom_char
    ]
    self.COLOR_CYCLE = [
        "",
        FORMAT.FG_BLACK,
        FORMAT.FG_DARK_BLUE,
        FORMAT.FG_DARK_GREEN,
        FORMAT.FG_DARK_CYAN,
        FORMAT.FG_DARK_RED,
        FORMAT.FG_DARK_MAGENTA,
        FORMAT.FG_DARK_YELLOW,
        FORMAT.FG_BBLACK,
        FORMAT.FG_BLUE,
        FORMAT.FG_GREEN,
        FORMAT.FG_CYAN,
        FORMAT.FG_RED,
        FORMAT.FG_MAGENTA,
        FORMAT.FG_YELLOW,
        FORMAT.FG_WHITE,
        FORMAT.BG_BLACK,
        FORMAT.BG_DARK_BLUE,
        FORMAT.BG_DARK_GREEN,
        FORMAT.BG_DARK_CYAN,
        FORMAT.BG_DARK_RED,
        FORMAT.BG_DARK_MAGENTA,
        FORMAT.BG_DARK_YELLOW,
        FORMAT.BG_BBLACK,
        FORMAT.BG_BLUE,
        FORMAT.BG_GREEN,
        FORMAT.BG_CYAN,
        FORMAT.BG_RED,
        FORMAT.BG_MAGENTA,
        FORMAT.BG_YELLOW,
        FORMAT.BG_WHITE,
        FORMAT.FG_RGB(*self.custom_fg),
        FORMAT.BG_RGB(*self.custom_bg)
    ]
    self.brushcolors = [
        [
            "X",
            f"{FORMAT.FG_BLACK}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_DARK_BLUE}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_DARK_GREEN}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_DARK_CYAN}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_DARK_RED}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_DARK_MAGENTA}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_DARK_YELLOW}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_BBLACK}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_BLUE}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_GREEN}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_CYAN}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_RED}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_MAGENTA}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_YELLOW}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.FG_WHITE}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}",
            f"{FORMAT.BG_BLACK}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_DARK_BLUE}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_DARK_GREEN}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_DARK_CYAN}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_DARK_RED}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_DARK_MAGENTA}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_DARK_YELLOW}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_BBLACK}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_BLUE}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_GREEN}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_CYAN}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_RED}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_MAGENTA}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_YELLOW}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{FORMAT.BG_WHITE}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}",
            f"{self.COLOR_CYCLE[-2]}C{FORMAT.RESET}",
            f"{self.COLOR_CYCLE[-1]}C{FORMAT.RESET}"
        ]
    ]

def reset(self):
    self.cursor_pos = [0, 0]
    self.brush = PIXEL_TYPE.PIXEL_SOLID
    self.brushcolor = 0
    self.brushtype = 0

def save_sprite(self):
    self.DrawSprite((2, 2), self.StringToSprite(f"Saving as {self.spritefile}... ", FORMAT.FG_CYAN))
    with open(self.spritefile, "w") as sprite_file:
        json.dump(self.sprite, sprite_file)

def resize_sprite(self, newsize):
    try:
        for i, s in enumerate(newsize): newsize[i] = int(s)
        self.spritesize = (clamp(newsize[0], 1, MAX_WIDTH), clamp(newsize[1], 1, MAX_HEIGHT))
        newsprite = [["" for i in range(self.spritesize[0])] for y in range(self.spritesize[1])]

        for y, l in enumerate(newsprite):
            for x, c in enumerate(l):
                try: newsprite[y][x] = self.sprite["sprite"][y][x]
                except IndexError:
                    continue

        self.sprite["sprite"] = newsprite
    except: pass

def load_sprite(self, sprname):
    try:
        self.sprite = self.LoadSprite(sprname)
        self.spritefile = sprname + ".spr"
        self.spritesize = (len(self.sprite["sprite"][0]), len(self.sprite["sprite"]))
    except: pass

def generate_sprite(self, size, filename):
    self.spritesize = (clamp(size[0], 1, MAX_WIDTH), clamp(size[1], 1, MAX_HEIGHT))
    self.spritefile = filename
    self.sprite = {
        "sprite" : [["" for i in range(self.spritesize[0])] for y in range(self.spritesize[1])]
    }

def new_sprite(self, newname, newsize):
    try:
        for i, s in enumerate(newsize): newsize[i] = int(s)
    except: pass
    else:
        if len(newsize) == 2 and newname != "":
            generate_sprite(self, newsize, newname)

def painting_actions(self):
    sprint = 1
    if self.Keyboard("ctrl"): sprint = 2
    if self.Keyboard("down") and self.cursor_pos[1] < self.spritesize[1] - 1:
        self.cursor_pos[1] += 8 * sprint * self.fElapsedTime
    if self.Keyboard("up") and self.cursor_pos[1] > 1:
        self.cursor_pos[1] -= 8 * sprint * self.fElapsedTime
    if self.Keyboard("right") and self.cursor_pos[0] < self.spritesize[0] - 1:
        self.cursor_pos[0] += 8 * sprint * self.fElapsedTime
    if self.Keyboard("left") and self.cursor_pos[0] > 1:
        self.cursor_pos[0] -= 8 * sprint * self.fElapsedTime

    if self.Keyboard("z"):
        self.sprite["sprite"][int(self.cursor_pos[1])][int(self.cursor_pos[0])] = self.brush
    if self.Keyboard("x"):
        self.sprite["sprite"][int(self.cursor_pos[1])][int(self.cursor_pos[0])] = ""

    if self.Keyboard("a"):
        self.brushcolor -= 10 * self.fElapsedTime
        if self.brushcolor < 0:
            self.brushcolor = len(self.COLOR_CYCLE) - 1
    if self.Keyboard("d"):
        self.brushcolor += 10 * self.fElapsedTime
        if self.brushcolor >= len(self.COLOR_CYCLE):
            self.brushcolor = 0

    if self.Keyboard("w"):
        self.brushtype -= 10 * self.fElapsedTime
        if self.brushtype < 0:
            self.brushtype = len(self.BRUSH_CYCLE) - 1
    if self.Keyboard("s"):
        self.brushtype += 10 * self.fElapsedTime
        if self.brushtype >= len(self.BRUSH_CYCLE):
            self.brushtype = 0

    if self.Keyboard("c"):
        newcustom = UI.Input((2, 2), FORMAT.FG_CYAN + "CUSTOM FOREGROUND (r g b): " + FORMAT.RESET).split()
        try:
            for i, s in enumerate(newcustom): newcustom[i] = int(s)
        except: pass
        else:
            if len(newcustom) == 3: self.custom_fg = newcustom
    if self.Keyboard("v"):
        newcustom = UI.Input((2,2), FORMAT.FG_CYAN + "CUSTOM BACKGROUND (r g b): " + FORMAT.RESET).split(' ')
        try:
            for i, s in enumerate(newcustom): newcustom[i] = int(s)
        except: pass
        else:
            if len(newcustom) == 3: self.custom_bg = newcustom
    if self.Keyboard("b"):
        newcustom = UI.Input((2,2), FORMAT.FG_CYAN + "CUSTOM BRUSH SHAPE: " + FORMAT.RESET)
        self.custom_char = newcustom

    if self.brushcolor > 0:
        self.brush = self.COLOR_CYCLE[int(self.brushcolor)] + self.BRUSH_CYCLE[int(self.brushtype)] + FORMAT.RESET
    else:
        self.brush = self.BRUSH_CYCLE[int(self.brushtype)]

    DEBUG.HideCursor()

def file_actions(self):
    if self.Keyboard("n"):
        newname = UI.Input((2,2), FORMAT.FG_CYAN + "NAME (string): " + FORMAT.RESET) + ".spr"
        DEBUG.ClearThisLine()
        newsize = UI.Input((2,2), FORMAT.FG_CYAN + "NEW SIZE (width height): " + FORMAT.RESET).split(' ')

        new_sprite(self, newname, newsize)

        reset(self)

    if self.Keyboard("m"):
        sprname = UI.Input((2,2), FORMAT.FG_CYAN + "NAME (string): " + FORMAT.RESET)
        load_sprite(self, sprname)
        reset(self)

    if self.Keyboard("k"):
        newsize = UI.Input((2,2), FORMAT.FG_CYAN + "NEW SIZE (width height): " + FORMAT.RESET).split(" ")
        resize_sprite(self, newsize)
        reset(self)

    if self.Keyboard("j"):
        newname = UI.Input((2,2), FORMAT.FG_CYAN + "NEW NAME (string): " + FORMAT.RESET) + ".spr"
        if newname != "": self.spritefile = newname

    if self.Keyboard("l"):
        save_sprite(self)

    DEBUG.HideCursor()

def handle_console(self):
    if self.Keyboard("p"):
        self.consoleInput.isFocused = True

    self.consoleInput.Handle(inputtext = "> ")

    if self.consoleInput.GetText() != "":
        txt = self.consoleInput.GetText().split(" ")
        if txt[0] == "exit": self.active = False
        elif txt[0] == "save": save_sprite(self)
        elif txt[0] == "resize" and len(txt) >= 3:
            resize_sprite(self, [txt[1], txt[2]])
        elif txt[0] == "rename" and len(txt) >= 2:
            if txt[1] != "": self.spritefile = txt[1] + ".spr"
        elif txt[0] == "open" and len(txt) >= 2:
            if txt[1] != "": load_sprite(self, txt[1])
        elif txt[0] == "new" and len(txt) >= 4:
            new_sprite(self, txt[1], [txt[2], txt[3]])
        elif txt[0] == "fg" and len(txt) >= 4:
            self.custom_fg = (int(txt[1]), int(txt[2]), int(txt[3]))
        elif txt[0] == "bg" and len(txt) >= 4:
            self.custom_bg = (int(txt[1]), int(txt[2]), int(txt[3]))
        elif txt[0] == "brush" and len(txt) >= 2:
            self.custom_char = txt[1]

        self.consoleInput.text = ""

@editor.OnUserCreate
def setup(self):
    self.title = "Sprite Editor"
    self.geometry = (200, 120)
    self.cursor_pos = [0, 0]
    self.consoleInput = UI.xInput(self, (2, 47))
    self.draw_position = ((self.geometry[0] - 1) - MAX_WIDTH - 2, (self.geometry[1] - 1) - MAX_HEIGHT - 2)
    self.brush = PIXEL_TYPE.PIXEL_SOLID
    self.brushcolor = 0
    self.brushtype = 0
    self.custom_fg = (255, 255, 255)
    self.custom_bg = (255, 255, 255)
    self.custom_char = "c"
    generate_brushes(self)

    generate_sprite(self, (16, 16), "MySprite.spr")

@editor.OnUserUpdate
def loop(self):
    generate_brushes(self)
    painting_actions(self)
    file_actions(self)
    handle_console(self)

    # File
    self.DrawText((2,5),["CURRENTLY EDITING: ", self.spritefile],[FORMAT.FG_RED, ""])
    self.DrawText((2,6),["SIZE: ", f"{self.spritesize[0]}x{self.spritesize[1]}"],[FORMAT.FG_RED, ""])

    # Help Bar
    bn = 8
    self.DrawText((2, bn+1),["move cursor: ", "←↑→↓"],[FORMAT.FG_YELLOW, ""])
    self.DrawText((2, bn+2),["sprint: ", "CTRL"],[FORMAT.FG_YELLOW, ""])
    self.DrawText((2, bn+4),["change brush: ", "WASD"],[FORMAT.FG_YELLOW, ""])
    self.DrawText((2, bn+5),["set custom foreground: ", "C"],[FORMAT.FG_YELLOW, ""])
    self.DrawText((2, bn+6),["set custom background: ", "V"],[FORMAT.FG_YELLOW, ""])
    self.DrawText((2, bn+7),["set custom brush: ", "B"],[FORMAT.FG_YELLOW, ""])

    self.DrawText((2, bn+9),["draw: ", "Z"],[FORMAT.FG_YELLOW, ""])
    self.DrawText((2, bn+10),["erase: ", "X"],[FORMAT.FG_YELLOW, ""])

    self.DrawText((2, bn+12),["open console: ", "P"],[FORMAT.FG_YELLOW, ""])

    bn2 = 25
    self.DrawText((2, bn2+1),["new file: ", "N"],[FORMAT.FG_YELLOW, ""])
    self.DrawText((2, bn2+2),["open file: ", "M"],[FORMAT.FG_YELLOW, ""])
    self.DrawText((2, bn2+3),["resize canvas: ", "K"],[FORMAT.FG_YELLOW, ""])
    self.DrawText((2, bn2+4),["rename file: ", "J"],[FORMAT.FG_YELLOW, ""])
    self.DrawText((2, bn2+5),["save file: ", "L"],[FORMAT.FG_YELLOW, ""])
    # Brush Settings
    bn3 = 38
    self.Draw((2, bn3+2), PIXEL_TYPE.PIXEL_SOLID)
    self.Draw((2, bn3+3), PIXEL_TYPE.PIXEL_THREEQUARTERS)
    self.Draw((2, bn3+4), PIXEL_TYPE.PIXEL_HALF)
    self.Draw((2, bn3+5), PIXEL_TYPE.PIXEL_QUARTER)
    self.Draw((2, bn3+6), self.custom_char)
    self.DrawSprite((3, bn3+1), self.brushcolors)

    self.Draw((int(self.brushcolor) + 3, int(self.brushtype) + bn3+2), "┼")

    self.DrawEdgeBox((1,4), (45, 3))
    self.DrawEdgeBox((1,bn), (45, 16))
    self.DrawEdgeBox((1,bn2), (45, 12))
    self.DrawEdgeBox((1,bn3), (45, 7))
    self.DrawEdgeBox((1,bn3+8), (45, 2))
    self.DrawEdgeBox((1,1), (self.geometry[0] - 3, 2))
    self.DrawEdgeBox(self.draw_position, (self.spritesize[0] + 1, self.spritesize[1] + 1))

    self.DrawSprite((self.draw_position[0]+1, self.draw_position[1]+1), self.sprite)
    self.Draw((self.draw_position[0]+1 + self.cursor_pos[0], self.draw_position[1]+1 + self.cursor_pos[1]), "┼")
