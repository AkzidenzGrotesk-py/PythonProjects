import ConsoleEngine, random, time, os
global playerX, playerY, circlesize

l4 = ConsoleEngine.PIXEL_TYPE.PIXEL_SOLID
l3 = ConsoleEngine.PIXEL_TYPE.PIXEL_THREEQUARTERS
l2 = ConsoleEngine.PIXEL_TYPE.PIXEL_HALF
l1 = ConsoleEngine.PIXEL_TYPE.PIXEL_QUARTER


playersprite = [
    ["",l4,l4,""],
    [l4,l2,l1,l4],
    [l4,l1,l2,l4],
    ["",l4,l4,""]
]
game = ConsoleEngine.ConsoleGame()

playerX = 1
playerY = 1
circlesize = 14


@game.OnUserCreate
def setup(self):
    self.title = "Hello World! - FPS: %fps%"
    self.geometry = (100, 100)
    self.clear = True
    self.safeSizing = 10

@game.OnUserUpdate
def loop(self):
    global playerX, playerY, circlesize

    self.DrawBox((0,0), (99, 99), ConsoleEngine.PIXEL_TYPE.PIXEL_SOLID, thickness = 2)
    self.DrawSprite((playerX, playerY), playersprite)
    self.DrawTriangle((2, 2), (17, 29), (74, 67), l3, l2)
    self.DrawCircle((50, 50), circlesize, fill = l1)
    self.Pixel((6, 6), "Hello, world! This is the console engine!")


    if self.Keyboard('w') and playerY > 1: playerY -= 1
    if self.Keyboard('s') and playerY < self.geometry[1] - 1 - len(playersprite): playerY += 1
    if self.Keyboard('a') and playerX > 1: playerX -= 1
    if self.Keyboard('d') and playerX < self.geometry[0] - 1 - len(playersprite[0]): playerX += 1
    if self.Keyboard('t'): circlesize += 1
    if self.Keyboard('y'): circlesize -= 1
    if self.Keyboard('x'): self.active = False
