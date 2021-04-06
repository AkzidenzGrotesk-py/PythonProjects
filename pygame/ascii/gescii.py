import pygame, sys, time
from pygame.locals import *

class TileSetConfig:
    def __init__(self, custom):
        if custom.lower() == "dwarf_fortress": 
            self.reference = {
                # Char : (x, y)
                " " : (0, 0), "$:)" : (1, 0), "2:0" : (2, 0), "3:0" : (3, 0), "4:0" : (4, 0), "5:0" : (5, 0), "6:0" : (6, 0), "7:0" : (7, 0), "8:0" : (8, 0), "9:0" : (9, 0), "10:0" : (10, 0), "11:0" : (11, 0), "$MALE" : (12, 0), "$FEMALE" : (13, 0), "14:0" : (14, 0), "15:0" : (15, 0),
                ">" : (0, 1), "<" : (1, 1), "2:1" : (2, 1), "$!!" : (3, 1), "$P" : (4, 1), "$S" : (5, 1), "6:1" : (6, 1), "7:1" : (7, 1), "8:1" : (8, 1), "$v" : (9, 1), "$-->" : (10, 1), "$<--" : (11, 1), "12:1" : (12, 1), "$<>" : (13, 1), "$/" : (14, 1), "$\\" : (15, 1),
                "$ " : (0, 2), "!" : (1, 2), "\"" : (2, 2), "#" : (3, 2), "4:2" : (4, 2), "%" : (5, 2), "&" : (6, 2), "\'" : (7, 2), "(" : (8, 2), ")" : (9, 2), "*" : (10, 2), "11:2" : (11, 2), "," : (12, 2), "-" : (13, 2), "." : (14, 2), "/" : (15, 2),
                "0" : (0, 3), "1" : (1, 3), "2" : (2, 3), "3" : (3, 3), "4" : (4, 3), "5" : (5, 3), "6" : (6, 3), "7" : (7, 3), "8" : (8, 3), "9" : (9, 3), ":" : (10, 3), ";" : (11, 3), "$//" : (12, 3), "=" : (13, 3), "$\\\\" : (14, 3), "?" : (15, 3),
                "0:4" : (0, 4), "A" : (1, 4), "B" : (2, 4), "C" : (3, 4), "D" : (4, 4), "E" : (5, 4), "F" : (6, 4), "G" : (7, 4), "H" : (8, 4), "I" : (9, 4), "J" : (10, 4), "K" : (11, 4), "L" : (12, 4), "M" : (13, 4), "N" : (14, 4), "O" : (15, 4),
                "P" : (0, 5), "Q" : (1, 5), "R" : (2, 5), "S" : (3, 5), "T" : (4, 5), "U" : (5, 5), "V" : (6, 5), "W" : (7, 5), "X" : (8, 5), "Y" : (9, 5), "Z" : (10, 5), "[" : (11, 5), "\\" : (12, 5), "]" : (13, 5), "^" : (14, 5), "_" : (15, 5),
                "`" : (0, 6), "a" : (1, 6), "b" : (2, 6), "c" : (3, 6), "d" : (4, 6), "e" : (5, 6), "f" : (6, 6), "g" : (7, 6), "h" : (8, 6), "i" : (9, 6), "j" : (10, 6), "k" : (11, 6), "l" : (12, 6), "m" : (13, 6), "n" : (14, 6), "o" : (15, 6),
                "p" : (0, 7), "q" : (1, 7), "r" : (2, 7), "s" : (3, 7), "t" : (4, 7), "u" : (5, 7), "v" : (6, 7), "w" : (7, 7), "x" : (8, 7), "y" : (9, 7), "z" : (10, 7), "{" : (11, 7), "|" : (12, 7), "}" : (13, 7), "~" : (14, 7), "$^" : (15, 7),
                "0:8" : (0, 8), "1:8" : (1, 8), "2:8" : (2, 8), "3:8" : (3, 8), "4:8" : (4, 8), "5:8" : (5, 8), "6:8" : (6, 8), "7:8" : (7, 8), "8:8" : (8, 8), "9:8" : (9, 8), "10:8" : (10, 8), "11:8" : (11, 8), "12:8" : (12, 8), "13:8" : (13, 8), "14:8" : (14, 8), "15:8" : (15, 8),
                "0:9" : (0, 9), "1:9" : (1, 9), "2:9" : (2, 9), "3:9" : (3, 9), "4:9" : (4, 9), "5:9" : (5, 9), "6:9" : (6, 9), "7:9" : (7, 9), "8:9" : (8, 9), "9:9" : (9, 9), "10:9" : (10, 9), "11:9" : (11, 9), "12:9" : (12, 9), "13:9" : (13, 9), "14:9" : (14, 9), "15:9" : (15, 9),
                "0:10" : (0, 10), "1:10" : (1, 10), "2:10" : (2, 10), "3:10" : (3, 10), "4:10" : (4, 10), "5:10" : (5, 10), "6:10" : (6, 10), "7:10" : (7, 10), "8:10" : (8, 10), "9:10" : (9, 10), "10:10" : (10, 10), "11:10" : (11, 10), "12:10" : (12, 10), "13:10" : (13, 10), "14:10" : (14, 10), "15:10" : (15, 10),
                "0:11" : (0, 11), "1:11" : (1, 11), "2:11" : (2, 11), "3:11" : (3, 11), "4:11" : (4, 11), "5:11" : (5, 11), "6:11" : (6, 11), "7:11" : (7, 11), "8:11" : (8, 11), "9:11" : (9, 11), "10:11" : (10, 11), "11:11" : (11, 11), "12:11" : (12, 11), "13:11" : (13, 11), "14:11" : (14, 11), "15:11" : (15, 11),
                "0:12" : (0, 12), "1:12" : (1, 12), "2:12" : (2, 12), "3:12" : (3, 12), "4:12" : (4, 12), "5:12" : (5, 12), "6:12" : (6, 12), "7:12" : (7, 12), "8:12" : (8, 12), "9:12" : (9, 12), "10:12" : (10, 12), "11:12" : (11, 12), "12:12" : (12, 12), "13:12" : (13, 12), "14:12" : (14, 12), "15:12" : (15, 12),
                "0:13" : (0, 13), "1:13" : (1, 13), "2:13" : (2, 13), "3:13" : (3, 13), "4:13" : (4, 13), "5:13" : (5, 13), "6:13" : (6, 13), "7:13" : (7, 13), "8:13" : (8, 13), "9:13" : (9, 13), "10:13" : (10, 13), "$|#|" : (11, 13), "12:13" : (12, 13), "13:13" : (13, 13), "14:13" : (14, 13), "15:13" : (15, 13),
                "0:14" : (0, 14), "1:14" : (1, 14), "2:14" : (2, 14), "3:14" : (3, 14), "4:14" : (4, 14), "5:14" : (5, 14), "6:14" : (6, 14), "7:14" : (7, 14), "8:14" : (8, 14), "9:14" : (9, 14), "10:14" : (10, 14), "11:14" : (11, 14), "12:14" : (12, 14), "13:14" : (13, 14), "14:14" : (14, 14), "15:14" : (15, 14),
                "0:15" : (0, 15), "1:15" : (1, 15), "2:15" : (2, 15), "3:15" : (3, 15), "4:15" : (4, 15), "5:15" : (5, 15), "6:15" : (6, 15), "7:15" : (7, 15), "8:15" : (8, 15), "9:15" : (9, 15), "10:15" : (10, 15), "11:15" : (11, 15), "12:15" : (12, 15), "13:15" : (13, 15), "14:15" : (14, 15), "15:15" : (15, 15),
            }
        
        else: self.reference = custom

class ASCIIPanel:
    def __init__(self, windowWidth, windowHeight, title, tileset_image, tile_width, tile_height, tscfg):
        pygame.init()
        def load_tile_table(filename, tile_width, tile_height):
            tileset_image = pygame.image.load(filename)
            # magenta = pygame.Color(255, 0, 255)
            # tileset_image.set_colorkey(magenta)
            image_width, image_height = tileset_image.get_size()
            tile_table = []
            for tile_x in range(int(image_width / tile_width)):
                line = []
                tile_table.append(line)
                for tile_y in range(int(image_height / tile_height)):
                    rect = (
                        tile_x * tile_width, 
                        tile_y * tile_height,
                        tile_width,
                        tile_height
                    )
                    line.append(tileset_image.subsurface(rect))
            return tile_table

        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.pixelWindowWidth = windowWidth * self.tile_width
        self.pixelWindowHeight = windowHeight * self.tile_height
        self.TileSetCfgReference = tscfg.reference

        self.ascii_tileset = load_tile_table(tileset_image, tile_width, tile_height)
        self.ArialFont = pygame.font.SysFont('Arial Bold', 30)

        self.master = pygame.display.set_mode((self.pixelWindowWidth, self.pixelWindowHeight))
        pygame.display.set_caption(title)

    def clamp(self, in_, min, max):
        '''Clamp a value between two values'''
        if in_ < min: return min
        if in_ > max: return max
        else: return in_

    def deltatime(self, init_ = False):
        if init_:
            self.tp1 = time.monotonic()
            self.tp2 = time.monotonic()

            return True
        else:
            self.tp2 = time.monotonic()
            elapsedTime = self.tp2 - self.tp1
            self.tp1 = self.tp2

            return elapsedTime

    def fps(self, deltatime, fps_color):
        try:
            return self.ArialFont.render(str(round(1.0 / deltatime, 2)), False, fps_color)
        except:
            return self.ArialFont.render("0.0", False, fps_color)

    def on_debug(self, x, y, surface):
        self.master.blit(surface, (x, y))

    def texture(self, x, y, texture):
        for l in range(len(texture['chars'])):
            for r in range(len(texture['chars'][l])):
                xb = self.clamp(x + l, 0, self.pixelWindowWidth - self.tile_width)
                yb = self.clamp(y + r, 0, self.pixelWindowHeight - self.tile_height)

                self.char(
                    xb, yb, 
                    texture['chars'][l][r], 
                    texture['colormap'][texture['color'][l][r]]
                )

    def char(self, x, y, char, rgb):
        def colorize(image, newColor):
            copy_image = image.copy()

            copy_image.fill((0,0,0,255), None, pygame.BLEND_RGBA_MULT)
            copy_image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

            return copy_image

        fx = self.clamp(x * self.tile_width, 0, self.pixelWindowWidth - self.tile_width)
        fy = self.clamp(y * self.tile_height, 0, self.pixelWindowHeight - self.tile_height)

        self.master.blit(
            colorize(self.ascii_tileset[self.TileSetCfgReference[char][0]][self.TileSetCfgReference[char][1]], rgb), 
            (fx, fy)
        )

    def check_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def clear(self):
        self.master.fill((0, 0, 0))

    def update(self):
        pygame.display.flip()
