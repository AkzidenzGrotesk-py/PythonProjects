from ConsoleEngine import *
import random, time

global ENABLE_WRAPAROUND, RAVE, BRICK_MODE, SNAKE_SPEED, SNAKE_COLOR

speed_settings = {
    0.25 : "Impossible",
    0.5 : "Expert+",
    1 : "Expert",
    2 : "Hard",
    4 : "Normal",
    8 : "Easy",
}
color_settings = {
    1: "Blue",
    2: "Green",
    3: "Cyan",
    4: "Yellow",
    5: "Magenta",
    6: "Mono",
    7: "Red"
}

ENABLE_WRAPAROUND   = False
RAVE                = False
BRICK_MODE          = False
SNAKE_SPEED         = 4
PLAY_AREA           = (24, 24)
SNAKE_COLOR         = 1
master = ConsoleGame()

def newapple(self):
    newapple_ = (random.randrange(1, PLAY_AREA[0] - 2), random.randrange(1, PLAY_AREA[1] - 2))
    c = True
    if BRICK_MODE:
        for b in self.bricks:
            if newapple_ == b: c = False
    if c: self.apple = newapple_
    else: newapple(self)

def newbrick(self):
    newbrick = (random.randrange(1, PLAY_AREA[0] - 2), random.randrange(1, PLAY_AREA[1] - 2))
    c = True
    if BRICK_MODE:
        for b in self.bricks:
            if newbrick == b: c = False
    if c: self.bricks.append(newbrick)
    else: newbrick(self)

def generate_snake_sprite(self):
    if self.snake_color == 1:
        s = f"{FORMAT.FG_BLUE}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
        sd = f"{FORMAT.FG_DARK_BLUE}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
    elif self.snake_color == 2:
        s = f"{FORMAT.FG_GREEN}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
        sd = f"{FORMAT.FG_DARK_GREEN}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
    elif self.snake_color == 3:
        s = f"{FORMAT.FG_CYAN}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
        sd = f"{FORMAT.FG_DARK_CYAN}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
    elif self.snake_color == 4:
        s = f"{FORMAT.FG_YELLOW}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
        sd = f"{FORMAT.FG_DARK_YELLOW}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
    elif self.snake_color == 5:
        s = f"{FORMAT.FG_MAGENTA}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
        sd = f"{FORMAT.FG_DARK_MAGENTA}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
    elif self.snake_color == 6:
        s = f"{FORMAT.FG_WHITE}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
        sd = f"{FORMAT.FG_BLACK}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
    else:
        s = f"{FORMAT.FG_RED}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
        sd = f"{FORMAT.FG_DARK_RED}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"

    self.snakesprite = [[s for i in range(4)] for j in range(4)]
    self.snakesprite2 = [[sd for i in range(4)] for j in range(4)]

def handle_controls(self):
    global ENABLE_WRAPAROUND, RAVE, BRICK_MODE, SNAKE_SPEED, SNAKE_COLOR
    if self.gamestate == 0:
        if self.Keyboard('up') or self.Keyboard('w'):
            if self.mdir != 3: self.mdir = 1
        if self.Keyboard('right') or self.Keyboard('a'):
            if self.mdir != 4: self.mdir = 2
        if self.Keyboard('down') or self.Keyboard('s'):
            if self.mdir != 1: self.mdir = 3
        if self.Keyboard('left') or self.Keyboard('d'):
            if self.mdir != 2: self.mdir = 4
        if self.Keyboard('x'): self.gamestate = 1
    if self.gamestate == 1:
        if self.Keyboard('space'):
            self.snake = [(PLAY_AREA[0] / 2, PLAY_AREA[1] / 2)]
            self.length = 2
            self.mdir = 0
            self.gamestate = 0
            self.bricks = []
        if self.Keyboard('x'): self.active = False
        if self.Keyboard('q'): self.gamestate = 2
    if self.gamestate == 2:
        if self.Keyboard('space'):
            self.snake = [(PLAY_AREA[0] / 2, PLAY_AREA[1] / 2)]
            self.length = 2
            self.mdir = 0
            self.gamestate = 0
            self.bricks = []
        if self.Keyboard('x'): self.active = False
        if self.Keyboard('t'):
            ENABLE_WRAPAROUND = not ENABLE_WRAPAROUND
            time.sleep(0.125)
        if self.Keyboard('y'):
            RAVE = not RAVE
            time.sleep(0.125)
        if self.Keyboard('u'):
            BRICK_MODE = not BRICK_MODE
            time.sleep(0.125)
        if self.Keyboard('i'):
            SNAKE_SPEED /= 2
            if SNAKE_SPEED < 0.25: SNAKE_SPEED = 8
            time.sleep(0.125)
        if self.Keyboard('o'):
            SNAKE_COLOR += 1
            if SNAKE_COLOR > 7: SNAKE_COLOR = 1
            self.snake_color = SNAKE_COLOR
            generate_snake_sprite(self)
            time.sleep(0.125)



def handle_movement(self):
    if self.gamestate == 0:
        self.speed += 55 * self.fElapsedTime
        if self.speed >= SNAKE_SPEED:
            if self.mdir == 1:
                self.snake.append((self.snake[-1][0], self.snake[-1][1] - 1))
            elif self.mdir == 2:
                self.snake.append((self.snake[-1][0] + 1, self.snake[-1][1]))
            elif self.mdir == 3:
                self.snake.append((self.snake[-1][0], self.snake[-1][1] + 1))
            elif self.mdir == 4:
                self.snake.append((self.snake[-1][0] - 1, self.snake[-1][1]))

            self.speed = 0

def update_snake(self):
    if self.gamestate == 0:
        # CHECK OOB
        if self.snake[-1][0] > (PLAY_AREA[0] - 1) and self.mdir == 2 or self.snake[-1][0] >= PLAY_AREA[0]:
            if ENABLE_WRAPAROUND:
                del self.snake[-1]
                self.snake.append((0, self.snake[-1][1]))
            else:
                self.gamestate = 1
        if self.snake[-1][0] < 0 and self.mdir == 4 or self.snake[-1][0] <= -1:
            if ENABLE_WRAPAROUND:
                del self.snake[-1]
                self.snake.append((PLAY_AREA[0] - 1, self.snake[-1][1]))
            else:
                self.gamestate = 1
        if self.snake[-1][1] > (PLAY_AREA[1] - 1) and self.mdir == 3 or self.snake[-1][1] >= PLAY_AREA[1]:
            if ENABLE_WRAPAROUND:
                del self.snake[-1]
                self.snake.append((self.snake[-1][0], 0))
            else:
                self.gamestate = 1
        if self.snake[-1][1] < 0 and self.mdir == 1 or self.snake[-1][1] <= -1:
            if ENABLE_WRAPAROUND:
                del self.snake[-1]
                self.snake.append((self.snake[-1][0], PLAY_AREA[1] - 1))
            else:
                self.gamestate = 1

        # UPDATE SNAKE
        if len(self.snake) > self.length:
            del self.snake[0]

        # CHECK BRICKS
        if BRICK_MODE:
            for b in self.bricks:
                if (int(self.snake[-1][0]), int(self.snake[-1][1])) == b:
                    self.gamestate = 1

        # UPDATE/CHECK APPLE
        if (int(self.snake[-1][0]), int(self.snake[-1][1])) == self.apple:
            newapple(self)
            self.length += 1

            if RAVE:
                self.snake_color += 1
                if self.snake_color >= 8:
                    self.snake_color = 1
                generate_snake_sprite(self)

            if BRICK_MODE:
                newbrick(self)


def draw(self):
    # DRAW SNAKE & CHECK FOR HEAD COLLISION
    if self.gamestate == 0:
        for i, s in enumerate(self.snake):
            if self.snake[-1] == s and i != (len(self.snake) - 1):
                self.gamestate = 1
            if i % 2 == 1: self.DrawSprite((s[0] * 4 + 1, s[1] * 4 + 1), self.snakesprite)
            else: self.DrawSprite((s[0] * 4 + 1, s[1] * 4 + 1), self.snakesprite2)

        for b in self.bricks:
            self.DrawSprite((b[0] * 4 + 1, b[1] * 4 + 1), self.bricksprite)

        self.DrawSprite((self.apple[0] * 4 + 1, self.apple[1] * 4 - 1), self.applesprite)
        self.Draw((2, 2), str((self.length - 2) * 100))
        self.DrawBox((0, 0), (self.geometry[0] - 1, self.geometry[1] - 1), PIXEL_TYPE.PIXEL_QUARTER)

    if self.gamestate == 1:
        txt = f"GAME OVER - SCORE: {(self.length - 2) * 100} ({self.length})"
        self.Draw(((self.geometry[0] / 2) - (len(txt) / 2), self.geometry[1] / 2 + 7), txt)
        self.DrawBox((0, 0), (self.geometry[0] - 1, self.geometry[1] - 1), PIXEL_TYPE.PIXEL_SOLID)
        self.DrawSprite((self.geometry[0] / 2 - len(self.gameover[0]) / 2, self.geometry[1] / 2 - len(self.gameover) / 2), self.gameover)
        self.DrawSprite((self.geometry[0] / 2 - len(self.snakelogo[0]) / 2, 10), self.snakelogo)

        txt = f"PRESS [ SPACE ]"
        self.DrawSprite((self.geometry[0] / 2 - len(txt) / 2, self.geometry[1] - 11), self.StringToSprite(txt, FORMAT.FG_YELLOW))
        txt = "[ X ] TO QUIT"
        self.Draw((self.geometry[0] / 2 - len(txt) / 2, self.geometry[1] - 8), txt)
        txt = "[ Q ] TO RETURN TO MENU"
        self.Draw((self.geometry[0] / 2 - len(txt) / 2, self.geometry[1] - 6), txt)

    if self.gamestate == 2:
        self.DrawBox((0, 0), (self.geometry[0] - 1, self.geometry[1] - 1), PIXEL_TYPE.PIXEL_SOLID)
        self.DrawSprite((self.geometry[0] / 2 - len(self.snakelogo[0]) / 2, 10), self.snakelogo)

        txt = f"←↑→↓ OR WASD TO MOVE"
        self.DrawSprite((self.geometry[0] / 2 - len(txt) / 2, self.geometry[1] / 2 - 10), self.StringToSprite(txt, FORMAT.FG_YELLOW))
        txt = "[T] ENABLE_WRAPAROUND: " + str(ENABLE_WRAPAROUND)
        self.Draw((self.geometry[0] / 2 - len(txt) / 2, self.geometry[1] / 2 - 6), txt)
        txt = "[Y] RAVE: " + str(RAVE)
        self.Draw((self.geometry[0] / 2 - len(txt) / 2, self.geometry[1] / 2 - 4), txt)
        txt = "[U] BRICK_MODE: " + str(BRICK_MODE)
        self.Draw((self.geometry[0] / 2 - len(txt) / 2, self.geometry[1] / 2 - 2), txt)
        txt = "[I] SNAKE_SPEED: " + speed_settings[SNAKE_SPEED]
        self.Draw((self.geometry[0] / 2 - len(txt) / 2, self.geometry[1] / 2), txt)
        txt = "[O] SNAKE_COLOR: " + color_settings[SNAKE_COLOR]
        self.Draw((self.geometry[0] / 2 - len(txt) / 2, self.geometry[1] / 2 + 2), txt)

        txt = f"PRESS [ SPACE ]"
        self.DrawSprite((self.geometry[0] / 2 - len(txt) / 2, self.geometry[1] - 11), self.StringToSprite(txt, FORMAT.FG_YELLOW))
        txt = "[ X ] TO QUIT"
        self.Draw((self.geometry[0] / 2 - len(txt) / 2, self.geometry[1] - 8), txt)



@master.OnUserCreate
def setup(self):
    self.title = "Snake"
    self.geometry = (PLAY_AREA[0] * 4 + 2, PLAY_AREA[1] *  4 + 2)

    self.snake = [(PLAY_AREA[0] / 2, PLAY_AREA[1] / 2)]
    self.bricks = []
    self.length = 2
    self.mdir = 0
    self.speed = 0
    self.gamestate = 2

    self.snake_color = SNAKE_COLOR
    generate_snake_sprite(self)

    a2 = f"{FORMAT.FG_RED}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
    a = f"{FORMAT.FG_DARK_RED}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
    st = f"{FORMAT.FG_RGB(139,69,19)}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
    self.applesprite = [
        ["",st,"",""],
        ["","",st,""],
        ["",a,a,""],
        [a,a2,a2,a],
        [a,a2,a2,a],
        ["",a,a,""]
    ]

    b1 = f"{FORMAT.FG_WHITE}{PIXEL_TYPE.PIXEL_THREEQUARTERS}{FORMAT.RESET}"
    b2 = f"{FORMAT.FG_BBLACK}{PIXEL_TYPE.PIXEL_HALF}{FORMAT.RESET}"
    self.bricksprite = [
        [b2,b2,b2,b2],
        [b2,b1,b1,b2],
        [b2,b1,b1,b2],
        [b2,b2,b2,b2]
    ]

    e = ""
    y = f"{FORMAT.FG_RED}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
    p = f"{PIXEL_TYPE.PIXEL_SOLID}"
    self.gameover = [
        [y,y,y,y,e,y,y,y,y,e,y,e,y,y,e,y,y,y,y],
        [y,e,e,e,e,y,e,e,y,e,y,y,e,y,e,y,y,y,e],
        [y,e,e,y,e,y,y,y,y,e,y,e,e,y,e,y,e,e,e],
        [y,y,y,y,e,y,e,e,y,e,y,e,e,y,e,y,y,y,y],
        [e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e,e],
        [y,y,y,y,e,y,e,e,y,e,y,y,y,y,e,y,y,y,y],
        [y,e,e,y,e,y,e,e,y,e,y,y,y,e,e,y,y,y,y],
        [y,e,e,y,e,e,y,y,e,e,y,e,e,e,e,y,e,y,e],
        [y,y,y,y,e,e,y,y,e,e,y,y,y,y,e,y,e,e,y]
    ]

    r = f"{FORMAT.FG_GREEN}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"
    f = f"{FORMAT.FG_DARK_GREEN}{PIXEL_TYPE.PIXEL_SOLID}{FORMAT.RESET}"

    self.snakelogo = [
        [r,f,r,f,r,e,e,p,e,e,e,p,e,e,e,p,p,p,e,e,p,e,e,e,p,e,e,p,p,p,p,p],
        [f,e,e,e,f,e,e,p,p,e,e,p,e,e,p,e,e,e,p,e,p,e,e,p,e,e,e,p,e,e,e,e],
        [r,e,e,e,e,e,e,p,e,p,e,p,e,e,p,e,e,e,p,e,p,e,p,e,e,e,e,p,e,e,e,e],
        [f,e,e,e,e,e,e,p,e,e,p,p,e,e,p,p,p,p,p,e,p,e,p,e,e,e,e,p,p,p,p,e],
        [r,f,r,f,r,e,e,p,e,e,e,p,e,e,p,e,e,e,p,e,p,p,e,p,e,e,e,p,e,e,e,e],
        [e,e,e,e,f,e,e,p,e,e,e,p,e,e,p,e,e,e,p,e,p,e,e,p,e,e,e,p,e,e,e,e],
        [e,e,e,e,r,e,e,p,e,e,e,p,e,e,p,e,e,e,p,e,p,e,e,e,p,e,e,p,e,e,e,e],
        [e,e,e,e,f,e,e,p,e,e,e,p,e,e,p,e,e,e,p,e,p,e,e,e,p,e,e,p,e,e,e,e],
        [r,e,e,e,r,e,e,p,e,e,e,p,e,e,p,e,e,e,p,e,p,e,e,e,p,e,e,p,e,e,e,e],
        [f,r,f,r,f,e,e,p,e,e,e,p,e,e,p,e,e,e,p,e,p,e,e,e,p,e,e,p,p,p,p,p]
    ]

    self.apple = (random.randrange(1, PLAY_AREA[0] - 2), random.randrange(1, PLAY_AREA[1] - 2))

@master.OnUserUpdate
def main(self):
    handle_controls(self)
    handle_movement(self)
    update_snake(self)
    draw(self)
