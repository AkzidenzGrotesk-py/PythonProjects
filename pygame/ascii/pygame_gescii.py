import gescii, os, random, pygame

tileset_cfg = gescii.TileSetConfig("DWARF_FORTRESS")
master = gescii.ASCIIPanel(64, 32, "GESCII Test Window", "8x8_pixel_tileset_transparent.png", 16, 16, tileset_cfg)
active = False

grass_texture = {
    "chars" : [
        ".;\',", ",,.,", "\"..,", ".,,;"
    ],
    "color" : [
        "GGGG", "GGGG", "GGGG", "GGGG"
    ],
    "colormap" : {"G" : (0, 255, 0)}
}

tree_rand = [(random.randint(0, master.windowWidth), random.randint(0, master.windowHeight)) for k in range(15, 30)]

master.deltatime(True)
while not active:
    deltatime = master.deltatime()
    master.check_exit()
    master.clear()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.Z:
                tree_rand = [(random.randint(0, master.windowWidth), random.randint(0, master.windowHeight)) for k in range(15, 30)]

    for i in range(int(master.windowWidth / len(grass_texture['chars'][0]))):
        for j in range(int(master.windowHeight / len(grass_texture['chars']))):
            master.texture(i * 4, j * 4, grass_texture)
    
    for t in tree_rand:
        master.char(t[0], t[1], "$|#|", (0, 0, 0))
        master.char(t[0], t[1], "0", (139,69,19))

    fps_debug = master.fps(deltatime, (255, 255, 255))
    master.on_debug(16, 8, fps_debug)
    master.update()
    # os.system("pause")