import pyglet
from pyglet.window import key
from pyglet import gl
import math

# Window setup
WIDTH, HEIGHT = 600, 400
window = pyglet.window.Window(WIDTH, HEIGHT, "Riptide")

# Camera parameters (start the camera at a position to see objects)
_cam = [0, 0, -10]  # Position the camera further back to see the objects

# A simple cube for testing
cube = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Back face
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]       # Front face
]

# Define which vertices form each face
faces = [
    [0, 1, 2, 3],  # Back face
    [4, 5, 6, 7],  # Front face
    [0, 1, 5, 4],  # Bottom face
    [2, 3, 7, 6],  # Top face
    [1, 2, 6, 5],  # Right face
    [0, 3, 7, 4],  # Left face
]

# Projection
def project(point):
    # Simple orthogonal projection for now
    x, y, z = point[0], point[1], point[2]
    scale = 20
    xi = x * scale / (z + 10)  # Perspective correction
    yi = y * scale / (z + 10)
    return xi + WIDTH // 2, yi + HEIGHT // 2

def draw_cube():
    # Draw each face of the cube
    for face in faces:
        screen_points = []
        for idx in face:
            point = cube[idx]
            # Apply camera transformation
            point[0] += _cam[0]
            point[1] += _cam[1]
            point[2] += _cam[2]
            ci = project(point)
            screen_points.append(ci[0])
            screen_points.append(ci[1])
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v2f', sum(screen_points, [])),
                             ('c3B', [255, 0, 255] * 4))  # Draw in magenta

@window.event
def on_draw():
    window.clear()
    gl.glClearColor(67 / 255.0, 166 / 255.0, 209 / 255.0, 1.0)  # Sky color
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    draw_cube()

@window.event
def on_key_press(symbol, modifiers):
    global _cam
    if symbol == key.W:
        _cam[2] += 1  # Move the camera closer to the object
    elif symbol == key.S:
        _cam[2] -= 1  # Move the camera further away

pyglet.app.run()