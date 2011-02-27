import pyglet
import math

def radian(degree):
    return degree*(math.pi/180.0)
    
def degree(rad):
    return rad*(180.0/math.pi)

def draw_wedge(batch, x, y, angle, size):
    rad = angle
    rad2 = angle+radian(120)
    rad3 = angle+radian(240)
    ax, ay = size*math.cos(rad), size*math.sin(rad)
    bx, by = size*math.cos(rad2), size*math.sin(rad2)
    cx, cy = size*math.cos(rad3), size*math.sin(rad3)
    batch.add_indexed(3,
                pyglet.gl.GL_TRIANGLES,
                None,
                [0, 1, 2],
                ('v2f',
                   (x+ax, y+ay,
                    x+bx, y+by,
                    x+cx, y+cy)))

def draw_polygon(vertices):
    gl = pyglet.gl.gl
    gl.glBegin(gl.GL_POLYGON)
    for v in vertices:
        gl.glVertex2f(v.x, v.y, 0)
    gl.glEnd()


def draw_circle(x, y, radius, angle):
    GL = pyglet.gl.gl
    GL.glPushMatrix()
    GL.glTranslatef(x, y, 0)
    GL.glRotatef(angle * (180/math.pi), 0, 0, 1)
    GL.glBegin(GL.GL_POLYGON)
    for i in xrange(0, 360, 20):
        r = i * (math.pi/180.0)
        GL.glVertex2f(math.cos(r)*radius, math.sin(r)*radius)
    GL.glEnd()
    
    #GL.glBegin(GL.GL_LINE_STRIP)
    #GL.glVertex2f(0, 0)
    #GL.glVertex2f(0, radius)
    #GL.glEnd()
    GL.glPopMatrix()

def draw_circle_shape(s):
    draw_circle(s.GetBody().position.x, s.GetBody().position.y, s.radius, s.GetBody().angle)

def draw_body(body):
    pass