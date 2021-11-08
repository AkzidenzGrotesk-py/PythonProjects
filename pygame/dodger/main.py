import pygame, sys, json, random, os
from numpy import random as nrand
pygame.init()

# Game Concept
# > Toshing system w/ different tools
#   > Comb, Sieve, Gloves (additional: Spoon, Stick)
#   > Different modes for each?
# > Map system?
#
# TODO
# > Art
# > Crude animations on button press (to tosh)
# > Random for coins recieved

vector2 = pygame.math.Vector2
FRAMERATES = [20, 24, 30, 45, 60, 72, 90, 92, 120]

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class Button:
    def __init__(self, pos, size, obj, surface, pos_scale = 1):
        self.pos = pos
        self.obj = obj
        self.size = size
        self.surf = surface
        self.pos_scale = pos_scale
        self.overrides = [False, (), ()]

        self.hover_obj = obj

    def render(self, hover = False):
        if not hover: self.surf.blit(self.obj, self.pos)
        if hover: self.surf.blit(self.hover_obj, self.pos)

    def intercept(self, mouse):
        if self.overrides[0]:
            if (self.overrides[1][0] + self.overrides[2][0]) * self.pos_scale >= mouse[0] >= self.overrides[1][0] * self.pos_scale:
                if (self.overrides[1][1] + self.overrides[2][1]) * self.pos_scale >= mouse[1] >= self.overrides[1][1] * self.pos_scale:
                    return True

        else:
            if (self.pos[0] + self.size[0]) * self.pos_scale >= mouse[0] >= self.pos[0] * self.pos_scale:
                if (self.pos[1] + self.size[1]) * self.pos_scale >= mouse[1] >= self.pos[1] * self.pos_scale:
                    return True

class Comb:
    def __init__(self, this):
        self.this = this
        self.x_axis = 16
        self.disabled = False
        self.perma_coin_render = False
        self.oneframe = 0

        self.surf = pygame.Surface((135, 360), pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        self.surf.blit(self.this.sprites["comb"], (0, 0))
        self.rect = self.surf.get_rect()

        self.pos = vector2(
            self.x_axis,
            360
        )

    def reset_surface(self):
        self.surf = pygame.Surface((135, 360), pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        self.surf.blit(self.this.sprites["comb"], (0, 0))
        self.rect = self.surf.get_rect()

    def render_coin(self):
        if self.n_of_coins >= 1:
            for c in self.coins:
                c_spr = self.n_to_coin(c[0])
                self.this.master.blit(c_spr, (c[1], c[2]))

    def update(self):
        if self.this.keys[pygame.K_LEFT] and not self.disabled:
            if self.pos.x > 10:
                self.pos.x -= 8 * self.this.framecoeff
                self.jiggle()
        if self.this.keys[pygame.K_RIGHT] and not self.disabled:
            if self.pos.x < 575:
                self.pos.x += 5 * self.this.framecoeff
                self.jiggle()
        if self.this.keys[pygame.K_q]:
            if self.pos.x >= 570 or self.perma_coin_render:
                if self.n_of_coins >= 1:
                    self.this.sounds["coins_collect"].play()
                    for c in self.coins:
                        self.this.pence += self.n_to_value(c[0])
                    self.n_of_coins = 0

        self.reset_surface()
        if self.pos.x >= 570 or self.perma_coin_render:
            if self.oneframe <= 1: self.oneframe += 1
            self.render_coin()
            self.perma_coin_render = True
            if self.oneframe == 1:
                for x in range(self.n_of_coins): self.this.coins_sound[random.randrange(0,5)].play()

        if self.pos.x <= 15:
            if self.n_of_coins >= 1 and self.oneframe >= 1:
                self.this.sounds["coins_collect"].play()
                for c in self.coins:
                    self.this.pence += self.n_to_value(c[0])
            self.reset()


        self.rect.midbottom = self.pos


    def n_to_coin(self, c):
        c_spr = self.this.coin_set[0][0]
        if c == 1: c_spr = self.this.coin_set[0][0]
        elif c == 2: c_spr = self.this.coin_set[1][0]
        elif c == 3: c_spr = self.this.coin_set[2][0]
        elif c == 4: c_spr = self.this.coin_set[3][0]
        elif c == 5: c_spr = self.this.coin_set[4][0]
        elif c == 6: c_spr = self.this.coin_set[5][0]
        elif c == 7: c_spr = self.this.coin_set[0][1]
        elif c == 8: c_spr = self.this.coin_set[1][1]
        elif c == 9: c_spr = self.this.coin_set[2][1]
        elif c == 10: c_spr = self.this.coin_set[3][1]
        elif c == 11: c_spr = self.this.coin_set[4][1]
        elif c == 12: c_spr = self.this.coin_set[5][1]
        elif c == 13: c_spr = self.this.coin_set[0][2]
        elif c == 14: c_spr = self.this.coin_set[1][2]
        return c_spr

    def n_to_value(self, c):
        c_val = 1/8
        if c == 1: c_val = 1/8
        elif c == 2: c_val = 1/4
        elif c == 3: c_val = 1/2
        elif c == 4: c_val = 1
        elif c == 5: c_val = 3
        elif c == 6: c_val = 4
        elif c == 7: c_val = 6
        elif c == 8: c_val = 12
        elif c == 9: c_val = 24
        elif c == 10: c_val = 30
        elif c == 11: c_val = 48
        elif c == 12: c_val = 60
        elif c == 13: c_val = 120
        elif c == 14: c_val = 240
        return c_val

    def jiggle(self):
        self.pos.y += random.randrange(-1, 1)
        if self.pos.y > 363: self.pos.y -= 3 * self.this.framecoeff
        if self.pos.y < 357: self.pos.y += 3 * self.this.framecoeff

    def reset(self, sound = True):
        self.disabled = True
        self.perma_coin_render = False
        self.oneframe = 0
        self.pos.x = 16
        n_of_coins = round(nrand.normal(loc=3, scale=3))
        if n_of_coins <= 1: n_of_coins = 1
        self.n_of_coins = n_of_coins
        self.coins = []

        for j in range(self.n_of_coins):
            j_value = nrand.normal(loc=1, scale=7)
            if j_value >= 10: j_value = nrand.normal(loc=1, scale=7)

            if j_value <= 0: j_value = 1
            if j_value >= 14: j_value = 14
            self.coins.append([round(j_value), random.randrange(598, 640 - 25), random.randrange(48, 360 - 30 - 48)])

        self.reset_surface()

        self.disabled = False




class Sieve:
    def __init__(self, this):
        self.data = {
            "globalstate" : 0,
            "shakestate" : 0,
            "frame_dip" : 0
        }
        self.this = this

        self.surf = pygame.Surface((350, 350), pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        self.surf.blit(self.this.sprites["sieve"]["default"], (0, 0))
        self.rect = self.surf.get_rect()
        self.state = random.randrange(1,3)

        self.pos = vector2(
            ((self.this.config["panel_size"][0] / 2),
            (self.this.config["panel_size"][1] - 350) / 2 + 350)
        )

    def reset_surface(self):
        self.surf = pygame.Surface((350, 350), pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        self.surf.blit(self.this.sprites["sieve"]["default"], (0, 0))
        self.rect = self.surf.get_rect()

    def n_to_coin(self, c):
        c_spr = self.this.coin_set[0][0]
        if c == 1: c_spr = self.this.coin_set[0][0]
        elif c == 2: c_spr = self.this.coin_set[1][0]
        elif c == 3: c_spr = self.this.coin_set[2][0]
        elif c == 4: c_spr = self.this.coin_set[3][0]
        elif c == 5: c_spr = self.this.coin_set[4][0]
        elif c == 6: c_spr = self.this.coin_set[5][0]
        elif c == 7: c_spr = self.this.coin_set[0][1]
        elif c == 8: c_spr = self.this.coin_set[1][1]
        elif c == 9: c_spr = self.this.coin_set[2][1]
        elif c == 10: c_spr = self.this.coin_set[3][1]
        elif c == 11: c_spr = self.this.coin_set[4][1]
        elif c == 12: c_spr = self.this.coin_set[5][1]
        elif c == 13: c_spr = self.this.coin_set[0][2]
        elif c == 14: c_spr = self.this.coin_set[1][2]
        return c_spr

    def n_to_value(self, c):
        c_val = 1/8
        if c == 1: c_val = 1/8
        elif c == 2: c_val = 1/4
        elif c == 3: c_val = 1/2
        elif c == 4: c_val = 1
        elif c == 5: c_val = 3
        elif c == 6: c_val = 4
        elif c == 7: c_val = 6
        elif c == 8: c_val = 12
        elif c == 9: c_val = 24
        elif c == 10: c_val = 30
        elif c == 11: c_val = 48
        elif c == 12: c_val = 60
        elif c == 13: c_val = 120
        elif c == 14: c_val = 240
        return c_val

    def render_coin(self):
        for c in self.coins:
            c_spr = self.n_to_coin(c[0])
            self.surf.blit(c_spr, (c[1], c[2]))

    def jiggle(self):
        self.pos.x += random.randrange(-2, 3)
        if self.pos.x >= (640 / 2) + 10:
            self.pos.x -= 6 * self.this.framecoeff
        if self.pos.x <= (640 / 2) - 10:
            self.pos.x += 6 * self.this.framecoeff
        if self.n_of_coins >= 2:
            if random.randrange(1,45) == 1:
                self.this.coins_sound[random.randrange(0,5)].play()

    def coin_jiggle(self, x = 1):
        for c in self.coins:
            xm = random.randrange(-2,3)
            ym = random.randrange(1,4)
            if x: c[2] += ym
            if not x: c[2] -= ym
            c[1] += xm
            if c[1] > (268 - 38):
                c[1] -= xm * 2
            if c[1] < 78:
                c[1] += xm * (-2)
            if c[2] > (268 - 38):
                c[2] -= ym * 2
            if c[2] < 78:
                c[2] += ym * 2

    def update(self):
        if self.data["frame_dip"] <= 1:
            if self.this.keys[pygame.K_UP]:
                if self.pos.y > 330:
                    self.pos.y -= 6 * self.this.framecoeff
                    self.data["shakestate"] += 1
                    self.jiggle()
                    self.coin_jiggle()

            if self.this.keys[pygame.K_DOWN]:
                if self.pos.y < self.this.config["panel_size"][1] + 50 - 30:
                    self.pos.y += 6 * self.this.framecoeff
                    self.data["shakestate"] += 1
                    self.jiggle()
                    self.coin_jiggle(0)

            if self.this.keys[pygame.K_q]:
                if self.data["globalstate"] == 0:
                    self.this.sounds["coins_collect"].play()
                    for c in self.coins:
                        self.this.pence += self.n_to_value(c[0])
                    self.dip()
            if self.data["globalstate"] >= 1:
                if self.data["shakestate"] >= 20:
                    self.data["globalstate"] -= 1
                    self.data["shakestate"] = 0
                    self.state = random.randrange(1,3)
                    self.reset_surface()

                if self.data["globalstate"] >= 4:
                    self.reset_surface()
                    self.render_coin()
                    self.surf.blit(self.this.sprites["sieve"]["4-" + str(self.state)], (0, 0))

                if self.data["globalstate"] <= 3 and self.data["globalstate"] != 0:
                    self.reset_surface()
                    self.render_coin()
                    self.surf.blit(self.this.sprites["sieve"][str(self.data["globalstate"])], (0, 0))
            if self.data["globalstate"] == 0:
                self.reset_surface()
                self.render_coin()
        self.rect.midbottom = self.pos

    def dip(self, sound = True):
        n_of_coins = round(nrand.normal(loc=4, scale=3))
        if n_of_coins <= 1: n_of_coins = 1
        self.n_of_coins = n_of_coins
        self.coins = []
        self.data["frame_dip"] = 255

        for j in range(self.n_of_coins):
            j_value = nrand.normal(loc=1, scale=7)
            if j_value >= 10: j_value = nrand.normal(loc=1, scale=7)

            if j_value <= 0: j_value = 1
            if j_value >= 14: j_value = 14
            self.coins.append([round(j_value), random.randrange(86 - 30, 266 - 30), random.randrange(86 - 30, 266 - 30)])

        self.data["globalstate"] = random.randrange(3, 10) * 2
        self.reset_surface()
        state = random.randrange(1,3)
        self.reset_surface()
        self.surf.blit(self.this.sprites["sieve"]["4-" + str(state)], (0, 0))
        if sound: self.this.sounds["water_collect"].play()

    def frame(self):
        op = self.data["frame_dip"]
        if op >= 1:
            self.overlay = self.this.sprites["sewer_bg"].copy()
            self.overlay.fill((255, 255, 255, op), None, pygame.BLEND_RGBA_MULT)
            self.this.master.blit(self.overlay, (0, 0))
            self.data["frame_dip"] -= random.randrange(1,12) * self.this.framecoeff

class FadeLayer:
    def __init__(self, this):
        self.data = {
            "fade_efct" : 0
        }
        self.this = this

    def frame(self, dire = False, apf = 3):
        op = self.data["fade_efct"]
        # False: 0 --> 255
        # True: 255 --> 0

        if dire:
            if op <= 254:
                if op >= 255: op = 255
                self.data["fade_efct"] += apf * self.this.framecoeff
                self.this.master.fill((0, 0, 0, clamp(op, 0, 255)), None, pygame.BLEND_RGBA_MULT)
            if op >= 255:
                self.this.master.fill((0, 0, 0, clamp(op, 0, 255)), None, pygame.BLEND_RGBA_MULT)
                return True
        if not dire:
            if op >= 0:
                if op <= 0: op = 0
                self.data["fade_efct"] -= apf * self.this.framecoeff
                self.this.master.fill((0, 0, 0, clamp(op, 0, 255)), None, pygame.BLEND_RGBA_MULT)
            if op <= 0:
                self.this.master.fill((0, 0, 0, clamp(op, 0, 255)), None, pygame.BLEND_RGBA_MULT)
                return True
        return False

class Tosher:
    def __init__(self):
        self.setup()
        self.game()

    def setup(self):
        ### LOAD FILES
        with open("settings.cfg", "r") as configuration:
            self.config = json.load(configuration)

        self.sprites = {
            "icon" : pygame.image.load(os.path.join(self.config["sprite"]["icon"])),
            "sewer_bg" : pygame.image.load(os.path.join(self.config["sprite"]["sewer_bg"])),
            "sewer_bg_2" : pygame.image.load(os.path.join(self.config["sprite"]["sewer_bg_2"])),
            "comb" : pygame.image.load(os.path.join(self.config["sprite"]["comb"])),
            "sieve" : {
                "default" : pygame.image.load(os.path.join(self.config["sprite"]["sieve"]["default"])),
                "0" : pygame.image.load(os.path.join(self.config["sprite"]["sieve"]["0"])),
                "1" : pygame.image.load(os.path.join(self.config["sprite"]["sieve"]["1"])),
                "2" : pygame.image.load(os.path.join(self.config["sprite"]["sieve"]["2"])),
                "3" : pygame.image.load(os.path.join(self.config["sprite"]["sieve"]["3"])),
                "4-1" : pygame.image.load(os.path.join(self.config["sprite"]["sieve"]["4_1"])),
                "4-2" : pygame.image.load(os.path.join(self.config["sprite"]["sieve"]["4_2"])),
                "4-3" : pygame.image.load(os.path.join(self.config["sprite"]["sieve"]["4_3"]))
            },
            "gui" : {
                "play" : pygame.image.load(os.path.join(self.config["sprite"]["gui"]["play"])),
                "settings" : pygame.image.load(os.path.join(self.config["sprite"]["gui"]["settings"])),
                "exit" : pygame.image.load(os.path.join(self.config["sprite"]["gui"]["exit"])),
                "h_play" : pygame.image.load(os.path.join(self.config["sprite"]["gui"]["h_play"])),
                "h_settings" : pygame.image.load(os.path.join(self.config["sprite"]["gui"]["h_settings"])),
                "h_exit" : pygame.image.load(os.path.join(self.config["sprite"]["gui"]["h_exit"])),
                "bg" : pygame.image.load(os.path.join(self.config["sprite"]["gui"]["bg"]))
            },
            "map" : pygame.image.load(os.path.join(self.config["sprite"]["map"])),
            "black_fade" : pygame.image.load(os.path.join(self.config["sprite"]["black_fade"])),
            "line1" : pygame.image.load(os.path.join(self.config["sprite"]["line1"])),
            "line2" : pygame.image.load(os.path.join(self.config["sprite"]["line2"]))
        }
        self.type = {
            "regular12" : pygame.font.Font("type/LinLibertine_R.ttf", 12),
            "bold_italic12" : pygame.font.Font("type/LinLibertine_RBI.ttf", 12),
            "italic12" : pygame.font.Font("type/LinLibertine_RI.ttf", 12),
            "regular16" : pygame.font.Font("type/LinLibertine_RBI.ttf", 24),
            "regular24" : pygame.font.Font("type/LinLibertine_R.ttf", 24)
        }
        self.sounds = {
            "coins_clink" : pygame.mixer.Sound('sound/coins_clink.mp3'),
            "coins_clink2" : pygame.mixer.Sound('sound/coins_clink2.mp3'),
            "coins_clink3" : pygame.mixer.Sound('sound/coins_clink3.mp3'),
            "coins_clink4" : pygame.mixer.Sound('sound/coins_clink5.mp3'),
            "coins_clink5" : pygame.mixer.Sound('sound/coins_clink5.mp3'),
            "coins_collect" : pygame.mixer.Sound('sound/coins_collect.mp3'),
            "sewer_sounds" : pygame.mixer.Sound('sound/sewer_sounds.mp3'),
            "water_collect" : pygame.mixer.Sound('sound/water_collect.mp3'),
            "london_sound" : pygame.mixer.Sound('sound/london_sound.mp3'),
            "ladder_down" : pygame.mixer.Sound('sound/ladder_down.mp3'),
            "ui_click" : pygame.mixer.Sound('sound/ui_click.mp3')
        }
        self.volumes = [0.7, 0.1, 0.1, 0.35, 0.3, 0.3, 0.5]
        self.config_reset()
        self.coins_sound = [
            self.sounds["coins_clink"], self.sounds["coins_clink2"], self.sounds["coins_clink3"], self.sounds["coins_clink4"], self.sounds["coins_clink5"]
        ]

        ### SETUP
        pygame.display.set_caption("Dodger: A London Tosher")
        pygame.display.set_icon(self.sprites["icon"])

        ### VARIABLES
        self.root = pygame.display.set_mode(tuple(self.config["window_size"]))
        self.master = pygame.surface.Surface(tuple(self.config["panel_size"]), pygame.SRCALPHA)
        self.load_coins()
        self.sieve = Sieve(self)
        self.comb = Comb(self)
        self.fade = FadeLayer(self)
        self.clock = pygame.time.Clock()
        self.pence = 0
        self.gamestate = 0
        self.fade_goal = 0
        self.fade_from = 0
        self.fade_spd = 3
        self.cline = 0
        self.fps_log = [0, 0]
        self.maxFPS = FRAMERATES[self.config["maxFPS"]]
        self.framecoeff = 60 / self.maxFPS
        self.sieve.dip(sound = False)
        self.comb.reset(sound = False)

        ### SEWER SOUNDS
        self.sounds["sewer_sounds"].play(-1)
        self.sounds["london_sound"].play(-1)

        self.sounds["sewer_sounds"].set_volume(0)
        self.sounds["london_sound"].set_volume(0)

    def config_reset(self):
        self.sounds["london_sound"].set_volume(self.volumes[5] * self.config["volume"])
        self.sounds["sewer_sounds"].set_volume(self.volumes[0] * self.config["volume"])
        self.sounds["water_collect"].set_volume(self.volumes[1] * self.config["volume"])
        self.sounds["coins_clink"].set_volume(self.volumes[2] * self.config["volume"])
        self.sounds["coins_clink2"].set_volume(self.volumes[2] * self.config["volume"])
        self.sounds["coins_clink3"].set_volume(self.volumes[2] * self.config["volume"])
        self.sounds["coins_clink4"].set_volume(self.volumes[2] * self.config["volume"])
        self.sounds["coins_clink5"].set_volume(self.volumes[2] * self.config["volume"])
        self.sounds["coins_collect"].set_volume(self.volumes[3] * self.config["volume"])
        self.sounds["ladder_down"].set_volume(self.volumes[4] * self.config["volume"])
        self.sounds["ui_click"].set_volume(self.volumes[6] * self.config["volume"])

        with open('settings.cfg', 'w') as json_file:
            json.dump(self.config, json_file)
        self.maxFPS = FRAMERATES[self.config["maxFPS"]]
        self.framecoeff = 60 / self.maxFPS

    def game_gui(self):
        score_text = "Earnings. " + str(round(self.pence, 2)) + "p (£" + str(round(self.pence / 240, 2)) + ") (£" + str(round(self.pence * 1.64, 2))+ ")"
        score = self.type["italic12"].render(score_text, True, (255, 255, 255))
        self.master.blit(score, ((4, 4)))

        self.map_icon = Button((592, 0), (48, 48), self.coin_set[2][2], self.master, pos_scale = 2)
        self.map_icon.hover_obj = self.coin_set[3][2]
        self.map_icon.render()
        if self.map_icon.intercept(self.mouse): self.map_icon.render(hover = True)

    def load_coins(self):
        def load_tile_table(filename, tile_width, tile_height):
            tileset_image = pygame.image.load(filename)
            # tileset_image.set_colorkey((0, 0, 0))
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
        self.coin_set = load_tile_table(
            os.path.join("sprite/coins_texture.png"),
            48, 48
        )

    def map_gui(self):
        home_text = "Solomon's Apartment"
        home = self.type["regular12"].render(home_text, True, (255, 255, 0))
        home_s = self.type["regular12"].render(home_text, True, (0, 0, 0))
        museum_text = "Mayhew's"
        museum = self.type["regular12"].render(museum_text, True, (255, 255, 0))
        museum_s = self.type["regular12"].render(museum_text, True, (0, 0, 0))
        east_text = "Fish St."
        east = self.type["regular12"].render(east_text, True, (255, 255, 0))
        east_s = self.type["regular12"].render(east_text, True, (0, 0, 0))
        west_text = "Ruby Ln."
        west = self.type["regular12"].render(west_text, True, (255, 255, 0))
        west_s = self.type["regular12"].render(west_text, True, (0, 0, 0))
        # south_text = "The Borough"
        # south = self.type["regular12"].render(south_text, True, (255, 255, 0))
        # south_s = self.type["regular12"].render(south_text, True, (0, 0, 0))

        self.home_icon = Button((440, 158), (14, 14), self.coin_set[5][2], self.master, pos_scale = 2)
        self.home_icon.hover_obj = self.coin_set[1][3]
        self.museum_icon = Button((298, 124), (14, 14), self.coin_set[5][2], self.master, pos_scale = 2)
        self.museum_icon.hover_obj = self.coin_set[1][3]
        self.east_sewer_icon = Button((360, 141), (14, 14), self.coin_set[4][2], self.master, pos_scale = 2)
        self.east_sewer_icon.hover_obj = self.coin_set[0][3]
        # self.south_sewer_icon = Button((333, 205), (14, 14), self.coin_set[4][2], self.master, pos_scale = 2)
        # self.south_sewer_icon.hover_obj = self.coin_set[0][3]
        self.west_sewer_icon = Button((190, 119), (14, 14), self.coin_set[4][2], self.master, pos_scale = 2)
        self.west_sewer_icon.hover_obj = self.coin_set[0][3]

        self.home_icon.render()
        self.museum_icon.render()
        self.east_sewer_icon.render()
        # self.south_sewer_icon.render()
        self.west_sewer_icon.render()

        if self.home_icon.intercept(self.mouse):
            self.home_icon.render(hover = True)
            self.master.blit(home_s, (440+20-1, 158-1))
            self.master.blit(home, (440+20, 158))
        if self.museum_icon.intercept(self.mouse):
            self.museum_icon.render(hover = True)
            self.master.blit(museum_s, (298+20-1, 124-1))
            self.master.blit(museum, (298+20, 124))
        if self.east_sewer_icon.intercept(self.mouse):
            self.east_sewer_icon.render(hover = True)
            self.master.blit(east_s, (360+20-1, 141-1))
            self.master.blit(east, (360+20, 141))
        # if self.south_sewer_icon.intercept(self.mouse):
        #     self.south_sewer_icon.render(hover = True)
        #     self.master.blit(south_s, (333+20-1, 205-1))
        #     self.master.blit(south, (333+20, 205))
        if self.west_sewer_icon.intercept(self.mouse):
            self.west_sewer_icon.render(hover = True)
            self.master.blit(west_s, (190+20-1, 119-1))
            self.master.blit(west, (190+20, 119))

    def main_menu_gui(self):
        self.play = Button((0, 0), (640, 360), self.sprites["gui"]["play"], self.master, pos_scale = 2)
        self.play.hover_obj = self.sprites["gui"]["h_play"]
        self.play.overrides = [True, (434, 127), (90, 24)]
        self.settings = Button((0, 0), (640, 360), self.sprites["gui"]["settings"], self.master, pos_scale = 2)
        self.settings.hover_obj = self.sprites["gui"]["h_settings"]
        self.settings.overrides = [True, (434, 169), (90, 24)]
        self.exit = Button((0, 0), (640, 360), self.sprites["gui"]["exit"], self.master, pos_scale = 2)
        self.exit.hover_obj = self.sprites["gui"]["h_exit"]
        self.exit.overrides = [True, (434, 211), (90, 24)]

        self.play.render()
        self.settings.render()
        self.exit.render()

        if self.play.intercept(self.mouse):
            self.play.render(hover = True)
        if self.settings.intercept(self.mouse):
            self.settings.render(hover = True)
        if self.exit.intercept(self.mouse):
            self.exit.render(hover = True)

    def volume_gui(self):
        volume_text = "            Volume: " + str(round(100 * self.config["volume"], 1)) + "%"
        framerate_text = "            Max FPS: " + str(FRAMERATES[self.config["maxFPS"]])
        vol = self.type["regular24"].render(volume_text, True, (255, 255, 255))
        framerate = self.type["regular24"].render(framerate_text, True, (255, 255, 255))
        vol_p = self.type["regular24"].render("(+)", True, (254, 255, 255))
        vol_s = self.type["regular24"].render("(-)", True, (254, 255, 255))
        vol_ph = self.type["regular24"].render("(+)", True, (254, 167, 17))
        vol_sh = self.type["regular24"].render("(-)", True, (254, 167, 17))
        self.master.blit(vol, (45, (360 / 2) - (24 / 2) - 24))
        self.master.blit(vol_p, (45, (360 / 2) - (24 / 2) - 24))
        self.master.blit(vol_s, (297, (360 / 2) - (24 / 2) - 24))
        # framerates
        self.master.blit(framerate, (45, (360 / 2) - (24 / 2) + 24))
        self.master.blit(vol_p, (45, (360 / 2) - (24 / 2) + 24))
        self.master.blit(vol_s, (297, (360 / 2) - (24 / 2) + 24))

        exit_text = "← Back"
        ext = self.type["regular16"].render(exit_text, True, (255, 255, 255))
        ext_h = self.type["regular16"].render(exit_text, True, (254, 167, 17))
        self.master.blit(ext, (45, 360 - 32))

        if (45 + 96) * 2 >= self.mouse[0] >= 45 * 2:
            if (360) * 2 >= self.mouse[1] >= (360 - 48) * 2:
                self.master.blit(ext_h, (45, 360 - 32))
            if 336 - 24 + 48 >= self.mouse[1] >= 336 - 24:
                self.master.blit(vol_ph, (45, (360 / 2) - (24 / 2) - 24))
            if 336 + 64 + 48 >= self.mouse[1] >= 336 + 24:
                self.master.blit(vol_ph, (45, (360 / 2) - (24 / 2) + 24))

        if (297 - 45 + 96) * 2 >= self.mouse[0] >= (297 - 45) * 2:
            if 336 - 24 + 48 >= self.mouse[1] >= 336 - 24:
                self.master.blit(vol_sh, (297, (360 / 2) - (24 / 2) - 24))
            if 336 + 64 + 48 >= self.mouse[1] >= 336 + 24:
                self.master.blit(vol_sh, (297, (360 / 2) - (24 / 2) + 24))

    def game(self):
        # Preload
        self.mouse = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()
        self.map_gui()
        self.game_gui()

        while True:
            self.master.fill((0, 0, 0))
            if not self.config["disable_fps"]:
                self.fps_log[0] += self.clock.get_fps()
                self.fps_log[1] += 1

            ### EVENT LOOP
            self.mouse = pygame.mouse.get_pos()
            self.keys = pygame.key.get_pressed()
            if self.keys[pygame.K_r]:
                with open("frame.txt", "w") as frame_output:
                    frame_output.write("FPS Average: " + str(self.fps_log[0] / self.fps_log[1]) + "\nLog: " + str(self.fps_log[0]) + ", " + str(self.fps_log[1]))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.gamestate == 0:
                        if self.play.intercept(self.mouse):
                            self.sounds["ui_click"].play()
                            self.gamestate = 10
                            self.fade_from = 0
                            self.fade_goal = 3
                            self.fade_spd = 6
                        if self.settings.intercept(self.mouse):
                            self.sounds["ui_click"].play()
                            self.gamestate = 10
                            self.fade_from = 0
                            self.fade_goal = 4
                            self.fade_spd = 6
                        if self.exit.intercept(self.mouse):
                            self.sounds["ui_click"].play()
                            sys.exit()
                    if self.gamestate == 1:
                        if self.home_icon.intercept(self.mouse):
                            self.sounds["ui_click"].play()
                            self.gamestate = 10
                            self.fade_from = 1
                            self.fade_goal = 0
                            self.fade_spd = 3
                        if self.museum_icon.intercept(self.mouse):
                            self.sounds["ui_click"].play()
                            self.gamestate = 10
                            self.fade_from = 1
                            self.fade_goal = 3
                            self.fade_spd = 3
                        #if self.south_sewer_icon.intercept(self.mouse):
                        #    self.sounds["ui_click"].play()
                        #    self.gamestate = 10
                        #    self.fade_from = 1
                        #    self.fade_goal = 2
                        #    self.fade_spd = 3
                        if self.east_sewer_icon.intercept(self.mouse):
                            self.sounds["ui_click"].play()
                            self.gamestate = 10
                            self.fade_from = 1
                            self.fade_goal = 2
                            self.fade_spd = 3
                        if self.west_sewer_icon.intercept(self.mouse):
                            self.sounds["ui_click"].play()
                            self.gamestate = 10
                            self.fade_from = 1
                            self.fade_goal = 5
                            self.fade_spd = 3
                    if self.gamestate == 2:
                        if self.map_icon.intercept(self.mouse):
                            self.sounds["ui_click"].play()
                            self.gamestate = 10
                            self.fade_from = 2
                            self.fade_goal = 1
                            self.fade_spd = 3
                    if self.gamestate == 3:
                        if (640) * 2 >= self.mouse[0] >= (640 - (48 * 4)) * 2:
                            if (360) * 2 >= self.mouse[1] >= (360 - 48) * 2:
                                self.sounds["ui_click"].play()
                                self.cline = int(not bool(self.cline))
                                if self.cline == 0:
                                    self.gamestate = 10
                                    self.fade_from = 3
                                    self.fade_goal = 1
                                    self.fade_spd = 3
                    if self.gamestate == 4:
                        if (45 + 64) * 2 >= self.mouse[0] >= 45 * 2:
                            if (360) * 2 >= self.mouse[1] >= (360 - 48) * 2:
                                self.sounds["ui_click"].play()
                                self.gamestate = 10
                                self.fade_from = 3
                                self.fade_goal = 0
                                self.fade_spd = 6
                        if (297 - 45 + 96) * 2 >= self.mouse[0] >= (297 - 45) * 2:
                            if 336 - 24 + 48 >= self.mouse[1] >= 336 - 24:
                                if round(self.config["volume"], 2) >= 0.05:
                                    self.config["volume"] = round(round(self.config["volume"], 2) - 0.05, 2)
                                self.config_reset()
                                print("volume", str(self.config["volume"]))
                                self.sounds["ui_click"].play()
                            if 336 + 64 + 48 >= self.mouse[1] >= 336 + 24:
                                if self.config["maxFPS"] >= 1:
                                    self.config["maxFPS"] -= 1
                                self.config_reset()
                                self.sounds["ui_click"].play()

                        if (45 + 96) * 2 >= self.mouse[0] >= 45 * 2:
                            if 336 - 24 + 48 >= self.mouse[1] >= 336 - 24:
                                if round(self.config["volume"], 2) <= 0.95:
                                    self.config["volume"] = round(round(self.config["volume"], 2) + 0.05, 2)
                                self.config_reset()
                                print("volume", str(self.config["volume"]))
                                self.sounds["ui_click"].play()
                            if 336 + 64 + 48 >= self.mouse[1] >= 336 + 24:
                                if self.config["maxFPS"] <= 7:
                                    self.config["maxFPS"] += 1
                                self.config_reset()
                                self.sounds["ui_click"].play()


                        #[20, 24, 30, 45, 60, 72, 90, 92, 120]

                    if self.gamestate == 5:
                        if self.map_icon.intercept(self.mouse):
                            self.sounds["ui_click"].play()
                            self.gamestate = 10
                            self.fade_from = 5
                            self.fade_goal = 1
                            self.fade_spd = 3

            if self.gamestate == 0:
                self.sounds["sewer_sounds"].set_volume(0)
                self.sounds["london_sound"].set_volume(0)
                self.master.blit(self.sprites["gui"]["bg"], (0, 0))
                self.main_menu_gui()

            if self.gamestate == 1:
                self.sounds["sewer_sounds"].set_volume(0)
                self.sounds["london_sound"].set_volume(self.volumes[5] * self.config["volume"])
                self.master.blit(self.sprites["map"], (0, 0))
                self.map_gui()

            if self.gamestate == 2:
                self.sounds["sewer_sounds"].set_volume(self.volumes[0] * self.config["volume"])
                self.sounds["london_sound"].set_volume(0)
                self.master.blit(self.sprites["sewer_bg"], (0, 0))
                self.sieve.update()
                self.master.blit(self.sieve.surf, self.sieve.rect)
                self.sieve.frame()
                self.game_gui()

            if self.gamestate == 3:
                self.sounds["sewer_sounds"].set_volume(0)
                self.sounds["london_sound"].set_volume(0)
                self.master.blit(self.sprites["line" + str(self.cline + 1)], (0, 0))

            if self.gamestate == 4:
                self.sounds["sewer_sounds"].set_volume(0)
                self.sounds["london_sound"].set_volume(0)
                self.volume_gui()

            if self.gamestate == 5:
                self.sounds["sewer_sounds"].set_volume(self.volumes[0] * self.config["volume"])
                self.sounds["london_sound"].set_volume(0)
                self.master.blit(self.sprites["sewer_bg_2"], (0, 0))
                self.comb.update()
                self.master.blit(self.comb.surf, self.comb.rect)
                # self.comb.frame()
                self.game_gui()

            if self.gamestate == 10:
                if self.fade_goal == 2 or self.fade_goal == 1 and self.fade_from == 2 or self.fade_goal == 5 or self.fade_goal == 1 and self.fade_from == 5: self.sounds["ladder_down"].play()
                self.fade.data["fade_efct"] = 0
                self.gamestate = 9

            if self.gamestate == 9:
                if self.fade_goal == 3:
                    self.sounds["london_sound"].set_volume(0)
                    self.sounds["sewer_sounds"].set_volume(0)
                if self.fade_goal == 2: self.sounds["london_sound"].set_volume(0)
                if self.fade_goal == 5: self.sounds["london_sound"].set_volume(0)
                if self.fade_goal == 1: self.sounds["sewer_sounds"].set_volume(0)
                if self.fade.frame(True, self.fade_spd):
                    self.fade.data["fade_efct"] = 255
                    self.gamestate = 8

            if self.gamestate == 8:
                if self.fade_goal == 2:
                    self.sounds["sewer_sounds"].set_volume(self.volumes[0] * self.config["volume"])
                    self.master.blit(self.sprites["sewer_bg"], (0, 0))
                    self.master.blit(self.sieve.surf, self.sieve.rect)
                    self.game_gui()
                elif self.fade_goal == 1:
                    self.sounds["london_sound"].set_volume(self.volumes[5] * self.config["volume"])
                    self.master.blit(self.sprites["map"], (0, 0))
                    self.map_gui()
                elif self.fade_goal == 3:
                    self.master.blit(self.sprites["line" + str(self.cline + 1)], (0, 0))
                    self.fade_spd = 3
                elif self.fade_goal == 5:
                    self.sounds["sewer_sounds"].set_volume(self.volumes[0] * self.config["volume"])
                    self.master.blit(self.sprites["sewer_bg_2"], (0, 0))
                    self.master.blit(self.comb.surf, self.comb.rect)
                    self.game_gui()

                if self.fade.frame(False, self.fade_spd):
                    self.gamestate = self.fade_goal


            self.root.blit(pygame.transform.scale(self.master, tuple(self.config["window_size"])), (0, 0))
            pygame.display.flip()
            self.clock.tick(self.maxFPS)

if __name__ == "__main__":
    game = Tosher()
