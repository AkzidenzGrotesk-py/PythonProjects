import pygame, pygao, math, json, sys, time
from pygao import triangle, vec3d, mat4x4
from numba import jit
pygame.init()

# TO DO LIST
# - Implement time.monotonic()
# - Follow javidx9 tutorial to finish
# - Camera, rendering pipeline, etc.

# Item to load
cubeMesh = [
    # SOUTH
    [[0.0, 0.0, 0.0],   [0.0, 1.0, 0.0],    [1.0, 1.0, 0.0]],
    [[0.0, 0.0, 0.0],   [1.0, 1.0, 0.0],    [1.0, 0.0, 0.0]],
    # EAST
    [[1.0, 0.0, 0.0],   [1.0, 1.0, 0.0],    [1.0, 1.0, 1.0]],
    [[1.0, 0.0, 0.0],   [1.0, 1.0, 1.0],    [1.0, 0.0, 1.0]],
    # NORTH
    [[1.0, 0.0, 1.0],   [1.0, 1.0, 1.0],    [0.0, 1.0, 1.0]],
    [[1.0, 0.0, 1.0],   [0.0, 1.0, 1.0],    [0.0, 0.0, 1.0]],
    # WEST
    [[0.0, 0.0, 1.0],   [0.0, 1.0, 1.0],    [0.0, 1.0, 0.0]],
    [[0.0, 0.0, 1.0],   [0.0, 1.0, 0.0],    [0.0, 0.0, 0.0]],
    # TOP
    [[0.0, 1.0, 0.0],   [0.0, 1.0, 1.0],    [1.0, 1.0, 1.0]],
    [[0.0, 1.0, 0.0],   [1.0, 1.0, 1.0],    [1.0, 1.0, 0.0]],
    # BOTTOM
    [[1.0, 0.0, 1.0],   [0.0, 0.0, 1.0],    [0.0, 0.0, 0.0]],
    [[1.0, 0.0, 1.0],   [0.0, 0.0, 0.0],    [1.0, 0.0, 0.0]]
]
loadme = cubeMesh

class GraphicsEngine:
    #### OUT OF LOOP
    def __init__(self):
        self.config()
        self.matrices()
        self.loop()

    # Configurate main variables and setup
    def config(self):
        # Load CONFIG.JSON
        with open("assets/config.json") as cfile:
            self.cfg = json.load(cfile)

        # Load .obj file
        self.models = []
        self.blockcoord = self.cfg["modelData"]["preloadedb"]
        self.blockfloorcoord = []

        # Generate "floor" from CFG size
        for j in range(self.cfg["floor"][0], self.cfg["floor"][2]):
            for t in range(self.cfg["floor"][0], self.cfg["floor"][2]):
                self.blockfloorcoord.append([j, self.cfg["floor"][1], t])

        # Load models in CFG
        for k, file in enumerate(self.cfg["modelData"]["file"]):
            self.models.append([tuple(self.cfg["modelData"]["offsets"][k]), tuple(self.cfg["modelData"]["rotations"][k]), pygao.LoadFromObjectFile(file)])

        # Load boxes from saved state
        for p in self.blockcoord:
            loc = (round(p[0]), round(p[1]), round(p[2]))
            self.models.append([
                loc,
                (0, 0, 0),
                pygao.LoadFromObjectFile("assets/box.obj")
            ])
        for p in self.blockfloorcoord:
            loc = (round(p[0]), round(p[1]), round(p[2]))
            self.models.append([
                loc,
                (0, 0, 0),
                pygao.LoadFromObjectFile("assets/box.obj")
            ])

        # Manage class:global variables
        self.root = pygame.display.set_mode(tuple(self.cfg["size"]), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.master = pygame.Surface(self.root.get_size())
        self.icon_image = pygame.image.load(self.cfg["icon"])
        self.active = True
        self.fps = 0
        # Camera
        self.vCamera = vec3d()
        self.vLookDir = vec3d()
        self.fYaw = 0
        self.fPitch = 0
        self.matProj = pygao.Matrix_MakeProjection(90, self.cfg["size"][1] / self.cfg["size"][0], 0.1, 1000)
        self.light_direction = vec3d(0.0, 1.0, 0.0)
        # Deltatime
        self.tp1 = time.monotonic()
        self.tp2 = time.monotonic()
        self.fTheta = 0
        self.vTargetOffsetY = 0


        # Configurate window
        pygame.display.set_icon(self.icon_image)
        pygame.display.set_caption(self.cfg["title"])
        pygame.mouse.set_visible(False)

    # Initialize matrices
    def matrices(self):
        # Camera stuff
        self.vUp = vec3d(0, 1, 0)
        self.vTarget = vec3d(0,0 + self.vTargetOffsetY,1)
        self.matCameraRotY = pygao.Matrix_MakeRotationY(self.fYaw)
        self.vLookDirY = pygao.Matrix_MultiplyVector(self.matCameraRotY, self.vTarget)
        self.vTarget = pygao.Vector_Add(self.vCamera, self.vLookDirY)

        # Update camera for rotation /// and initialize
        self.matCamera = pygao.Matrix_PointAt(self.vCamera, self.vTarget, self.vUp)
        self.matView = pygao.Matrix_QuickInverse(self.matCamera)

    # Cleanup and close program
    def cleanup(self):
        sys.exit()

    #### IN LOOP
    # Handle window events
    def events(self, event):
        if event.type == pygame.QUIT:
            self.active = False


    # Key events
    def key_events(self):
        mouse = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()
        nmx, nmy = mouse
        size = self.cfg["size"]
        lock_value = 3
        nr_mouse = False

        if self.keys[pygao.ltk(self.cfg["controls"]["quit"])]:
            self.active = False

        if self.keys[pygao.ltk(self.cfg["controls"]["up"])]:
            self.vCamera.y += 8 * self.fElapsedTime

        if self.keys[pygao.ltk(self.cfg["controls"]["down"])]:
            self.vCamera.y -= 8 * self.fElapsedTime


        basespeed = 8.0
        speed = basespeed * 2 if self.keys[pygao.ltk(self.cfg["controls"]["sprint"])] else basespeed
        vForward = pygao.Vector_Mul(self.vLookDirY, speed * self.fElapsedTime)
        rLeft = 90 * math.pi / 180
        vLeft = pygao.Vector_Add(vec3d(rLeft, 0, rLeft), self.vLookDirY)
        vLeft = pygao.Vector_Mul(vLeft, speed * self.fElapsedTime)

        if self.keys[pygao.ltk(self.cfg["controls"]["forward"])]:
            self.vCamera = pygao.Vector_Add(self.vCamera, vForward)

        if self.keys[pygao.ltk(self.cfg["controls"]["backwards"])]:
            self.vCamera = pygao.Vector_Sub(self.vCamera, vForward)

        #if self.keys[pygao.ltk(self.cfg["controls"]["left"])]:
            #self.vCamera.x -= 8 * self.fElapsedTime
        #    self.vCamera = pygao.Vector_Add(self.vCamera, vLeft)

        #if self.keys[pygao.ltk(self.cfg["controls"]["right"])]:
            #self.vCamera.x += 8 * self.fElapsedTime
        #    self.vCamera = pygao.Vector_Sub(self.vCamera, vLeft)

        #if self.keys[pygame.K_LEFT]:
        #    self.fYaw -= 2 * self.fElapsedTime
        #if self.keys[pygame.K_RIGHT]:
        #    self.fYaw += 2 * self.fElapsedTime
        #if self.keys[pygame.K_UP]:
        #    self.fPitch -= 2 * self.fElapsedTime
        #if self.keys[pygame.K_DOWN]:
        #    self.fPitch += 2 * self.fElapsedTime

        if size[0] / 2 - lock_value > mouse[0]:
            nr_mouse = True
            self.fYaw -= self.cfg["controls"]["lrsensitivity"] * self.fElapsedTime
        if size[0] / 2 + lock_value < mouse[0]:
            nr_mouse = True
            self.fYaw += self.cfg["controls"]["lrsensitivity"] * self.fElapsedTime
        if size[1] / 2 - lock_value > mouse[1]:
            nr_mouse = True
            if self.vTargetOffsetY < 1.5: self.vTargetOffsetY += 2 * self.fElapsedTime
        if size[1] / 2 + lock_value < mouse[1]:
            nr_mouse = True
            if self.vTargetOffsetY > -1.5: self.vTargetOffsetY -= 2 * self.fElapsedTime

        if nr_mouse:
            nmx = size[0] / 2
            nmy = size[1] / 2
            pygame.mouse.set_pos((nmx, nmy))


        # place blocks
        if self.keys[pygame.K_i]:
            loc = [round(self.vTarget.x), round(self.vTarget.y), round(self.vTarget.z)]
            pyes = True
            for p in self.blockcoord:
                if p == loc:
                    pyes = False

            if pyes:
                self.models.append([
                    loc,
                    (0, 0, 0),
                    pygao.LoadFromObjectFile("assets/box.obj")
                ])
                self.blockcoord.append(loc)

        if self.keys[pygame.K_k]:
            print(self.blockcoord)

        if self.keys[pygame.K_q]:
            self.light_direction = self.vTarget



    def triangle_project(self, tri, tris):
        vOffsetView = vec3d(1, 1, 0)
        triProjected = tris
        triProjected.lum = tri.lum
        triProjected.tag = tri.tag
        for j, vsj in enumerate(tris.vs):
            triProjected.vs[j] = pygao.Matrix_MultiplyVector(self.matProj, tri.vs[j])

            triProjected.vs[j] = pygao.Vector_Div(triProjected.vs[j], triProjected.vs[j].w)

            triProjected.vs[j].x *= -1.0
            triProjected.vs[j].y *= -1.0

            triProjected.vs[j] = pygao.Vector_Add(triProjected.vs[j], vOffsetView)
            triProjected.vs[j].x *= 0.5 * self.cfg["size"][0]
            triProjected.vs[j].y *= 0.5 * self.cfg["size"][1]

        #print(triProjected)

        return triProjected


    # Handle repeated calculations
    # @jit(nopython=True)
    def content(self):
        # Update rotation matricies
        self.matrices()

        vecTrianglesToRaster = []
        vecSecondSet = []
        # Go through triangles of mesh [loadme]
        for modelToLoad in self.models:
            # World to Camera
            self.matRotZ = pygao.Matrix_MakeRotationZ(modelToLoad[1][2])
            self.matRotY = pygao.Matrix_MakeRotationY(modelToLoad[1][1])
            self.matRotX = pygao.Matrix_MakeRotationX(modelToLoad[1][0])
            self.matTrans = pygao.Matrix_MakeTranslation(modelToLoad[0][0], modelToLoad[0][1], modelToLoad[0][2])

            self.matWorld = pygao.Matrix_MakeIdentity()
            self.matWorld = pygao.Matrix_MultiplyMatrix(self.matRotZ, self.matRotX)
            self.matWorld = pygao.Matrix_MultiplyMatrix(self.matRotY, self.matWorld)
            self.matWorld = pygao.Matrix_MultiplyMatrix(self.matWorld, self.matTrans)

            for tri in modelToLoad[2]:
                # Split mesh into triangles with vectors
                tris = triangle(
                    vec3d(tri[0].x, tri[0].y, tri[0].z),
                    vec3d(tri[1].x, tri[1].y, tri[1].z),
                    vec3d(tri[2].x, tri[2].y, tri[2].z)
                )
                triProjected = tris
                triTransformed = tris
                triViewed = tris

                # Rotate and Translate triangle vectors
                for i, vs in enumerate(tris.vs):
                    # Rotate
                    triTransformed.vs[i] = pygao.Matrix_MultiplyVector(self.matWorld, tris.vs[i])

                # Calculate normals
                normal, line1, line2 = vec3d(), vec3d(), vec3d()
                line1 = pygao.Vector_Sub(triTransformed.vs[1], triTransformed.vs[0])
                line2 = pygao.Vector_Sub(triTransformed.vs[2], triTransformed.vs[0])

                normal = pygao.Vector_CrossProduct(line1, line2)
                normal = pygao.Vector_Normalize(normal)

                # Project and scale the triangle vectors if visible
                #if normal.z < 0:
                vCameraRay = pygao.Vector_Sub(triTransformed.vs[0], self.vCamera)
                if pygao.Vector_DotProduct(normal, vCameraRay) < 0:
                    # Illumination
                    self.light_direction = pygao.Vector_Normalize(self.light_direction)
                    dp = max(0.1, pygao.Vector_DotProduct(self.light_direction, normal))
                    lumi = abs(dp * 255)
                    triTransformed.lum = (lumi, lumi, lumi)

                    for i, vs in enumerate(tris.vs):
                        triViewed.vs[i] = pygao.Matrix_MultiplyVector(self.matView, triTransformed.vs[i])


                    nClippedTriangles = pygao.Triangle_ClipAgainstPlane(vec3d(0,0,0.1), vec3d(0,0,1), triViewed)

                    #if nClippedTriangles[0] == 0: pass
                    if nClippedTriangles[0] == 1:
                        vecTrianglesToRaster.append(self.triangle_project(nClippedTriangles[1], tris))
                    if nClippedTriangles[0] == 2:
                        tri1 = self.triangle_project(nClippedTriangles[1], tris)
                        tri2 = self.triangle_project(nClippedTriangles[2], tris)

                        vecTrianglesToRaster.append(tri2)
                        vecTrianglesToRaster.append(tri1)




                        #print(pt1)
                        #print(pt2)

                #print(len(vecTrianglesToRaster))

        vecTrianglesToRaster.sort(key = pygao.paintersSort, reverse = True)

        for triToRaster in vecTrianglesToRaster:

            clipped = [triangle(), triangle()]
            listTriangles = []
            listTriangles.append(triToRaster)
            nNewTriangles = 1

            for p in range(4):
                nTrisToAdd = 0
                while nNewTriangles > 0:
                    test = listTriangles[0]
                    del listTriangles[0]
                    nNewTriangles -= 1
                    if p == 0:
                        trisData = pygao.Triangle_ClipAgainstPlane(vec3d(0, 0, 0), vec3d(0, 1, 0), test)
                    if p == 1:
                        trisData = pygao.Triangle_ClipAgainstPlane(vec3d(0, self.cfg["size"][1] - 1, 0), vec3d(0, -1, 0), test)
                    if p == 2:
                        trisData = pygao.Triangle_ClipAgainstPlane(vec3d(0, 0, 0), vec3d(1, 0, 0), test)
                    if p == 3:
                        trisData = pygao.Triangle_ClipAgainstPlane(vec3d(self.cfg["size"][0] - 1, 0, 0), vec3d(-1, 0, 0), test)

                    nTrisToAdd = trisData[0]
                    if nTrisToAdd != 0: clipped[0] = trisData[1]
                    if nTrisToAdd == 2: clipped[1] = trisData[2]

                    for w in range(nTrisToAdd):
                        listTriangles.append(clipped[w])
                nNewTriangles = len(listTriangles)

            for t in listTriangles:
                pygame.draw.polygon(
                    self.root,
                    t.lum,
                    [
                        (t.vs[0].x, t.vs[0].y),
                        (t.vs[1].x, t.vs[1].y),
                        (t.vs[2].x, t.vs[2].y)
                    ],
                    width = 0
                )

                if self.cfg["wireFrame"]:
                    pygao.DrawTriangle(
                        t.vs[0].x, t.vs[0].y,
                        t.vs[1].x, t.vs[1].y,
                        t.vs[2].x, t.vs[2].y,
                        tuple(self.cfg["wireFrameColour"]),
                        self.root
                    )

    def __fps(self):
        self.fps = round(1/self.fElapsedTime, self.cfg["roundFPS"])
        pygame.display.set_caption(self.cfg["title"].replace("%fps%", str(self.fps)))

    # Generate and time monotonic deltatime
    def deltatime(self):
        self.tp2 = time.monotonic()
        elapsedTime = self.tp2 - self.tp1
        self.tp1 = self.tp2
        self.fElapsedTime = elapsedTime
        #self.fTheta += 1.0 * self.fElapsedTime

        if self.fElapsedTime != 0:
            if not self.cfg["constantFPS"]:
                if (1/self.fElapsedTime - self.fps) >= 5 or (1/self.fElapsedTime - self.fps) <= -5:
                    self.__fps()
            else:
                self.__fps()

    # Main loop function
    def loop(self):
        while self.active:
            self.root.fill((0, 0, 0))
            self.deltatime()
            for event in pygame.event.get():
                self.events(event)
            self.key_events()

            self.content()
            pygame.display.flip()

        self.cleanup()

if __name__ == "__main__":
    app = GraphicsEngine()
