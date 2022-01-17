import numpy as np
from pyglet.gl import *
from object import Object
from bspline import Bspline

window = pyglet.window.Window(1280, 720)


def bspline_approximation(bspline, t, i):
    T_3 = np.array([t ** 3, t ** 2, t, 1])
    B_i3 = 1 / 6 * np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
    R_i = np.array([bspline.vertices[i - 1], bspline.vertices[i], bspline.vertices[i + 1], bspline.vertices[i + 2]])
    return T_3 @ B_i3 @ R_i


def bspline_tangent(bspline, t, i):
    T_2 = np.array([t ** 2, t, 1])
    B_i3 = 0.5 * np.array([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]])
    R_i = np.array([bspline.vertices[i - 1], bspline.vertices[i], bspline.vertices[i + 1], bspline.vertices[i + 2]])
    return T_2 @ B_i3 @ R_i


def rotation(start, end):
    ax = np.cross(start, end)
    cos_theta = (start @ end) / (np.linalg.norm(start) * np.linalg.norm(end))
    theta = np.rad2deg(np.arccos(cos_theta))
    return ax, theta


def draw_curve(bspline):
    glBegin(GL_LINE_STRIP)
    glColor3f(0.0, 1.0, 1.0)
    for i in range(len(bspline.vertices) - 2):
        for t in np.arange(0, 1, 0.05):
            p_i = bspline_approximation(bspline, t, i)
            dp_i = bspline_tangent(bspline, t, i)
            p_i /= bspline.scale
            glVertex3f(*p_i)
            dp_i /= 1.5 * bspline.scale
            p_i += dp_i
            glVertex3f(*p_i)
    glEnd()


def draw_object(object):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 1.0)
    for polygon in object.polygons:
        for vertex_id in polygon:
            glVertex3f(*object.vertices[vertex_id - 1])
    glEnd()


def update(x, dt):
    global t, i

    t += 0.1

    if t > 1.0:
        t -= t
        i += 1

    if i >= (len(my_bspline.vertices) - 2):
        i -= i


def set_parameters():
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50, 1280.0 / 720.0, 0.1, 1000)
    gluLookAt(1, 1, 1, -1.5, -1.5, 0, 0, .2, .9)
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()


@window.event
def on_draw():
    set_parameters()

    bspline_vertex = bspline_approximation(my_bspline, t, i)
    tangent = bspline_tangent(my_bspline, t, i)
    axis, theta = rotation(np.array([0, 0, 1]), tangent)

    draw_curve(my_bspline)

    bspline_vertex /= my_bspline.scale
    glTranslatef(*bspline_vertex)
    glScalef(1 / 6, 1 / 6, 1 / 6)
    glRotatef(theta, *axis)

    draw_object(my_obj)


if __name__ == "__main__":
    t = i = 0

    my_bspline = Bspline('bspline.txt')
    my_obj = Object('bird.obj')

    pyglet.clock.schedule(update, 1 / 20.0)
    pyglet.app.run()
