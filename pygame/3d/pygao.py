import pygame, math, json
from numba import jit

global cfg
with open("assets/config.json") as cfile:
    cfg = json.load(cfile)

@jit(nopython=True)
def ltk(letter):
    if letter == "a": return pygame.K_a
    if letter == "b": return pygame.K_b
    if letter == "c": return pygame.K_c
    if letter == "d": return pygame.K_d
    if letter == "e": return pygame.K_e
    if letter == "f": return pygame.K_f
    if letter == "g": return pygame.K_g
    if letter == "h": return pygame.K_h
    if letter == "i": return pygame.K_i
    if letter == "j": return pygame.K_j
    if letter == "k": return pygame.K_k
    if letter == "l": return pygame.K_l
    if letter == "m": return pygame.K_m
    if letter == "n": return pygame.K_n
    if letter == "o": return pygame.K_o
    if letter == "p": return pygame.K_p
    if letter == "q": return pygame.K_q
    if letter == "r": return pygame.K_r
    if letter == "s": return pygame.K_s
    if letter == "t": return pygame.K_t
    if letter == "u": return pygame.K_u
    if letter == "v": return pygame.K_v
    if letter == "w": return pygame.K_w
    if letter == "x": return pygame.K_x
    if letter == "y": return pygame.K_y
    if letter == "z": return pygame.K_z
    if letter == " ": return pygame.K_SPACE
    if letter == "lshift": return pygame.K_LSHIFT
    if letter == "lctrl": return pygame.K_LCTRL
    if letter == "left": return pygame.K_LEFT
    if letter == "right": return pygame.K_RIGHT
    if letter == "up": return pygame.K_UP
    if letter == "down": return pygame.K_DOWN

    return pygame.K_SPACE


class vec3d:
    def __init__(self, x = 0, y = 0, z = 0, w = 1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.xyz = [self.x, self.y, self.z, self.w]
        
    def nxyz(self):
        self.xyz = [self.x, self.y, self.z, self.w]
        return self.xyz
        
def list_to_vec3d(l):
    return vec3d(l[0],l[1],l[2],l[3])
        
class triangle:
    def __init__(self, v1 = vec3d(), v2 = vec3d(), v3 = vec3d(), ready = False):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.points = [
            self.v1.xyz, self.v2.xyz, self.v3.xyz
        ]
        self.vs = [self.v1, self.v2, self.v3]
        self.tag = ""

        self.lum = (255, 255, 255)
        
        if ready:
            self.v1 = vec3d(1, 1, 1, 1)
            self.v2 = vec3d(1, 1, 1, 1)
            self.v3 = vec3d(1, 1, 1, 1)
            self.points = [
                self.v1.xyz, self.v2.xyz, self.v3.xyz
            ]
            self.vs = [self.v1, self.v2, self.v3]
            self.tag = ""

            self.lum = (255, 255, 255)
    
    def nvs(self):
        self.vs = [self.v1, self.v2, self.v3]
        return self.vs
        

class mat4x4:
    def __init__(self):
        self.m = [[0 for x in range(4)] for y in range(4)]

@jit(nopython=True)
def MultiplyMatrixVector(vector = vec3d(), mat = mat4x4()):
    w = vector.x * mat.m[0][3] + vector.y * mat.m[1][3] + vector.z * mat.m[2][3] + mat.m[3][3]
    if w != 0.0:
        vector.x /= w;vector.y /= w;vector.z /= w

    return vec3d(
        vector.x * mat.m[0][0] + vector.y * mat.m[1][0] + vector.z * mat.m[2][0] + mat.m[3][0],
        vector.x * mat.m[0][1] + vector.y * mat.m[1][1] + vector.z * mat.m[2][1] + mat.m[3][1],
        vector.x * mat.m[0][2] + vector.y * mat.m[1][2] + vector.z * mat.m[2][2] + mat.m[3][2],
        w
    )

#v = vec3d()
#    v.x = i.x * m.m[0][0] + i.y * m.m[1][0] + i.z * m.m[2][0] + i.w * m.m[3][0]
#    v.y = i.x * m.m[0][1] + i.y * m.m[1][1] + i.z * m.m[2][1] + i.w * m.m[3][1]
#    v.z = i.x * m.m[0][2] + i.y * m.m[1][2] + i.z * m.m[2][2] + i.w * m.m[3][2]
#    v.w = i.x * m.m[0][3] + i.y * m.m[1][3] + i.z * m.m[2][3] + i.w * m.m[3][3]
#    return v

def Matrix_MultiplyVector(m, i):
    v = vec3d()
    v.x = i.x * m.m[0][0] + i.y * m.m[1][0] + i.z * m.m[2][0] + i.w * m.m[3][0]
    v.y = i.x * m.m[0][1] + i.y * m.m[1][1] + i.z * m.m[2][1] + i.w * m.m[3][1]
    v.z = i.x * m.m[0][2] + i.y * m.m[1][2] + i.z * m.m[2][2] + i.w * m.m[3][2]
    v.w = i.x * m.m[0][3] + i.y * m.m[1][3] + i.z * m.m[2][3] + i.w * m.m[3][3]
    return v

def Matrix_MakeIdentity():
    matrix = mat4x4()
    matrix.m[0][0] = 1.0
    matrix.m[1][1] = 1.0
    matrix.m[2][2] = 1.0
    matrix.m[3][3] = 1.0
    return matrix

def Matrix_MakeRotationX(fAngleRad):
    matrix = mat4x4()
    matrix.m[0][0] = 1
    matrix.m[1][1] = math.cos(fAngleRad)
    matrix.m[1][2] = math.sin(fAngleRad)
    matrix.m[2][1] = -math.sin(fAngleRad)
    matrix.m[2][2] = math.cos(fAngleRad)
    matrix.m[3][3] = 1
    return matrix

def Matrix_MakeRotationY(fAngleRad):
    matrix = mat4x4()
    matrix.m[0][0] = math.cos(fAngleRad)
    matrix.m[0][2] = math.sin(fAngleRad)
    matrix.m[2][0] = -math.sin(fAngleRad)
    matrix.m[1][1] = 1
    matrix.m[2][2] = math.cos(fAngleRad)
    matrix.m[3][3] = 1
    return matrix

def Matrix_MakeRotationZ(fAngleRad):
    matrix = mat4x4()
    matrix.m[0][0] = math.cos(fAngleRad)
    matrix.m[0][1] = math.sin(fAngleRad)
    matrix.m[1][0] = -math.sin(fAngleRad)
    matrix.m[1][1] = math.cos(fAngleRad)
    matrix.m[2][2] = 1
    matrix.m[3][3] = 1
    return matrix

def Matrix_MakeTranslation(x,y,z):
    matrix = mat4x4()
    matrix.m[0][0] = 1
    matrix.m[1][1] = 1
    matrix.m[2][2] = 1
    matrix.m[3][3] = 1
    matrix.m[3][0] = x
    matrix.m[3][1] = y
    matrix.m[3][2] = z
    return matrix

def Matrix_MakeProjection(fFovDegrees, fAspectRatio, fNear, fFar):
    matrix1 = mat4x4()
    fFovRad = 1.0 / math.tan(fFovDegrees * 0.5 / 180 * math.pi)
    matrix1.m[0][0] = fAspectRatio * fFovRad
    matrix1.m[1][1] = fFovRad
    matrix1.m[2][2] = fFar / (fFar - fNear)
    matrix1.m[3][2] = (-fFar * fNear) / (fFar - fNear)
    matrix1.m[2][3] = 1.0
    matrix1.m[3][3] = 0.0
    return matrix1

def Matrix_MultiplyMatrix(m1, m2):
    matrix = mat4x4()
    for c in range(4):
        for r in range(4):
            matrix.m[r][c] = m1.m[r][0] * m2.m[0][c] + m1.m[r][1] * m2.m[1][c] + m1.m[r][2] * m2.m[2][c] + m1.m[r][3] * m2.m[3][c]
    return matrix


def Matrix_PointAt(pos, target, up):
    newForward = Vector_Sub(target, pos)
    newForward = Vector_Normalize(newForward)

    a = Vector_Mul(newForward, Vector_DotProduct(up, newForward))
    newUp = Vector_Sub(up, a)
    newUp = Vector_Normalize(newUp)

    newRight = Vector_CrossProduct(newUp, newForward)
    matrix = mat4x4()
    matrix.m[0][0] = newRight.x;    matrix.m[0][1] = newRight.y;    matrix.m[0][2] = newRight.z;    matrix.m[0][3] = 0;
    matrix.m[1][0] = newUp.x;       matrix.m[1][1] = newUp.y;       matrix.m[1][2] = newUp.z;       matrix.m[1][3] = 0;
    matrix.m[2][0] = newForward.x;  matrix.m[2][1] = newForward.y;  matrix.m[2][2] = newForward.z;  matrix.m[2][3] = 0;
    matrix.m[3][0] = pos.x;         matrix.m[3][1] = pos.y;         matrix.m[3][2] = pos.z;         matrix.m[3][3] = 1;
    return matrix

def Matrix_QuickInverse(m):
    matrix = mat4x4()
    matrix.m[0][0] = m.m[0][0]; matrix.m[0][1] = m.m[1][0]; matrix.m[0][2] = m.m[2][0]; matrix.m[0][3] = 0.0;
    matrix.m[1][0] = m.m[0][1]; matrix.m[1][1] = m.m[1][1]; matrix.m[1][2] = m.m[2][1]; matrix.m[1][3] = 0.0;
    matrix.m[2][0] = m.m[0][2]; matrix.m[2][1] = m.m[1][2]; matrix.m[2][2] = m.m[2][2]; matrix.m[2][3] = 0.0;
    matrix.m[3][0] = -(m.m[3][0] * matrix.m[0][0] + m.m[3][1] * matrix.m[1][0] + m.m[3][2] * matrix.m[2][0]);
    matrix.m[3][1] = -(m.m[3][0] * matrix.m[0][1] + m.m[3][1] * matrix.m[1][1] + m.m[3][2] * matrix.m[2][1]);
    matrix.m[3][2] = -(m.m[3][0] * matrix.m[0][2] + m.m[3][1] * matrix.m[1][2] + m.m[3][2] * matrix.m[2][2]);
    matrix.m[3][3] = 1.0;
    return matrix

Vector_Add = lambda v1, v2: vec3d(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)
Vector_Sub = lambda v1, v2: vec3d(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
Vector_Mul = lambda v1, k: vec3d(v1.x * k, v1.y * k, v1.z * k)
Vector_Div = lambda v1, k: vec3d(v1.x / k, v1.y / k, v1.z / k)
Vector_DotProduct = lambda v1, v2: v1.x*v2.x + v1.y*v2.y + v1.z*v2.z
Vector_Length = lambda v: math.sqrt(Vector_DotProduct(v, v))

def Vector_Normalize(v):
    l = Vector_Length(v)
    x = v.x / l if l != 0 else 0
    y = v.y / l if l != 0 else 0
    z = v.z / l if l != 0 else 0
    return vec3d(x, y, z)

def Vector_FromArray(array):
    return vec3d(array[0], array[1], array[2])

def Vector_CrossProduct(v1, v2):
    v = vec3d()
    v.x = v1.y * v2.z - v1.z * v2.y
    v.y = v1.z * v2.x - v1.x * v2.z
    v.z = v1.x * v2.y - v1.y * v2.x
    return v

def Vector_IntersectPlane(plane_p, plane_n, lineStart, lineEnd):
    plane_n = Vector_Normalize(plane_n)
    plane_d = -(Vector_DotProduct(plane_n, plane_p))
    ad = Vector_DotProduct(lineStart, plane_n)
    bd = Vector_DotProduct(lineEnd, plane_n)
    t = (-plane_d - ad) / (bd - ad) if (-plane_d - ad) != 0 and (bd - ad) != 0 else 0
    lineStartToEnd = Vector_Sub(lineEnd, lineStart)
    lineToIntersect = Vector_Mul(lineStartToEnd, t)
    return Vector_Add(lineStart, lineToIntersect)
    
def RGB_TintRGB(color1, color2):
    unnomalized = [color1[0] + color2[0], color1[1] + color2[1], color1[2] + color2[2]]
    new = Vector_Normalize(Vector_FromArray(unnomalized))
    new.x *= 255; new.y *= 255; new.z *= 255;
    return (new.x, new.y, new.z)
    
def Triangle_ClipAgainstPlane(plane_p, plane_n, in_tri):
    plane_n = Vector_Normalize(plane_n)
    
    dist = lambda p: (plane_n.x * p.x + plane_n.y * p.y + plane_n.z * p.z - Vector_DotProduct(plane_n, plane_p))
    
    inside_points = []; nInsidePointCount = 0
    outside_points = []; nOutsidePointCount = 0
    
    d0 = dist(in_tri.vs[0])
    d1 = dist(in_tri.vs[1])
    d2 = dist(in_tri.vs[2])
    
    
    if (d0 >= 0): inside_points.append(in_tri.vs[0]);nInsidePointCount+=1;
    else: outside_points.append(in_tri.vs[0]);nOutsidePointCount+=1;
    if (d1 >= 0): inside_points.append(in_tri.vs[1]);nInsidePointCount+=1;
    else: outside_points.append(in_tri.vs[1]);nOutsidePointCount+=1;
    if (d2 >= 0): inside_points.append(in_tri.vs[2]);nInsidePointCount+=1;
    else: outside_points.append(in_tri.vs[2]);nOutsidePointCount+=1;
    
    if nInsidePointCount == 0: return [0]
    elif nInsidePointCount == 3: return [1, in_tri]
    elif nInsidePointCount == 1 and nOutsidePointCount == 2:
        out_tri0 = triangle()
        out_tri0.lum = RGB_TintRGB((0, 0, 255), in_tri.lum) if cfg["showClipping"] else in_tri.lum
        
        out_tri0.vs[0] = inside_points[0]
        out_tri0.vs[1] = Vector_IntersectPlane(plane_p, plane_n, inside_points[0], outside_points[0])
        out_tri0.vs[2] = Vector_IntersectPlane(plane_p, plane_n, inside_points[0], outside_points[1])
        
        return [1, out_tri0]
    elif nInsidePointCount == 2 and nOutsidePointCount == 1:
        out_tri1 = triangle(
            inside_points[0],
            inside_points[1],
            Vector_IntersectPlane(plane_p, plane_n, inside_points[0], outside_points[0])
        )
        out_tri2 = triangle(
            inside_points[1],
            out_tri1.vs[2],
            Vector_IntersectPlane(plane_p, plane_n, inside_points[1], outside_points[0])
        )
        out_tri1.lum = RGB_TintRGB((255, 0, 0), in_tri.lum) if cfg["showClipping"] else in_tri.lum
        out_tri2.lum = RGB_TintRGB((0, 255, 0), in_tri.lum) if cfg["showClipping"] else in_tri.lum
        
        return [2, out_tri2, out_tri1]

@jit(nopython=True)
def DrawTriangle(x1, y1, x2, y2, x3, y3, color, surface):
    pygame.draw.line(surface, color, (x1, y1), (x2, y2))
    pygame.draw.line(surface, color, (x2, y2), (x3, y3))
    pygame.draw.line(surface, color, (x1, y1), (x3, y3))

def LoadFromObjectFile(filename):
    tris = []
    with open(filename, "r") as modelfile:
        modelobj = modelfile.read().split("\n")
        verts = []

        for l in modelobj:
            junk = ""
            sl = l.split(" ")
            if sl[0] == "v":
                junk = sl[0]
                v = vec3d()
                v.x = float(sl[1]);v.y = float(sl[2]);v.z = float(sl[3])
                verts.append(v)
            if sl[0] == "f":
                f = []
                for j in (1,2,3): f.append(int(sl[j]))
                tris.append([verts[f[0] - 1], verts[f[1] - 1], verts[f[2] - 1]])

    return tris

def paintersSort(e):
    return (e.vs[0].z + e.vs[1].z + e.vs[2].z) / 3
