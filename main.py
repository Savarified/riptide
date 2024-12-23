import pygame
import sys
import math
import os

os.system('clear')
fullscreen = False

#create new window
os.environ['SDL_VIDEO_WINDOW_POS'] = str(1000) + "," + str(0)
pygame.init()
#define window specifications
WIDTH, HEIGHT = 600, 400
if fullscreen:
    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

sky = [67, 166, 209]
colors = [[255,0,0],
          [0,0,255]]
cube = [[0,0,0],#
        [1,0,0],
        [1,1,0],
        [0,1,0],
        
        [0,0,1],#
        [1,0,1],
        [1,1,1],
        [0,1,1]]

            
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
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def project(point):
    #perspective projection algorithm
    x,y,z = point[0], point[1], point[2]
    x += -_cam[0]
    y += -_cam[1]
    z += -_cam[2]
    x = x * _scale
    y = y * _scale
    z = z * _scale
    
    d = [x,y,z] #vertice points
    s = [600,400] #display size
    r = [400,266, 200] #focal plane //?
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
meshScale = 16
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
        while i < round(len(mesh)/4):
            quad = [mesh[i], mesh[i+1], mesh[i+2], mesh[i+3]]
            drawQuad(quad, colors[0])
            i+=3
            quad = [mesh[i], mesh[i+1], mesh[i+2], mesh[i+3]]
            drawQuad(quad, colors[1])
            i+=3

WASD = [0,0,0,0]
speed = 0.1
player = character(0.9,1.5,6)
def playerMovement():
    global _cam
    player.x += float(int(WASD[1])) * speed
    player.x -= float(int(WASD[3])) * speed
    player.z -= float(int(WASD[0])) * speed
    player.z += float(int(WASD[2])) * speed

    _cam = [player.x, player.y, player.z, _cam[3], _cam[4], _cam[5]]
        
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
