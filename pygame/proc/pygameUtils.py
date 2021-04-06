import time

def deltatime(gameclass, setup = False):
    if setup:
        gameclass.tp1 = time.monotonic()
        gameclass.tp2 = time.monotonic()
        return 1
    else:
        gameclass.tp2 = time.monotonic()
        elapsedTime = gameclass.tp2 - gameclass.tp1
        gameclass.tp1 = gameclass.tp2
        return elapsedTime

class vec2d:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def __add__(self, e):
		x = self.x + e.x
		y = self.y + e.y
		return vec2d(x, y)
