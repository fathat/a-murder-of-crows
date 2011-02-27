import physics
import pyglet
import graphics
import math
from pyglet.sprite import Sprite

class Crate(physics.Polygon):
    
    def __init__(self, world, location, box_size=1.5 ):
        self.vertices = [(-box_size, -box_size),
                          (box_size, -box_size),
                          (box_size,  box_size),
                          (-box_size,  box_size)]
        self.box_size = box_size
        physics.Polygon.__init__(self, physics.PolygonDef(world, self.vertices, density=0.05, restitution=0.5))
        self.body.position = location
        self.texture = pyglet.resource.texture('data/crate.png')

    def draw(self):
        gl = pyglet.gl.gl
        v = self.vertices
        texture = self.texture
        gl.glEnable(texture.target)        # typically target is GL_TEXTURE_2D
        gl.glBindTexture(texture.target, texture.id)
        gl.glColor4f(1,1,1,1)
        gl.glPushMatrix()
        gl.glTranslatef(self.body.position.x, self.body.position.y, 0)
        gl.glRotatef(graphics.degree(self.body.angle), 0, 0, 1)
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2f(0, 0)
        gl.glVertex2f(v[0][0], v[0][1])
        gl.glTexCoord2f(1, 0)
        gl.glVertex2f(v[1][0], v[1][1])
        gl.glTexCoord2f(1, 1)
        gl.glVertex2f(v[2][0], v[2][1])
        gl.glTexCoord2f(0, 1)
        gl.glVertex2f(v[3][0], v[3][1])
        gl.glEnd()
        gl.glPopMatrix()
        
        gl.glDisable(texture.target)
