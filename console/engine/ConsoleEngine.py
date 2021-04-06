import os, time, keyboard, math

# FORMAT CAUSES MANY BUGS
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

class PIXEL_TYPE:
    PIXEL_SOLID = chr(0x2588)
    PIXEL_THREEQUARTERS = chr(0x2593)
    PIXEL_HALF = chr(0x2592)
    PIXEL_QUARTER = chr(0x2591)

class vector:
    def __init__(self, x = 0, y = 0, z = 0, w = 0):
        self.x, self.y, self.z, self.w = x, y, z, w

    def __add__(self, e):
        return vector(e.x + self.x, e.y + self.y, e.z + self.z, e.w + self.w)

class ConsoleGame:
    def __init__(self):
        # Initialize variables
        self.title = "%fps%"
        self.fpsInTitle = True
        self.geometry = (100, 100)
        self.emptychar = " "
        self.colorsetting = "0f"
        self.clear = True
        self.active = True
        self.safeSizing = 1
        self.root = [[self.emptychar for i in range(self.geometry[0])] for i in range(self.geometry[1] + 1)]

        # Setup deltatime
        self.tp1 = time.monotonic()
        self.tp2 = time.monotonic()

    #
    # DECORATER FUNCTIONS
    #

    # @self.OnUserCreate --> Executed once on initialization + decorated functions
    def OnUserCreate(self, func):
        func(self)
        if self.title.replace("%fps%", "") == self.title: self.fpsInTitle = False
        # set title, window size and color & Hide cursor
        os.system(f"@echo off & title {self.title} & mode con:cols={self.geometry[0] + self.safeSizing} lines={self.geometry[1] + self.safeSizing} & color {self.colorsetting}")
        print("\033[?25l")

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
            if self.fElapsedTime != 0 and self.fpsInTitle:
                os.system("title {}".format(self.title.replace("%fps%", str(round(1/self.fElapsedTime, 2)))))

            # Clear root array
            if self.clear: self.__ClearRoot()

            # Run decorated function
            func(self)

            # Output string + print and reset cursor
            line = ""
            for i in self.root:
                for j in i:
                    line += j
                line += "\n"
            print(line + "\033[H", end='')

    #
    # NON DECORATION FUNCTIONS
    #

    # Reset root array
    def __ClearRoot(self):
        self.root = [[self.emptychar for i in range(self.geometry[0])] for i in range(self.geometry[1])]

    # Bresenham algorithm for generating lines
    def __Bresenham(self, start, end):
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
    def __MidPointCircle(self, centerpos, radius):
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

    # Fill circle
    def __FillCircleWithEdge(self, points, char = PIXEL_TYPE.PIXEL_SOLID, rawc = False):
        # Sort points into sublists by Y position
        points.sort(key = lambda e: e[1])
        spoints = []
        psy = [p[1] for p in points]
        py = psy[0]
        pc = 0

        for c, y in enumerate(psy):
            if y != py:
                spoints.append(points[pc:c])
                pc = c
                py = y

        for y_sets in spoints:
            x_set = [x[0] for x in y_sets]
            pleft = min(*x_set)
            pright = max(*x_set)
            self.DrawRawLine((pleft, y_sets[0][1]), (pright, y_sets[0][1]), char = char, rawc = True)

    # Convert special character symbols from codes to string
    def __CharConvert(self, char):
        if char[:2] == "&L":
            lum = int(char[2:])
            if lum == 4: char = "█"
            if lum == 3: char = "▓"
            if lum == 2: char = "▒"
            if lum == 1: char = "░"

        return char

    # Mathamatical functions from
    # http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html
    # to fill in triangles (need fill flat bottom and top for this algorithm)
    def __FillBottomFlatTriangle(self, v1, v2, v3, char = PIXEL_TYPE.PIXEL_SOLID, rawc = False):
        invslope1 = (v2[0] - v1[0]) / (v2[1] - v1[1])
        invslope2 = (v3[0] - v1[0]) / (v3[1] - v1[1])

        curx1 = v1[0]
        curx2 = v1[0]

        for scanlineY in range(v1[1], v2[1]):
            self.DrawRawLine((curx1, scanlineY), (curx2, scanlineY), char = char, rawc = True)
            curx1 += invslope1
            curx2 += invslope2
    def __FillTopFlatTriangle(self, v1, v2, v3, char = PIXEL_TYPE.PIXEL_SOLID, rawc = False):
        invslope1 = (v3[0] - v1[0]) / (v3[1] - v1[1])
        invslope2 = (v3[0] - v2[0]) / (v3[1] - v2[1])

        curx1 = v3[0]
        curx2 = v3[0]

        scanlineY = v3[1]
        while scanlineY > v1[1]:
            self.DrawRawLine((curx1, scanlineY), (curx2, scanlineY), char = char, rawc = True)
            curx1 -= invslope1
            curx2 -= invslope2

            scanlineY -= 1

    # Place a /char/ at /pos/, check pixel using /place/ --- /fsp/ forces all text into one string
    def Pixel(self, pos, char = PIXEL_TYPE.PIXEL_SOLID, place = True, rawc = False, fsp = False):
        if pos[0] > (self.geometry[0] - 1) or pos[1] > (self.geometry[1] - 1) or pos[0] < 0 or pos[1] < 0:
            return False

        if place:
            if len(char) > 1 and not fsp:
                r = 0
                for c in char:
                    if pos[0] + r > (self.geometry[0] - 1) or pos[1] > (self.geometry[1] - 1) or pos[0] < 0 or pos[1] < 0:
                        return False
                    self.root[pos[1]][pos[0]+r] = c
                    r += 1

            else: self.root[pos[1]][pos[0]] = char
        else:
            if self.root[pos[1]][pos[0]] == char:
                return True

    # Replace the entire screen array with /plan/
    def RootArray(self, plan = []):
        if plan != []: self.root = plan

    # Draw a line from /pos1/ to /pos2/ with /char/ and use /rawc/ to toggle char conversion
    def DrawRawLine(self, pos1, pos2, char = PIXEL_TYPE.PIXEL_SOLID, rawc = False):
        for point in self.__Bresenham(pos1, pos2):
            self.Pixel(point, char, fsp = True)

    # Draw line /thickness/
    def DrawLine(self, pos1, pos2, char = PIXEL_TYPE.PIXEL_SOLID, thickness = 1, rawc = False):
        if pos1 == pos2:
            self.Pixel(pos1, char = char, fsp = True)
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
    def DrawBox(self, pos, size, char = PIXEL_TYPE.PIXEL_SOLID, fill = " ", thickness = 1, rawc = False, rawf = False):
        point1 = pos
        point2 = (pos[0], pos[1] + size[1])
        point3 = (pos[0] + size[0], pos[1] + size[1])
        point4 = (pos[0] + size[0], pos[1])

        if fill != " " or rawf:
            for x in range(pos[0] + 1, size[0]):
                for y in range(pos[1] + 1, size[1]):
                    self.Pixel((x, y), char = fill, fsp = True)

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

    # Draw a triangle with points /pos1/ /pos2/ /pos3/ with /char/, /rawc/ to toggle char conversion.
    def DrawTriangle(self, pos1, pos2, pos3, char = PIXEL_TYPE.PIXEL_SOLID, fill = " ", thickness = 1, rawc = False, rawf = False):
        poss = [pos1, pos2, pos3]
        poss.sort(key = lambda e: e[1])
        pos1, pos2, pos3 = poss[0], poss[1], poss[2]

        if fill != " " or rawf:
            if pos2[1] == pos3[1]:
                self.__FillBottomFlatTriangle(pos1, pos2, pos3, char = fill, rawc = True)
            elif pos1[1] == pos2[1]:
                self.__FillTopFlatTriangle(pos1, pos2, pos3, char = fill, rawc = True)
            else:
                pos4 = ((pos1[0] + ((pos2[1] - pos1[1]) / (pos3[1] - pos1[1])) * (pos3[0] - pos1[0])), pos2[1])
                self.__FillBottomFlatTriangle(pos1, pos2, pos4, char = fill, rawc = True)
                self.__FillTopFlatTriangle(pos2, pos4, pos3, char = fill, rawc = True)
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
    def DrawSprite(self, pos, chararray = []):
        for y, line in enumerate(chararray):
            for x, pixel in enumerate(line):
                if pixel != "": self.Pixel((pos[0] + x, pos[1] + y), char = pixel)

    # Circle centered at /centerpos/ with rad /radius/ drawn with /char/ and filled with /fill/
    def DrawCircle(self, centerpos, radius, char = PIXEL_TYPE.PIXEL_SOLID, fill = " ", rawc = False, rawf = False):
        circleedge = self.__MidPointCircle(centerpos, radius)

        if fill != " " or rawf:
            self.__FillCircleWithEdge(circleedge, char = fill, rawc = True)

        for point in circleedge:
            self.Pixel(point, char, fsp = True)

    # Keyboard detection
    def Keyboard(self, key):
        return keyboard.is_pressed(key)
