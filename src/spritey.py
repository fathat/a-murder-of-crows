import physics
import pyglet
import graphics
import math

class Spritey(physics.Polygon):
    
    def __init__(self, texture_filename, body, size):
        self.vertices = [(-size, -size),
                          (size, -size),
                          (size,  size),
                          (-size,  size)]
        self.size = size
        self.body = body
        self.angle = None
        self.texture = pyglet.resource.texture(texture_filename)

    def draw(self):
        gl = pyglet.gl.gl
        v = self.vertices
        texture = self.texture
        gl.glEnable(texture.target)        # typically target is GL_TEXTURE_2D
        gl.glBindTexture(texture.target, texture.id)
        gl.glPushMatrix()
        gl.glTranslatef(self.body.position.x, self.body.position.y, 0)
        if self.angle:
            angle = self.angle
        else:
            angle = self.body.angle
        gl.glRotatef(graphics.degree(angle), 0, 0, 1)
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
        #pyglet.gl.gl.glColor4f(.5, .5, .2, 1)
        #super(Crate, self).draw()
