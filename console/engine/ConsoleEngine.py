import os, time, keyboard, math, mouse, json
from numba import jit

# jit
# Bresenham algorithm for generating lines
@jit(nopython=True)
def jitBresenham(start: tuple, end: tuple):
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(round(x1), round(x2 + 1)):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

# Mid point circle algorithm --> https://www.geeksforgeeks.org/mid-point-circle-drawing-algorithm/
@jit(nopython=True)
def jitMidPointCircle(centerpos: tuple, radius: int):
    x = radius
    y = 0
    points = [(x + centerpos[0], y + centerpos[1])]

    if radius > 0:
        points.append((y + centerpos[0],   x + centerpos[1]))
        points.append((y + centerpos[0],   centerpos[1] - x))
        points.append((centerpos[0] - x,   y + centerpos[1]))

    p = 1 - radius

    while x > y:
        y += 1
        if p <= 0: p = p + 2 * y + 1
        else: x -= 1;p = p + 2 * y - 2 * x + 1

        if x < y: break

        points.append((x + centerpos[0], y + centerpos[1]))
        points.append((-x + centerpos[0], y + centerpos[1]))
        points.append((x + centerpos[0], -y + centerpos[1]))
        points.append((-x + centerpos[0], -y + centerpos[1]))

        if x != y:
            points.append((y + centerpos[0], x + centerpos[1]))
            points.append((-y + centerpos[0], x + centerpos[1]))
            points.append((y + centerpos[0], -x + centerpos[1]))
            points.append((-y + centerpos[0], -x + centerpos[1]))

    return points

# Fill circle, gives warning
@jit(nopython=True)
def jitFillCircleWithEdge(points: tuple):
    # Sort points into sublists by Y position
    mpoints = points
    mpoints.sort(key = lambda e: e[1])
    spoints = []
    psy = [p[1] for p in mpoints]
    py = psy[0]
    pc = 0

    for c, y in enumerate(psy):
        if y != py:
            spoints.append(mpoints[pc:c])
            pc = c
            py = y

    linesets = []
    for y_sets in spoints:
        x_set = [x[0] for x in y_sets]
        pleft = min(x_set)
        pright = max(x_set)
        linesets.append([(pleft, y_sets[0][1]), (pright, y_sets[0][1])])

    return linesets

# Mathamatical functions from
# http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html
# to fill in triangles (need fill flat bottom and top for this algorithm)
@jit(nopython=True)
def jitFillBottomFlatTriangle(v1: tuple, v2: tuple, v3: tuple):
    invslope1 = (v2[0] - v1[0]) / (v2[1] - v1[1])
    invslope2 = (v3[0] - v1[0]) / (v3[1] - v1[1])

    curx1 = v1[0]
    curx2 = v1[0]

    outpoints = []
    for scanlineY in range(v1[1], v2[1]):
        outpoints.append([(curx1, scanlineY), (curx2, scanlineY)])
        curx1 += invslope1
        curx2 += invslope2

    return outpoints

@jit(nopython=True)
def jitFillTopFlatTriangle(v1: tuple, v2: tuple, v3: tuple):
    invslope1 = (v3[0] - v1[0]) / (v3[1] - v1[1])
    invslope2 = (v3[0] - v2[0]) / (v3[1] - v2[1])

    curx1 = v3[0]
    curx2 = v3[0]

    scanlineY = v3[1]
    outpoints = []
    while scanlineY > v1[1]:
        outpoints.append([(curx1, scanlineY), (curx2, scanlineY)])
        curx1 -= invslope1
        curx2 -= invslope2

        scanlineY -= 1

    return outpoints


# Console Engine Formatting
class FORMAT:
    RESET=              "\033[0m"
    UNDERLINE=          "\033[4m"
    NOUNDERLINE=        "\033[24m"
    BOLD=               "\033[1m"
    NOBOLD=             "\033[22m"
    NEGATIVE=           "\033[7m"
    POSITIVE=           "\033[27m"
    FG_BLACK=           "\033[30m"
    FG_DARK_BLUE=       "\033[34m"
    FG_DARK_GREEN=      "\033[32m"
    FG_DARK_CYAN=       "\033[36m"
    FG_DARK_RED=        "\033[31m"
    FG_DARK_MAGENTA=    "\033[35m"
    FG_DARK_YELLOW =    "\033[33m"
    FG_BBLACK=          "\033[90m"
    FG_BLUE=            "\033[94m"
    FG_GREEN=           "\033[92m"
    FG_CYAN=            "\033[96m"
    FG_RED=             "\033[91m"
    FG_MAGENTA=         "\033[95m"
    FG_YELLOW=          "\033[93m"
    FG_WHITE=           "\033[37m"
    BG_BLACK=           "\033[40m"
    BG_DARK_BLUE=       "\033[44m"
    BG_DARK_GREEN=      "\033[42m"
    BG_DARK_CYAN=       "\033[46m"
    BG_DARK_RED=        "\033[41m"
    BG_DARK_MAGENTA=    "\033[45m"
    BG_DARK_YELLOW=     "\033[43m"
    BG_BBLACK=          "\033[100m"
    BG_BLUE=            "\033[104m"
    BG_GREEN=           "\033[102m"
    BG_CYAN=            "\033[106m"
    BG_RED=             "\033[101m"
    BG_MAGENTA=         "\033[105m"
    BG_YELLOW=          "\033[103m"
    BG_WHITE=           "\033[47m"

    @staticmethod
    def FG_RGB(r:int, g:int, b:int) -> str:
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def BG_RGB(r:int, g:int, b:int) -> str:
        return f"\033[48;2;{r};{g};{b}m"

# Console Engine Pixel Types
class PIXEL_TYPE:
    PIXEL_SOLID = chr(0x2588)
    PIXEL_THREEQUARTERS = chr(0x2593)
    PIXEL_HALF = chr(0x2592)
    PIXEL_QUARTER = chr(0x2591)

    LINE_VERT = "│"
    LINE_HORZ = "─"
    LINE_TOPL = "┌"
    LINE_TOPR = "┐"
    LINE_BTML = "└"
    LINE_BTMR = "┘"

# Console Engine Debug
class DEBUG:
    @staticmethod
    def CursorPos(x: int = 0, y: int = 0): print(f"\033[{y + 1};{x + 1}H", end = '')

    @staticmethod
    def ClearLines(n): print(f"\033[{n}M", end = '')

    @staticmethod
    def InsertLines(n): print(f"\033[{n}L", end = '')

    @staticmethod
    def HideCursor(): print("\033[?25l", end = '')

    @staticmethod
    def ShowCursor(): print("\033[?25h", end = '')

    @staticmethod
    def ClearThisLine(): DEBUG.ClearLines(1);DEBUG.InsertLines(1)

class UI:
    class xInput:
        def __init__(self, parent, pos):
            self.pos = pos
            self.parent = parent
            self.text = ""
            self.isFocused = False

        def Handle(self, inputtext = ""):
            self.parent.Draw(self.pos, self.text)
            if self.isFocused:
                DEBUG.ShowCursor();DEBUG.CursorPos(*self.pos)
                print(" " * len(self.text), end = '')
                DEBUG.CursorPos(*self.pos)
                self.text = input(inputtext)
                DEBUG.HideCursor();DEBUG.CursorPos()
                self.isFocused = False

        def GetText(self):
            return self.text

    def Input(pos: tuple, text: str = "", mode: int = 0):
        DEBUG.ShowCursor();DEBUG.CursorPos(pos[0], pos[1])
        i = input(text)
        DEBUG.HideCursor();DEBUG.CursorPos()
        return i

class ConsoleGame:
    def __init__(self):
        # Initialize variables
        self.title = "Console Game"
        self.geometry = (100, 100)
        self.emptychar = " "
        self.colorsetting = "0f"
        self.clear = True
        self.active = True
        self.safeSizing = 1
        self.root = [[self.emptychar for i in range(self.geometry[0])] for i in range(self.geometry[1] + 1)]
        self.lettersize = (8, 8)

        # Setup deltatime
        self.tp1 = time.monotonic()
        self.tp2 = time.monotonic()

    #
    # DECORATOR FUNCTIONS
    #

    # @self.OnUserCreate --> Executed once on initialization + decorated functions
    def OnUserCreate(self, func):
        func(self)
        self.title = "ConsoleEngine: " + self.title + " - FPS: %fps%"
        # set title, window size and color & Hide cursor
        os.system(f"@echo off & title {self.title} & mode con:cols={self.geometry[0] + self.safeSizing} lines={self.geometry[1] + self.safeSizing} & color {self.colorsetting}")
        DEBUG.HideCursor()

        # Regenerate root array
        self.root = [[self.emptychar for i in range(self.geometry[0])] for i in range(self.geometry[1])]

    # @self.OnUserUpdate --> Loop function, loops and executes decorated function.
    def OnUserUpdate(self, func):
        while self.active:
            # Deltatime
            self.tp2 = time.monotonic()
            elapsedTime = self.tp2 - self.tp1
            self.tp1 = self.tp2
            self.fElapsedTime = elapsedTime

            # Update title
            if self.fElapsedTime != 0:
                os.system("title {}".format(self.title.replace("%fps%", str(round(1/self.fElapsedTime, 2)))))

            # Clear root array
            if self.clear: self.__ClearRoot()

            # Run decorated function
            func(self)

            # Output string + print and reset cursor
            line = ""
            for i in self.root:
                for j in i:
                    line += j # if j != "" else " "
                line += "\n"
            print(line + "\033[H", end='')

    #
    # NON DECORATOR FUNCTIONS
    #

    # Reset root array
    def __ClearRoot(self):
        self.root = [[self.emptychar for i in range(self.geometry[0])] for i in range(self.geometry[1])]

    # Convert special character symbols from codes to string
    def __CharConvert(self, char: str):
        if char[:2] == "&L":
            lum = int(char[2:])
            if lum == 4: char = "█"
            if lum == 3: char = "▓"
            if lum == 2: char = "▒"
            if lum == 1: char = "░"

        return char

    # Place a /char/ at /pos/, check pixel using /place/ --- /fsp/ forces all text into one string
    def Draw(self, pos: tuple, char: str = PIXEL_TYPE.PIXEL_SOLID, place: bool = True, rawc: bool = False, fsp: bool = False):
        if pos[0] > (self.geometry[0] - 1) or pos[1] > (self.geometry[1] - 1) or pos[0] < 0 or pos[1] < 0:
            return False

        if place:
            if len(char) > 1 and not fsp:
                r = 0
                for c in char:
                    if pos[0] + r > (self.geometry[0] - 1) or pos[1] > (self.geometry[1] - 1) or pos[0] < 0 or pos[1] < 0:
                        return False
                    self.root[int(pos[1])][int(pos[0])+r] = c
                    r += 1

            else:
                if char == "": char = " "
                self.root[int(pos[1])][int(pos[0])] = char
        else:
            if self.root[int(pos[1])][int(pos[0])] == char:
                return True

    # Convert string --> functional with colour
    def StringToSprite(self, string: str = PIXEL_TYPE.PIXEL_SOLID, effects: str = FORMAT.FG_RED) -> list:
        string = [[s for s in string]]
        string[0][0] = effects + string[0][0]
        string[0][-1] += FORMAT.RESET
        return string

    # Replace the entire screen array with /plan/
    def RootArray(self, plan: list = []):
        if plan != []: self.root = plan

    # Draw a line from /pos1/ to /pos2/ with /char/ and use /rawc/ to toggle char conversion
    def DrawRawLine(self, pos1: tuple, pos2: tuple, char: str = PIXEL_TYPE.PIXEL_SOLID, rawc: bool = False):
        for point in jitBresenham(pos1, pos2):
            self.Draw(point, char, fsp = True)

    # Draw line /thickness/
    def DrawLine(self, pos1: tuple, pos2: tuple, char: str = PIXEL_TYPE.PIXEL_SOLID, thickness: int = 1, rawc: bool = False):
        if pos1 == pos2:
            self.Draw(pos1, char = char, fsp = True)
            return True

        try: slope = (pos2[1] - pos1[1]) / (pos2[0] - pos1[0])
        except ZeroDivisionError: slope = 1

        if slope >= 1 or slope <= -1:
            for i in range(thickness): self.DrawRawLine((pos1[0]+i,pos1[1]), (pos2[0]+i, pos2[1]), char)
        elif slope < 1 and slope > -1:
            for i in range(thickness): self.DrawRawLine((pos1[0],pos1[1]+i), (pos2[0], pos2[1]+i), char)
        else:
            for i in range(thickness): self.DrawRawLine((pos1[0]+i,pos1[1]+i), (pos2[0]+i, pos2[1]+i), char)

    # Draw a box at /pos/ sized /size/ with /char/, optional /fill/ to fill with a character. /rawc/ + /rawf/ to toggle char conversion
    def DrawBox(self, pos: tuple, size: tuple, char: str = PIXEL_TYPE.PIXEL_SOLID, fill: str = " ", thickness: int = 1, rawc: bool = False, rawf: bool = False):
        point1 = pos
        point2 = (pos[0], pos[1] + size[1])
        point3 = (pos[0] + size[0], pos[1] + size[1])
        point4 = (pos[0] + size[0], pos[1])

        if fill != " " or rawf:
            for x in range(pos[0] + 1, size[0]):
                for y in range(pos[1] + 1, size[1]):
                    self.Draw((x, y), char = fill, fsp = True)

        if thickness == 1:
            self.DrawRawLine(point1, point2, char = char, rawc = True)
            self.DrawRawLine(point2, point3, char = char, rawc = True)
            self.DrawRawLine(point3, point4, char = char, rawc = True)
            self.DrawRawLine(point4, point1, char = char, rawc = True)
        elif thickness > 1:
            self.DrawLine(point1, point2, char = char, rawc = True, thickness = thickness)
            self.DrawLine(point4, point1, char = char, rawc = True, thickness = thickness)

            # adjust for lines to appear on inside
            self.DrawLine((point2[0], point2[1] - thickness + 1),
                            (point3[0], point3[1] - thickness + 1),
                            char = char, rawc = True, thickness = thickness)
            self.DrawLine((point3[0] - thickness + 1, point3[1]),
                            (point4[0] - thickness + 1, point4[1]),
                            char = char, rawc = True, thickness = thickness)
    # Draw Edge Box
    def DrawEdgeBox(self, pos: tuple, size: tuple):
        point1 = pos
        point2 = (pos[0], pos[1] + size[1])
        point3 = (pos[0] + size[0], pos[1] + size[1])
        point4 = (pos[0] + size[0], pos[1])

        self.DrawRawLine(point1, point2, char = PIXEL_TYPE.LINE_VERT, rawc = True)
        self.DrawRawLine(point2, point3, char = PIXEL_TYPE.LINE_HORZ, rawc = True)
        self.DrawRawLine(point3, point4, char = PIXEL_TYPE.LINE_VERT, rawc = True)
        self.DrawRawLine(point4, point1, char = PIXEL_TYPE.LINE_HORZ, rawc = True)

        self.Draw(point1, char = PIXEL_TYPE.LINE_TOPL, fsp = True)
        self.Draw(point2, char = PIXEL_TYPE.LINE_BTML, fsp = True)
        self.Draw(point3, char = PIXEL_TYPE.LINE_BTMR, fsp = True)
        self.Draw(point4, char = PIXEL_TYPE.LINE_TOPR, fsp = True)

    # Draw a triangle with points /pos1/ /pos2/ /pos3/ with /char/, /rawc/ to toggle char conversion.
    def DrawTriangle(self, pos1: tuple, pos2: tuple, pos3: tuple, char: str = PIXEL_TYPE.PIXEL_SOLID, fill: str = " ", thickness: int = 1, rawc: bool = False, rawf: bool = False):
        poss = [pos1, pos2, pos3]
        poss.sort(key = lambda e: e[1])
        pos1, pos2, pos3 = poss[0], poss[1], poss[2]

        if fill != " " or rawf:
            if pos2[1] == pos3[1]:
                for l in jitFillBottomFlatTriangle(pos1, pos2, pos3):
                    self.DrawRawLine(l[0], l[1], char = fill, rawc = True)

            elif pos1[1] == pos2[1]:
                for l in jitFillTopFlatTriangle(pos1, pos2, pos3):
                    self.DrawRawLine(l[0], l[1], char = fill, rawc = True)
            else:
                pos4 = ((pos1[0] + ((pos2[1] - pos1[1]) / (pos3[1] - pos1[1])) * (pos3[0] - pos1[0])), pos2[1])
                for l in jitFillBottomFlatTriangle(pos1, pos2, pos4):
                    self.DrawRawLine(l[0], l[1], char = fill, rawc = True)

                for l in jitFillTopFlatTriangle(pos2, pos4, pos3):
                    self.DrawRawLine(l[0], l[1], char = fill, rawc = True)

                self.DrawRawLine(pos2, pos4, char = fill, rawc = True)

        if thickness == 1:
            self.DrawRawLine(pos1, pos2, char = char, rawc = True)
            self.DrawRawLine(pos2, pos3, char = char, rawc = True)
            self.DrawRawLine(pos1, pos3, char = char, rawc = True)
        if thickness > 1:
            self.DrawLine(pos1, pos2, char = char, rawc = True, thickness = thickness)
            self.DrawLine(pos2, pos3, char = char, rawc = True, thickness = thickness)
            self.DrawLine(pos1, pos3, char = char, rawc = True, thickness = thickness)

    # Draw sprite from array
    def DrawSprite(self, pos: tuple, chararray = []):
        if type(chararray) == dict:
            chararray = chararray["sprite"]

        for y, line in enumerate(chararray):
            for x, pixel in enumerate(line):
                if pixel != "": self.Draw((pos[0] + x, pos[1] + y), char = pixel, fsp = True)

    # Load sprite from .spr file
    def LoadSprite(self, name: str) -> dict:
        with open(name + ".spr", "r") as sprite_file:
            return json.load(sprite_file)

    # Circle centered at /centerpos/ with rad /radius/ drawn with /char/ and filled with /fill/
    def DrawCircle(self, centerpos: tuple, radius: int, char: str = PIXEL_TYPE.PIXEL_SOLID, fill: str = " ", rawc: bool = False, rawf: bool = False):
        circleedge = jitMidPointCircle(centerpos, radius)

        if fill != " " or rawf:
            for l in jitFillCircleWithEdge(circleedge):
                self.DrawRawLine(l[0], l[1], char = fill, rawc = True)

        for point in circleedge:
            self.Draw(point, char, fsp = True)

    # Draw polygon
    def DrawPolygon(self, points: list, char: str = PIXEL_TYPE.PIXEL_SOLID, fill: str = " ", thickness: int = 1, rawc: bool = False, rawf:bool = False):
        prv = points[-1]
        for p in points:
            self.DrawLine(prv, p, char = char, thickness = thickness)

            prv = p

    # Draw text
    def DrawText(self, pos: tuple, text: list, effects: list):
        drawx = 0
        for i, e in enumerate(text):
            if effects[i] == "":
                self.Draw((pos[0] + drawx, pos[1]), e)
            else:
                self.DrawSprite((pos[0] + drawx, pos[1]), self.StringToSprite(e, effects[i]))

            drawx += len(e)

    # Keyboard detection
    def Keyboard(self, key):
        return keyboard.is_pressed(key)

    # Mouse
    def GetMousePos(self, adjusted = True):
        m = mouse.get_position()
        if adjusted:
            return (m[0] / self.lettersize[0], m[1] / self.lettersize[1])
        return m
