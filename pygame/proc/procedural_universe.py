from lemire import dlRandom
import pygameUtils as pyg
from pygameUtils import vec2d
import pygame, sys, timeit

WHITE = (255, 255, 255)
BLACK = (0  , 0  , 0  )

STARCOLOURS = [
	(255, 255, 255), (255, 192, 203), (50, 255, 50), (50, 50, 255),
	(255, 255, 50), (50, 255, 255), (75, 75, 75), (255, 255, 200)
]

class Planet:
	def __init__(self):
		self.distance = 0.0
		self.diameter = 0.0
		self.foliage = 0.0
		self.minerals = 0.0
		self.water = 0.0
		self.gases = 0.0
		self.temperature = 0.0
		self.population = 0.0
		self.ring = False
		self.moons = []

class StarSystem:
	def __init__(self, x, y, generateFullSystem = False):
		self.x = x
		self.y = y
		self.nWyuno = (x & 0xFFFF) << 16 | (y & 0xFFFF)
		if self.nWyuno == 0: self.nWyuno = 1
		self.rb = dlRandom(self.nWyuno)
		self.planets = []

		self.starExists = (self.rb.wyuno_range(0, 20) == 1)
		if self.starExists:

			self.starDiameter = self.rb.wyuno_range(100, 800) / 10
			self.starColour = STARCOLOURS[self.rb.wyuno_range(0, 8)]

			if generateFullSystem:
				distanceFromStar = self.rb.wyuno_range(600, 2000) / 10
				nPlanets = self.rb.wyuno_range(0, 10)
				for i in range(nPlanets):
					p = Planet()
					p.distance = distanceFromStar
					distanceFromStar += self.rb.wyuno_range(200, 2000) / 10
					p.diameter = self.rb.wyuno_range(40, 200) / 10
					p.temperature = self.rb.wyuno_range(-2000, 3000) / 10
					p.foliage = self.rb.wyuno_range(1, 10000) / 10000
					p.minerals = self.rb.wyuno_range(1, 10000) / 10000
					p.gases = self.rb.wyuno_range(1, 10000) / 10000
					p.water = self.rb.wyuno_range(1, 10000) / 10000
					dSum = 1 / (p.foliage + p.minerals + p.gases + p.water)
					p.foliage *= dSum;p.minerals *= dSum;p.gases *= dSum;p.water *= dSum;

					p.population = max(self.rb.wyuno_range(-5000000, 20000000), 0)
					p.ring = self.rb.wyuno_range(0, 10) == 1

					moons = max(self.rb.wyuno_range(-5, 5), 0)
					for j in range(moons):
						p.moons.append(self.rb.wyuno_range(10, 50) / 10)

					self.planets.append(p)




class Universe:
	def __init__(self):
		pygame.init()
		self.config()
		self.ready()

	def config(self):
		self.cell = 16
		self.size = (self.cell * 40, self.cell * 40)
		self.title = "Procedural Universe - FPS: %fps%"
		self.root = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
		self.master = pygame.Surface(self.root.get_size())
		self.active = True
		self.fps = 0
		self.galaxyOffset = vec2d()
		self.starSelected = False
		self.whichStarSelected = vec2d()

		self.rb = dlRandom()
		self.deltatime = pyg.deltatime(self, True)
		self.arial24 = pygame.font.SysFont('Arial Black', 24)

		pygame.display.set_caption(self.title)

	def loop_header(self):
		# Deltatime, keys and mouse pos
		self.deltatime = pyg.deltatime(self)
		self.keys = pygame.key.get_pressed()
		self.mouse = pygame.mouse.get_pos()
		self.mousep = pygame.mouse.get_pressed()

		# FPS
		if self.deltatime != 0:
			self.fps = round(1/self.deltatime, 2)
			pygame.display.set_caption(self.title.replace("%fps%", str(self.fps)))

	def ready(self):
		while self.active:
			self.loop_header()

			# Events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.active = False

			# Controls
			init_speed = 50
			speed = init_speed
			if self.keys[pygame.K_LCTRL]: speed *= 3
			if self.keys[pygame.K_w]: self.galaxyOffset.y -= speed * self.deltatime
			if self.keys[pygame.K_s]: self.galaxyOffset.y += speed * self.deltatime
			if self.keys[pygame.K_a]: self.galaxyOffset.x -= speed * self.deltatime
			if self.keys[pygame.K_d]: self.galaxyOffset.x += speed * self.deltatime

			speed = init_speed

			if self.keys[pygame.K_q]:
				x_input, y_input = 0, 0
				x_input = round(float(input("x ")), 2)
				y_input = round(float(input("y ")), 2)
				self.galaxyOffset = vec2d(x_input, y_input)


			# Clear
			self.root.fill((0, 0, 0))
			self.master.fill((0, 0, 0))

			# Stars

			# Mouse
			sMouse = vec2d(self.mouse[0] / self.cell, self.mouse[1] / self.cell)
			galaxy_mouse = sMouse + self.galaxyOffset

			# Galaxy
			sectorsX = round(self.size[0] / self.cell)
			sectorsY = round(self.size[1] / self.cell)

			# Do stuff
			for x in range(int(self.size[0] / 8)):
				for y in range(int(self.size[1] / 8)):
					nSeed = y + sectorsY + int(self.galaxyOffset.y) << 16 | x + sectorsX + int(self.galaxyOffset.x)
					self.rb.__seed__(nSeed)
					if self.rb.wyuno_range(1, 256) < 32:
						self.master.set_at((x * 8, y * 8), (100, 100, 100))

			screen_sector = vec2d()
			for screen_sector.x in range(sectorsX):
				for screen_sector.y in range(sectorsY):
					star = StarSystem(screen_sector.x + int(self.galaxyOffset.x),
						screen_sector.y + int(self.galaxyOffset.y))

					if star.starExists:
						pygame.draw.circle(
							self.master,
							star.starColour,
							(screen_sector.x * self.cell + self.cell / 2, screen_sector.y * self.cell + self.cell / 2),
							star.starDiameter / 8,
							width = 0
						)

						if int(sMouse.x) == screen_sector.x and int(sMouse.y) == screen_sector.y:
							color = (255, 0, 0)
							if self.mousep[0]: color = (255, 255, 255)
							pygame.draw.circle(
								self.master,
								color,
								(screen_sector.x * self.cell + self.cell / 2, screen_sector.y * self.cell + self.cell / 2),
								12,
								width = 2
							)

			if self.mousep[0]:
				star = StarSystem(int(galaxy_mouse.x), int(galaxy_mouse.y))

				if star.starExists:
					self.starSelected = True
					self.whichStarSelected = galaxy_mouse

				else:
					self.starSelected = False


			if self.starSelected:
				star = StarSystem(int(self.whichStarSelected.x), int(self.whichStarSelected.y), True)

				pygame.draw.rect(self.master, (0, 0, 71), 	(8, self.size[1] - 232 - 8, self.size[0] - 8, 232), width=0)
				pygame.draw.rect(self.master, WHITE, 		(8, self.size[1] - 232 - 8, self.size[0] - 8, 232), width=1)

				vBody = vec2d(14, self.size[1] - 232 - 8 + (356 - 240))
				vBody.x += star.starDiameter * 1.375
				pygame.draw.circle(self.master,
					star.starColour,
					(vBody.x, vBody.y),
					star.starDiameter * 1.375,
					width = 0
				)
				vBody.x += star.starDiameter * 1.375 + 8

				for planet in star.planets:
					if (vBody.x + planet.diameter >= 496): break

					vBody.x += planet.diameter
					pygame.draw.circle(self.master,
						(255, 15, 15),
						(vBody.x, vBody.y),
						planet.diameter * 1.0,
						width = 0
					)

					vMoon = vec2d(vBody.x, vBody.y)
					vMoon.y += planet.diameter + 10

					for moon in planet.moons:
						vMoon.y += moon
						pygame.draw.circle(self.master,
							(150, 150, 150),
							(vMoon.x, vMoon.y),
							moon * 1.0,
							width = 0
						)
						vMoon.y += moon + 10

					vBody.x += planet.diameter + 8

			coordRender = self.arial24.render(f"({round(self.galaxyOffset.x, 2)}, {round(self.galaxyOffset.y, 2)})", True, (255, 0, 0))
			self.master.blit(coordRender, (4, 0))

			# Render
			self.root.blit(self.master, (0, 0))
			pygame.display.flip()


		sys.exit()

if __name__ == "__main__":
	master = Universe()
