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
font = font = pygame.font.Font(None, 36)

sky = [67, 166, 209]
colors = [[255,0,0],
          [0,0,255],
          [0,255,0]]
texture_paths = ['textures/grass_block_side.png',
            'textures/dirt.png',
            'textures/stone.png',
            'textures/oak_log.png']
textures = []
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
textureScale = 64
for tex_path in texture_paths:
    tex = pygame.image.load(tex_path)
    tex = pygame.transform.scale(tex, (textureScale, textureScale))
    textures.append(tex)
            
pygame.display.set_caption('Riptide')
font = pygame.font.Font(None, 16)
clock = pygame.time.Clock()
FPS = 30
_cam = [0,0,1,0,0,0]
_scale = 4
mouseDown = False

def debugText(string, color, position):
    text = font.render(str(string), True, color)
    textRect = text.get_rect()
    textRect.top = position[1]
    textRect.left = position[0]
    screen.blit(text, textRect)

class vox:
    _registry = []
    def __init__(self, x, y, z, o, mesh):
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

eps = 0.001
s = [600,400] #display size
r = [400,266, 400] #focal plane //?
def project(point):
    #perspective projection algorithm
    x,y,z = point[0], point[1], point[2]
    x *= _scale
    y *= _scale
    z *= _scale

    x -= _cam[0]
    y += _cam[1]
    z -= _cam[2] - eps

    xi = (x * s[0])/(z * r[0]) * r[2]
    yi = (y * s[1])/(z * r[1]) * r[2]

    xi += 300
    yi += 200
    ci = [xi, yi]
    return ci

drawColor = (255,0,255,255)
def drawQuad(quad):
    screenPoints = []
    for point in quad:
        screenPoints.append(project(point))
    pygame.draw.polygon(screen, drawColor, screenPoints)

def createMeshes():
    for voxel in vox._registry:
        voxel.mesh = []
        for point in cube: #
            vert = [(point[0]+voxel.x),
                    (point[1]+voxel.y),
                    (point[2]+voxel.z)]
            voxel.mesh.append(vert)

grass_ = vox(0,0,0,2, [])
vert = []
def render():
    if len(vox._registry) > 1: vox._registry.sort(key=lambda v: (v.z - _cam[2])**2 + (v.x - _cam[0])**2 + (v.y - _cam[1])**2, reverse=True)
    i = 0
    for voxel in vox._registry: #2
        i = 0
        quadTotal = round(len(voxel.mesh)/4)
        while i < quadTotal:
            face = i*4
            quad = [voxel.mesh[face], voxel.mesh[face+1], voxel.mesh[face+2], voxel.mesh[face+3]]
            drawQuad(quad)
            i+=1
        texture = textures[cycle(0, len(textures)-1, voxel.o)]
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (screen.get_at((x,y))==drawColor):
                    screen.set_at((x,y), texture.get_at((cycle(0,textureScale-1,x),cycle(0,textureScale-1,y))))

WASD = [0,0,0,0]
speed = .25
player = character(4.75,2,-13.5, 0)
groundPlane = 2
gravity = 0
def playerMovement():
    global _cam, gravity
    player.x -= float(int(WASD[1])) * speed
    player.x += float(int(WASD[3])) * speed
    player.z += float(int(WASD[0])) * speed
    player.z -= float(int(WASD[2])) * speed
    player.y += player.dy
    if(player.y <= groundPlane):
        player.y = groundPlane
        player.dy = 0
        gravity = 0

    if player.y > groundPlane:
        gravity += .02
        player.dy -= gravity

    _cam = [player.x, player.y, player.z, _cam[3], _cam[4], _cam[5]]

def jump():
    if player.y <= 2.1:
        player.dy += .5
        
run = True
def quitGame():
    run = False
    pygame.quit()
    sys.exit()

createMeshes()
shiftDown = False
while run:
    screen.fill(sky)
    playerMovement()
    render()
    debugText(round(clock.get_fps()),(255,255,255,255), [0,0])
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

            if event.key == pygame.K_LCTRL:
                player.y -= 1

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
