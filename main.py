import pygame
import sys
import math
import os

os.system('cls')
fullscreen = False

#create new window
os.environ['SDL_VIDEO_WINDOW_POS'] = str(1000) + "," + str(32)
pygame.init()
#define window specifications
WIDTH, HEIGHT = 600, 400
if fullscreen:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

sky = [67, 166, 209]
colors = [[255,0,0],
          [0,0,255],
          [0,255,0]]
textures = ['textures/grass.png']
cube = [
        [0,1,0],#bottom
        [1,1,0],
        [1,1,1],
        [0,1,1],
        [0,0,1],#far face
        [1,0,1],
        [1,1,1],
        [0,1,1],
        [0,0,0],#left side
        [0,1,0],
        [0,1,1],
        [0,0,1],
        [1,0,0],#right side
        [1,1,0],
        [1,1,1],
        [1,0,1],
        [0,0,0],#top
        [1,0,0],
        [1,0,1],
        [0,0,1],
        [0,0,0],#close face
        [1,0,0],
        [1,1,0],
        [0,1,0],
        ]

            
pygame.display.set_caption('Riptide')
font = pygame.font.Font(None, 16)
clock = pygame.time.Clock()
FPS = 30
_cam = [0,0,1,0,0,0]
_scale = 4
mouseDown = False

class vox:
    _registry = []
    def __init__(self, x, y, z, o):
        self.x = x
        self.y = y
        self.z = z
        self.o = o
        self._registry.append(self)

class character:
    def __init__(self, x, y, z, dy):
        self.x = x
        self.y = y
        self.z = z
        self.dy = dy

def cycle(a, b, t):
    return a + ((t - a) % (b - a + 1))
    '''while (t > b):
        t -= (b-a)
    if(t<a):
        t = b
    return t'''

eps = 0.001
def project(point):
    #perspective projection algorithm
    x,y,z = point[0], point[1], point[2]
    x *= _scale
    y *= _scale
    z *= _scale

    x -= _cam[0]
    y += _cam[1]
    z -= _cam[2]
    z += eps

    d = [x,y,z] #vertice points
    s = [600,400] #display size
    r = [400,266, 400] #focal plane //?
    xi = (d[0] * s[0])/(d[2] * r[0]) * r[2]
    yi = (d[1] * s[1])/(d[2] * r[1]) * r[2]
    xi += s[0]/2
    yi += s[1]/2
    ci = [xi, yi]
    return ci

def drawQuad(quad, drawColor):
    screenPoints = []
    for point in quad:
        screenPoints.append(project(point))
    pygame.draw.polygon(screen, drawColor, screenPoints)

testBlock = vox(0,0,0,0)
meshScale = 1
def render():
    global cube
    for voxel in vox._registry:
        mesh = []
        for point in cube:
            vert = [(point[0]+voxel.x)*meshScale,
                    (point[1]+voxel.y)*meshScale,
                    (point[2]+voxel.z)*meshScale]
            mesh.append(vert)
        i = 0
        quadTotal = round(len(mesh)/4)
        while i < quadTotal:
            face = i*4
            quad = [mesh[face], mesh[face+1], mesh[face+2], mesh[face+3]]
            drawQuad(quad, colors[cycle(0, len(colors)-1, i)])
            i+=1

WASD = [0,0,0,0]
speed = .75
player = character(0,2,-6, 0)
groundPlane = 2
gravity = 0
def playerMovement():
    global _cam, gravity
    player.x -= float(int(WASD[1])) * speed
    player.x += float(int(WASD[3])) * speed
    player.z += float(int(WASD[0])) * speed
    player.z -= float(int(WASD[2])) * speed
    player.y += player.dy
    if(player.y < groundPlane):
        player.y = groundPlane
        player.dy = 0
        gravity = 0

    if player.y > groundPlane:
        gravity += .02
        player.dy -= gravity

    _cam = [player.x, player.y, player.z, _cam[3], _cam[4], _cam[5]]

def jump():
    print('jump')
    player.dy += 1
        
run = True
def quitGame():
    run = False
    pygame.quit()
    sys.exit()

shiftDown = False
while run:
    screen.fill(sky)
    playerMovement()
    render()
    pygame.display.flip()
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
                
            if event.key == pygame.K_w: #player controls
                WASD[0] = True
            if event.key == pygame.K_a:
                WASD[1] = True
            if event.key == pygame.K_s:
                WASD[2] = True
            if event.key == pygame.K_d:
                WASD[3] = True
            
            if event.key == pygame.K_SPACE:
                jump()

            if event.key == pygame.K_c: #camera position + scale
                print(f'POSITION x:{_cam[0]} y:{_cam[1]} z:{_cam[2]}\n')

            if event.key == pygame.K_LSHIFT: shiftDown = True
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w: #player controls
                WASD[0] = False
            if event.key == pygame.K_a:
                WASD[1] = False
            if event.key == pygame.K_s:
                WASD[2] = False
            if event.key == pygame.K_d:
                WASD[3] = False
            if event.key == pygame.K_LSHIFT: shiftDown = False
