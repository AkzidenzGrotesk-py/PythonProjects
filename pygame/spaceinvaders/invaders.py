import pygame, sys, os, random, math
pygame.init()

# CONFIGURATION

WIDTH   = 256   # Playfield width
HEIGHT  = 256   # Playfield height
WINWIDTH= 768   # Window width
WINHEIGH= 768   # Window height
FPS     = 60    # Max framerate / gamespeed
ATK_F   = 30    # Every X frames, an attack is shot if the atk button is held
DIF     = 25     # Decrease to increase bullethell
E_ATK_F = 60 * DIF# Every X frames, an attack is shot by the enemy
MOV_F   = 0.03  # Enemy moves down per frame
WORTH1  = 20    # Score from killing enemy
WORTH2  = 30    # Score from killing enemy
WORTH3  = 40    # Score from killing enemy
BULLETS = 3     # Bullet speed
DODGE   = 0.05  # Enemy strafe move speed
PLATHP  = 5     # Platform health

# Controls
MOVE_L  = pygame.K_LEFT
MOVE_R  = pygame.K_RIGHT
ATK     = pygame.K_z

###############
# GLOBAL

vector2 = pygame.math.Vector2
mainfont = pygame.font.Font("sprite/dogica.ttf", 8)
boldfont = pygame.font.Font("sprite/dogicabold.ttf", 8)

###############

########### BULLET
class Bullet(pygame.sprite.Sprite):
    def __init__(self, this, owner = 0, loc = (0, 0)):
        super().__init__()
        self.this = this
        self.owner = owner

        if owner == 0:
            self.surf = pygame.Surface((2, 2))
            self.surf.blit(this.sprites["bullet"], (-7, -7))
        if owner == 1:
            self.surf = pygame.Surface((4, 5))
            self.surf.blit(this.sprites["invader_bullet"], (-6, -6))
        self.rect = self.surf.get_rect()

        self.pos = vector2(loc)

    def move(self):
        if self.owner == 0:
            self.pos.y -= BULLETS
            if self.pos.y < 0: self.kill()
        if self.owner == 1:
            self.pos.y += BULLETS
            if self.pos.y > HEIGHT: self.kill()

        self.rect.midbottom = self.pos

    def update(self):
        if self.owner == 0:
            hits = pygame.sprite.spritecollide(self, self.this.enemy_group, False)
            phits = pygame.sprite.spritecollide(self, self.this.platform_group, False)
            for entity in hits:
                if entity.type == 1: self.this.score += WORTH3
                if entity.type == 2: self.this.score += WORTH2
                if entity.type == 3: self.this.score += WORTH1
                entity.death = True
                self.kill()
            for entity in phits:
                self.kill()
        if self.owner == 1:
            hits = pygame.sprite.spritecollide(self, self.this.player_group, False)
            phits = pygame.sprite.spritecollide(self, self.this.platform_group, False)
            for entity in hits:
                self.this.level = 3
                entity.kill()
                self.kill()
            for entity in phits:
                entity.health -= 1
                self.kill()

########### INVADER
class Invader(pygame.sprite.Sprite):
    def __init__(self, this, setpos = (16, 16), type = 1):
        super().__init__()
        self.this = this
        self.type = type
        self.death = False
        self.initial_pos = vector2(setpos)

        self.surf = pygame.Surface((16, 16))
        self.surf.blit(this.sprites["invader"][f"{self.type}-0"], (0, 0))
        self.rect = self.surf.get_rect()
        self.atk_counter = random.randint(0, E_ATK_F)
        self.frame_sprite = 60
        self.death_sprite = 20
        self.frame = False
        self.deviation = 0
        self.d_dir = 1

        self.pos = vector2(setpos)

    def move(self):
        if self.d_dir == 1: self.deviation += DODGE
        if self.d_dir == -1: self.deviation -= DODGE

        self.pos.x = self.initial_pos.x + self.deviation

        if self.deviation >= 16 or self.deviation <= -16:
            self.d_dir = -self.d_dir

        self.pos.y += MOV_F
        self.rect.midbottom = self.pos

    def update(self):
        if self.atk_counter <= 0:
            self.this.bullet_group.add(Bullet(self.this, owner = 1,  loc = (self.pos.x, self.pos.y + 16)))
            self.atk_counter = E_ATK_F
        else:
            self.atk_counter -= 1

        if self.frame_sprite <= 0:
            self.surf.fill((0, 0, 0))
            self.surf.blit(self.this.sprites["invader"][f"{self.type}-{int(self.frame)}"], (0, 0))
            self.frame = not self.frame
            self.frame_sprite = 30
        else:
            self.frame_sprite -= 1

        if self.death:
            if self.death_sprite <= 0:
                self.kill()
            if self.death_sprite <= 10:
                self.surf.fill((0, 0, 0))
                self.surf.blit(self.this.sprites["explode"], (0, 0))

            self.death_sprite -= 1

########### PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self, this):
        super().__init__()
        self.this = this

        self.surf = pygame.Surface((16, 16))
        self.surf.blit(this.sprites["player"], (0, 0))
        self.rect = self.surf.get_rect()

        self.pos = vector2((16, HEIGHT - 16))

    def move(self):
        if self.this.keys[MOVE_L]:
            self.pos.x -= 3
        if self.this.keys[MOVE_R]:
            self.pos.x += 3

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos

    def update(self):
        if self.this.keys[ATK]:
            if self.this.attack_counter <= 0:
                self.this.bullet_group.add(Bullet(self.this, loc = (self.pos.x, self.pos.y - 16)))
                self.this.attack_counter = ATK_F
            else:
                self.this.attack_counter -= 1

        if self.this.keys[pygame.K_x]: print(self.this.score)

########### PLATFORM
class Platform(pygame.sprite.Sprite):
    def __init__(self, this, size = 1, setpos = (0, 0)):
        super().__init__()
        self.this = this
        self.size = size
        self.health = PLATHP

        if self.size == 1:
            self.surf = pygame.Surface((16, 16))
            self.surf.blit(this.sprites["wall"]["small5"], (0, 0))
        elif self.size == 2:
            self.surf = pygame.Surface((32, 16))
            self.surf.blit(this.sprites["wall"]["large5"], (0, 0))

        self.rect = self.surf.get_rect(center = setpos)

    def update(self):
        if self.health <= 0:
            self.kill()
        elif self.size == 1:
            self.surf.fill((0, 0, 0))
            self.surf.blit(self.this.sprites["wall"][f"small{str(self.health)}"], (0, 0))
        elif self.size == 2:
            self.surf.fill((0, 0, 0))
            self.surf.blit(self.this.sprites["wall"][f"large{str(self.health)}"], (0, 0))

    def move(self):
        pass



class SpaceInvaders:
    def __init__(self):
        # VARIABLES
        self.master = pygame.display.set_mode((WINWIDTH, WINHEIGH))
        self.scale_master = pygame.surface.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.window_icon = pygame.image.load(os.path.join("invader_icon.png"))
        self.sprites = {
            "bullet" : pygame.image.load(os.path.join("sprite/bullet.png")),
            "invader_bullet" : pygame.image.load(os.path.join("sprite/invader_bullet.png")),
            "player" : pygame.image.load(os.path.join("sprite/player.png")),
            "explode" : pygame.image.load(os.path.join("sprite/explode.png")),
            "invader" : {
                "1-0" : pygame.image.load(os.path.join("sprite/invader_1_0.png")),
                "1-1" : pygame.image.load(os.path.join("sprite/invader_1_1.png")),
                "2-0" : pygame.image.load(os.path.join("sprite/invader_2_0.png")),
                "2-1" : pygame.image.load(os.path.join("sprite/invader_2_1.png")),
                "3-0" : pygame.image.load(os.path.join("sprite/invader_3_0.png")),
                "3-1" : pygame.image.load(os.path.join("sprite/invader_3_1.png"))
            },
            "wall" : {
                "small5" : pygame.image.load(os.path.join("sprite/wall_small_5.png")),
                "small4" : pygame.image.load(os.path.join("sprite/wall_small_4.png")),
                "small3" : pygame.image.load(os.path.join("sprite/wall_small_3.png")),
                "small2" : pygame.image.load(os.path.join("sprite/wall_small_2.png")),
                "small1" : pygame.image.load(os.path.join("sprite/wall_small_1.png")),
                "large5" : pygame.image.load(os.path.join("sprite/wall_large_5.png")),
                "large4" : pygame.image.load(os.path.join("sprite/wall_large_4.png")),
                "large3" : pygame.image.load(os.path.join("sprite/wall_large_3.png")),
                "large2" : pygame.image.load(os.path.join("sprite/wall_large_2.png")),
                "large1" : pygame.image.load(os.path.join("sprite/wall_large_1.png"))
            }
        }

        # WINDOW
        pygame.display.set_caption("Space Invaders")
        pygame.display.set_icon(self.window_icon)

        # SETUP
        self.player = Player(self)
        self.attack_counter = 0
        self.score = 0
        self.level = 1

        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.total_sprites = [
            self.player_group,
            self.enemy_group,
            self.bullet_group,
            self.platform_group
        ]

        # self.generate_level()
        self.mainloop()

    def generate_level(self):
        if self.level == 4:
            v = 1
            for k in range(1, 14):
                for l in range(1, 4):
                    self.enemy_group.add(Invader(self, setpos = ((k + 1) * 16, (l + 4) * 16), type = l))

            self.platform_group.add(Platform(self, setpos = (32, HEIGHT - 48)))
            self.platform_group.add(Platform(self, setpos = (WIDTH - 32, HEIGHT - 48)))
            self.platform_group.add(Platform(self, size = 2, setpos = (WIDTH / 2 - 32, HEIGHT - 48)))
            self.platform_group.add(Platform(self, size = 2, setpos = (WIDTH / 2 + 32, HEIGHT - 48)))
        if self.level == 5: self.level = 1

    def update_level(self):
        if not len(self.enemy_group) and len(self.player_group) and self.level >= 4:
            self.level += 1
            self.player_group = pygame.sprite.Group()
            self.player_group.add(self.player)
            self.enemy_group = pygame.sprite.Group()
            self.bullet_group = pygame.sprite.Group()
            self.platform_group = pygame.sprite.Group()
            self.total_sprites = [
                self.player_group,
                self.enemy_group,
                self.bullet_group,
                self.platform_group
            ]
            self.generate_level()

        score = mainfont.render(f"SCORE {self.score}", True, (255, 255, 255))
        if self.level >= 4: self.scale_master.blit(score, (8, 8))

        if self.level == 1:
            titletext = "SPACE INVADERS"
            authortext = "Clone by AkzidenzGrotesk"
            moretext = "press p for more"
            pressstarttext = "PRESS SPACE"

            title = boldfont.render(titletext, True, (255, 255, 255))
            author = mainfont.render(authortext, True, (255, 255, 255))
            pressstart = boldfont.render(pressstarttext, True, (255, 255, 255))
            more = mainfont.render(moretext, True, (255, 255, 255))

            self.scale_master.blit(self.sprites["invader"]["1-0"], (WIDTH / 2 - 8, HEIGHT / 2 - 80))
            self.scale_master.blit(title, ((WIDTH / 2) - (len(titletext) / 2 * 8), HEIGHT / 2 - 48))
            self.scale_master.blit(author, ((WIDTH / 2) - (len(authortext) / 2 * 8), HEIGHT / 2 - 32))
            self.scale_master.blit(more, ((WIDTH / 2) - (len(moretext) / 2 * 8), HEIGHT / 2 + 112))
            self.scale_master.blit(pressstart, ((WIDTH / 2) - (len(pressstarttext) / 2 * 8), HEIGHT / 2 + 64))

            if self.keys[pygame.K_SPACE]:
                self.score = 0
                self.level = 4
                self.player_group = pygame.sprite.Group()
                self.player_group.add(self.player)
                self.enemy_group = pygame.sprite.Group()
                self.bullet_group = pygame.sprite.Group()
                self.platform_group = pygame.sprite.Group()
                self.total_sprites = [
                    self.player_group,
                    self.enemy_group,
                    self.bullet_group,
                    self.platform_group
                ]
                self.generate_level()
            if self.keys[pygame.K_p]: self.level = 2
        if self.level == 2:
            titletext = "SPACE INVADERS"
            controlstext = "Z - Attack"
            controls2text = "ARROWS - Move"
            returntext = "PRESS Q"

            title = boldfont.render(titletext, True, (255, 255, 255))
            controls = mainfont.render(controlstext, True, (255, 255, 255))
            controls2 = mainfont.render(controls2text, True, (255, 255, 255))
            return_ = boldfont.render(returntext, True, (255, 255, 255))

            self.scale_master.blit(title, ((WIDTH / 2) - (len(titletext) / 2 * 8), HEIGHT / 2 - 112))
            self.scale_master.blit(controls, ((WIDTH / 2) - (len(controlstext) / 2 * 8), HEIGHT / 2 - 80))
            self.scale_master.blit(controls2, ((WIDTH / 2) - (len(controls2text) / 2 * 8), HEIGHT / 2 - 64))
            self.scale_master.blit(return_, ((WIDTH / 2) - (len(returntext) / 2 * 8), HEIGHT / 2 + 112))

            if self.keys[pygame.K_q]: self.level = 1

        if self.level == 3:
            titletext = "SPACE INVADERS"
            gameovertext = "GAME OVER"
            scoretext = f"SCORE {self.score}"
            pressreturntext = "PRESS Q"

            title = mainfont.render(titletext, True, (255, 255, 255))
            gameover = boldfont.render(gameovertext, True, (255, 255, 255))
            score = mainfont.render(scoretext, True, (255, 255, 255))
            pressreturn = mainfont.render(pressreturntext, True, (255, 255, 255))

            self.scale_master.blit(title, ((WIDTH / 2) - (len(titletext) / 2 * 8), HEIGHT / 2 - 112))
            self.scale_master.blit(gameover, ((WIDTH / 2) - (len(gameovertext) / 2 * 8), HEIGHT / 2 - 16))
            self.scale_master.blit(score, ((WIDTH / 2) - (len(scoretext) / 2 * 8), HEIGHT / 2))
            self.scale_master.blit(pressreturn, ((WIDTH / 2) - (len(pressreturntext) / 2 * 8), HEIGHT / 2 + 112))

            if self.keys[pygame.K_q]: self.level = 1

    def mainloop(self):
        while True:
            self.scale_master.fill((0, 0, 0))

            self.keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.level >= 4:
                for group in self.total_sprites:
                    for entity in group:
                        self.scale_master.blit(entity.surf, entity.rect)
                        entity.move()
                        entity.update()

            self.update_level()
            self.master.blit(pygame.transform.scale(self.scale_master, (WINWIDTH, WINHEIGH)), (0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SpaceInvaders()
