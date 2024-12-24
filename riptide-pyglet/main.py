import pyglet
from pyglet.window import key
from pyglet import gl
import sys
import math
import os

os.system('cls')
fullscreen = False

#create new window
os.environ['SDL_VIDEO_WINDOW_POS'] = str(1000) + "," + str(32)
#define window specifications
WIDTH, HEIGHT = 600, 400
window = pyglet.window.Window(WIDTH, HEIGHT, "Riptide")
batch = pyglet.graphics.Batch()
font = pyglet.font.load(None, 36)


sky = [67, 166, 209,255]
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
def load_textures(texture_paths):
    textures = []
    for tex_path in texture_paths:
        tex = pyglet.image.load(tex_path)
        if tex:
            tex = tex.get_texture()
            tex.width = textureScale
            tex.height = textureScale
            textures.append(tex)
        else:
            print(f"Error loading texture: {tex_path}")
    return textures

FPS = 30
_cam = [0,0,1,0,0,0]
_scale = 4
mouseDown = False

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
    while (t>b):
        t -= (b-a)
    if(t<a):
        t = b
    return t

def read_pixel_color(x, y):
    try:
        # Ensure the coordinates are within the window bounds
        if not (0 <= x < window.width and 0 <= y < window.height):
            raise ValueError("Coordinates out of bounds")

        # Flip the y-coordinate to match OpenGL's coordinate system
        y = window.height - y  # Flip Y axis to match OpenGL's origin

        # Create a buffer to hold the RGBA values (4 bytes: R, G, B, A)
        buffer = (gl.GLubyte * 4)()

        # Use glReadPixels to read the color data
        gl.glReadPixels(x, y, 1, 1, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, buffer)

        return (buffer[0], buffer[1], buffer[2], buffer[3])

    except Exception as e:
        print(f"Error reading pixel color: {e}")
        return (0, 0, 0, 0)

def get_tex_color(x, y, texture):
    pixel = texture.get_image_data().get_data('RGBA', texture.width * 4)
    index = (y * texture.width + x) * 4
    r = pixel[index]
    g = pixel[index + 1]
    b = pixel[index + 2]
    a = pixel[index + 3]
    
    return (r, g, b, a)

def set_color_at_window_coordinate(x, y, color):
    y = window.height - y
    gl.glColor4ub(color[0], color[1], color[2], color[3])
    pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2f', [x, y]))

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
    screen_points = []
    for point in quad:
        ci = project(point)
        screen_points.append(ci[0])
        screen_points.append(ci[1])
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                         ('v2f', screen_points),
                         ('c3B', [255, 0, 255] * 4))  # Draw in magenta

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
        quadTotal = len(voxel.mesh)//4
        while i < quadTotal:
            face = i*4
            quad = [voxel.mesh[face], voxel.mesh[face+1], voxel.mesh[face+2], voxel.mesh[face+3]]
            drawQuad(quad)
            i+=1
        texture = textures[cycle(0, len(textures)-1, voxel.o)]
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (read_pixel_color(x,y)==drawColor):
                    texColor = get_tex_color(x,y,texture)
                    set_color_at_window_coordinate(x,y,texColor)

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

@window.event
def on_key_press(symbol, modifiers):
    global WASD
    if symbol == key.W:
        WASD[0] = True
    if symbol == key.A:
        WASD[1] = True
    if symbol == key.S:
        WASD[2] = True
    if symbol == key.D:
        WASD[3] = True
    if symbol == key.SPACE:
        jump()

@window.event
def on_key_release(symbol, modifiers):
    global WASD
    if symbol == key.W:
        WASD[0] = False
    if symbol == key.A:
        WASD[1] = False
    if symbol == key.S:
        WASD[2] = False
    if symbol == key.D:
        WASD[3] = False

@window.event
def on_draw():
    try:
        window.clear()
        gl.glClearColor(67 / 255.0, 166 / 255.0, 209 / 255.0, 1.0)  # Sky color
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        playerMovement()
        render()
    except Exception as e:
        print(f"Error in on_draw: {e}")
        pyglet.app.exit()  # Exit the app if an error occurs

createMeshes()
pyglet.app.run()