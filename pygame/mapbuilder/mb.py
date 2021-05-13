import pygame, sys, time, json
pygame.init()

class Colours:
    def __init__(self):
        self.background = (238, 238, 238)
        self.secondarybackground = (220, 220, 250)
        self.ninedots = (0, 0, 0)
        self.primarydots = (150, 150, 150)
        self.secondarydots = (200, 200, 200)
        self.selectedot = (15, 15, 255)
        self.line = (0, 0, 0)
        self.selectedline = (200, 15, 15)

        self.UI_background = (255, 255, 255)
        self.UI_border = (15, 15, 255)
        self.UI_backgroundhover = (200, 200, 200)

class UIButton:
    def __init__(self, parent, pos = [0, 0], size = [32, 32]):
        self.parent = parent
        self.pos = pos
        self.size = size
        self.rstate = 0
        self.theme = Colours()

        self.image = [False, [0, 0], 0, [0, 0], 0]
        self.bordercolor = self.theme.UI_border
        self.bgnorm = self.theme.UI_background
        self.bghov = self.theme.UI_backgroundhover

    def render_on_frame(self, surface):
        if self.image[0]:
            if self.rstate == 0:
                pygame.draw.rect(surface, self.bgnorm, [*self.pos, *self.size])
                pygame.draw.rect(surface, self.bordercolor, [*self.pos, *self.size], width = 1)
                surface.blit(self.image[2], (self.image[1][0] + self.pos[0], self.image[1][1] + self.pos[1]))
            if self.rstate == 1:
                pygame.draw.rect(surface, self.bghov, [*self.pos, *self.size])
                pygame.draw.rect(surface, self.bordercolor, [*self.pos, *self.size], width = 1)
                surface.blit(self.image[4], (self.image[3][0] + self.pos[0], self.image[3][1] + self.pos[1]))
        else:
            if self.rstate == 0:
                pygame.draw.rect(surface, self.bgnorm, [*self.pos, *self.size])
                pygame.draw.rect(surface, self.bordercolor, [*self.pos, *self.size], width = 1)
            if self.rstate == 1:
                pygame.draw.rect(surface, self.bghov, [*self.pos, *self.size])
                pygame.draw.rect(surface, self.bordercolor, [*self.pos, *self.size], width = 1)

    def event_on_frame(self, mousepos, mousestate):
        s = False
        if mousepos[0] > self.pos[0] and mousepos[0] < self.pos[0] + self.size[0]:
            if mousepos[1] > self.pos[1] and mousepos[1] < self.pos[1] + self.size[1]:
                self.rstate = 1
                self.parent.cancel = True

                if mousestate[0]:
                    return True
                s = True
        if not s: self.rstate = 0
        return False

class MapBuilder:
    def __init__(self):
        self.setup()
        self.loop()

    def setup(self):
        # game
        self.dotdist = 4
        self.selected = 0
        self.selectedpoint = -1
        self.selectedcirc = -1
        self.size = [500, 500]
        self.map_size = [30, 30]
        self.camerapos = [0, 0]
        self.grid = True
        self.theme = Colours()
        self.title = "Map Builder :: %filename%"
        self.cfile = "NewMap.mb"
        self.cancel = False

        # button
        self.btntest = UIButton(self, [8, 8], [32, 32])
        self.btntest.image = [True, [0, 0], pygame.image.load('next_norm.png'), [0, 0], pygame.image.load('next_hovr.png')]
        self.btntest.bghov = self.btntest.bgnorm

        # points
        self.data = {"lines" : [[]], "circles" : [[]], "map_size" : self.map_size}

        # deltatime
        self.tp1 = time.monotonic()
        self.tp2 = time.monotonic()

        # config
        self.active = True
        self.icon_image = pygame.image.load("mapbuilderlogo.PNG")

        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon_image)
        self.root = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

    def add_new_line_segment(self):
        if self.data["lines"][-1] != []:
            self.data["lines"].append([])
            self.selected = len(self.data["lines"]) - 1
        elif self.data["lines"][-1] == []:
            self.selected = len(self.data["lines"]) - 1

    def events(self, event):
        if event.type == pygame.QUIT:
            self.active = False

        ### RESIZE
        if event.type == pygame.VIDEORESIZE:
            self.size = (event.w, event.h)
            self.root = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

        ### MOUSE BUTTONS
        if event.type == pygame.MOUSEBUTTONDOWN:
            speed = 1000.0 * self.fElapsedTime
            # Add new point to currently selected line
            if not self.cancel:
                if event.button == 1:
                    thispoint = [round((self.camerapos[0] + self.mouse[0]) / self.dotdist), round((self.camerapos[1] + self.mouse[1]) / self.dotdist)]
                    n = False
                    for i, p in enumerate(self.data["lines"][self.selected]):
                        if p == thispoint:
                            self.selectedpoint = i
                            n = True

                    if not n:
                        if self.selectedpoint == -1:
                            self.data["lines"][self.selected].append(thispoint)
                            self.selectedpoint += 1
                        else:
                            self.data["lines"][self.selected].insert(self.selectedpoint+1, thispoint)
                            self.selectedpoint += 1
                        self.selectedpoint = -1

                if event.button == 3:
                    thispoint = [round((self.camerapos[0] + self.mouse[0]) / self.dotdist), round((self.camerapos[1] + self.mouse[1]) / self.dotdist), 3]
                    n = False
                    for i, p in enumerate(self.data["circles"]):
                        if p != []:
                            if p[0] == thispoint[0] and p[1] == thispoint[1]:
                                self.selectedcirc = i
                                n = True

                    if not n:
                        if self.selectedcirc == -1:
                            self.data["circles"].append(thispoint)
                            self.selectedcirc += 1
                        else:
                            self.data["circles"].insert(self.selectedcirc+1, thispoint)
                            self.selectedcirc += 1
                        self.selectedcirc = -1
            # Zoom in and out and pan
            if event.button == 4:
                if self.keys[pygame.K_LSHIFT]: self.camerapos[0] -= speed
                elif self.keys[pygame.K_LCTRL]: self.dotdist += 1
                else: self.camerapos[1] -= speed

            if event.button == 5 and self.dotdist > 1:
                if self.keys[pygame.K_LSHIFT]: self.camerapos[0] += speed
                elif self.keys[pygame.K_LCTRL]: self.dotdist -= 1
                else: self.camerapos[1] += speed

        ### KEYDOWNS
        if event.type == pygame.KEYDOWN:

            # Add new line
            if event.key == pygame.K_RETURN:
                self.add_new_line_segment()

            if self.keys[pygame.K_LCTRL]:
                # Remove current line
                if event.key == pygame.K_x and self.data["lines"][self.selected] != []:
                    del self.data["lines"][self.selected]
                    if self.selected > 4: self.selected -= 1
                    if len(self.data["lines"]) == 0: self.data["lines"] = [[]]

                # Map size
                if event.key == pygame.K_w and self.map_size[1] > 2:
                    self.map_size[1] -= 2
                if event.key == pygame.K_s:
                    self.map_size[1] += 2
                if event.key == pygame.K_a and self.map_size[0] > 2:
                    self.map_size[0] -= 2
                if event.key == pygame.K_d:
                    self.map_size[0] += 2
            else:
                # Select next line
                if event.key == pygame.K_w and self.selected < len(self.data["lines"]) - 1:
                    self.selected += 1

                # Select last line
                if event.key == pygame.K_s and self.selected > 0:
                    self.selected -= 1

                # Circle size
                if self.selectedcirc != -1:
                    if event.key == pygame.K_a and self.data["circles"][self.selectedcirc][2] > 1:
                        self.data["circles"][self.selectedcirc][2] -= 1

                    # Select last line
                    if event.key == pygame.K_d:
                        self.data["circles"][self.selectedcirc][2] += 1

                # Remove point
                if event.key == pygame.K_x and 0 < len(self.data["lines"][self.selected]):
                    del self.data["lines"][self.selected][self.selectedpoint]
                    if self.selectedpoint > -1: self.selectedpoint -= 1

                # Remove circle
                if event.key == pygame.K_y and len(self.data["circles"]) > 0:
                    del self.data["circles"][self.selectedcirc]
                    if self.selectedcirc > -1: self.selectedcirc -= 1

            # Toggle grid
            if event.key == pygame.K_q:
                self.grid = not self.grid

            # File
            if event.key == pygame.K_s and self.keys[pygame.K_RCTRL] and self.keys[pygame.K_RSHIFT]:
                filename = input("save loc: ")
                try:
                    self.data["map_size"] = self.map_size
                    with open(filename, "w") as file:
                        json.dump(self.data, file)
                    self.cfile = filename
                except: print("error saving to file")
            elif event.key == pygame.K_s and self.keys[pygame.K_RCTRL]:
                if self.cfile == "NewMap.mb":
                    filename = input("save loc: ")
                    try:
                        self.data["map_size"] = self.map_size
                        with open(filename, "w") as file:
                            json.dump(self.data, file)
                        self.cfile = filename
                    except: print("error saving to file")
                else:
                    self.data["map_size"] = self.map_size
                    with open(self.cfile, "w") as file:
                        json.dump(self.data, file)

            if event.key == pygame.K_o and self.keys[pygame.K_RCTRL]:
                filename = input("filename: ")
                try:
                    with open(filename, "r") as file:
                        self.data = json.load(file)
                    self.map_size = self.data["map_size"]
                    self.cfile = filename
                except: print("error loading file [", filename, "]")


    def key_events(self):
        self.mouse = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()
        self.mousekeys = pygame.mouse.get_pressed()

        if not self.cancel:
            if self.mousekeys[0] and self.selectedpoint != -1:
                thispoint = [round((self.camerapos[0] + self.mouse[0]) / self.dotdist), round((self.camerapos[1] + self.mouse[1]) / self.dotdist)]
                self.data["lines"][self.selected][self.selectedpoint] = thispoint
            if self.mousekeys[2] and self.selectedcirc != -1:
                thispoint = [round((self.camerapos[0] + self.mouse[0]) / self.dotdist), round((self.camerapos[1] + self.mouse[1]) / self.dotdist), self.data["circles"][self.selectedcirc][2]]
                self.data["circles"][self.selectedcirc] = thispoint

        if self.btntest.event_on_frame(self.mouse, self.mousekeys):
            self.add_new_line_segment()

    def deltatime(self):
        self.tp2 = time.monotonic()
        elapsedTime = self.tp2 - self.tp1
        self.tp1 = self.tp2
        self.fElapsedTime = elapsedTime

        if self.fElapsedTime != 0:
            self.fps = round(1/self.fElapsedTime)
            pygame.display.set_caption(self.title.replace("%fps%", str(self.fps)).replace("%filename%", self.cfile))

    def loop(self):
        while self.active:
            self.root.fill(self.theme.secondarybackground)
            self.deltatime()
            self.key_events()
            for event in pygame.event.get():
                self.events(event)

            ### DRAWING PANEL
            # render border
            m = self.dotdist * 2
            pygame.draw.rect(self.root, self.theme.background, [-self.camerapos[0] - m, -self.camerapos[1] - m, self.map_size[0] * 4 * self.dotdist + m*2, self.map_size[1] * 4 * self.dotdist + m*2])
            pygame.draw.rect(self.root, self.theme.selectedline, [-self.camerapos[0] - m, -self.camerapos[1] - m, self.map_size[0] * 4 * self.dotdist + m*2, self.map_size[1] * 4 * self.dotdist + m*2], width = 1)

            # render grid
            if self.grid:
                for x in range(0, int(self.map_size[0] * 4 + 1)):
                    if (x * self.dotdist - self.camerapos[0]) > self.size[0]: break # quit if OOB
                    for y in range(0, int(self.map_size[1] * 4 + 1)):
                        if (y * self.dotdist - self.camerapos[1]) > self.size[1]: break # quit if OOB
                        if x % 8 == 0 and y % 8 == 0:
                            c = self.theme.ninedots
                            s = 2
                        elif x % 4 == 0 and y % 4 == 0:
                            c = self.theme.primarydots
                            s = 1
                        else:
                            c = self.theme.secondarydots
                            s = 1

                        # draw point
                        pygame.draw.circle(self.root, c, (x * self.dotdist - self.camerapos[0], y * self.dotdist - self.camerapos[1]), s, width = 1)

            # render points
            for i, s in enumerate(self.data["lines"]):
                color = self.theme.selectedline if i == self.selected else self.theme.line
                if s != []:
                    prevp = s[-1]
                    for j, p in enumerate(s):
                        pcolor = self.theme.selectedot if self.selectedpoint == j and self.selected == i else color
                        lcolor = self.theme.selectedot if (0 if self.selectedpoint + 1 > len(s) - 1 else self.selectedpoint + 1) == j and self.selected == i else color

                        if self.grid:
                            pygame.draw.circle(self.root, pcolor, (p[0] * self.dotdist - self.camerapos[0], p[1] * self.dotdist - self.camerapos[1]), 2)
                        pygame.draw.line(self.root, lcolor, [prevp[0] * self.dotdist - self.camerapos[0], prevp[1] * self.dotdist - self.camerapos[1]], [p[0] * self.dotdist - self.camerapos[0], p[1] * self.dotdist - self.camerapos[1]], 1)
                        prevp = p

            # render circles
            for i, c in enumerate(self.data["circles"]):
                if c != []:
                    xs = c[0] * self.dotdist - self.camerapos[0]
                    ys = c[1] * self.dotdist - self.camerapos[1]
                    color = self.theme.selectedline if i == self.selectedcirc else self.theme.line
                    if self.grid:
                        pygame.draw.line(self.root, color, [xs, ys], [xs + c[2] * self.dotdist, ys], 1)
                        pygame.draw.circle(self.root, color, (xs, ys), 2)
                        pygame.draw.circle(self.root, color, (xs + c[2] * self.dotdist, ys), 2)
                    pygame.draw.circle(self.root, color, (xs, ys), c[2] * self.dotdist, width = 1)

            ### UI
            # render UI Frame
            pygame.draw.rect(self.root, self.theme.UI_background, [8, 8, 32, 256])
            pygame.draw.rect(self.root, self.theme.UI_border, [8, 8, 32, 256], width = 1)
            self.btntest.render_on_frame(self.root)

            pygame.display.flip()
            self.cancel = False
        sys.exit()

if __name__ == "__main__":
    app = MapBuilder()
