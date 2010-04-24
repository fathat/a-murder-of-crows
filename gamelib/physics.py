import pyglet
import graphics
import Box2D as box2d
import math

print box2d.b2_maxPairs

class MyVeryOwnContactListener(box2d.b2ContactListener):
    def Add(self, point):
        print 'adding ', point

class PolygonDef(object):
    def __init__(self, world, vertices, density=1.0, friction=0.3, restitution=0.1,  texture=None):
        self.world = world
        self._vertices = vertices
        self._display_list = None
        self._texture = None
        if texture:
            self._texture = pyglet.resource.texture(texture)
        
        
        sd = box2d.b2PolygonDef()
        sd.vertexCount = len(vertices)
        i = 0
        for v in vertices:
            sd.setVertex(i, v[0], v[1])
            i += 1
        sd.density = density
        sd.friction = friction
        sd.restitution = restitution
        self.shape_def = sd
        
    def draw(self, instance):
        
        gl = pyglet.gl.gl
        
        gl.glPushMatrix()
        gl.glTranslatef(instance.body.position.x, instance.body.position.y, 0)
        gl.glRotatef(graphics.degree(instance.body.angle), 0, 0, 1)
        
        if not self._display_list:
            self._display_list = gl.glGenLists(1)
            gl.glNewList(self._display_list, gl.GL_COMPILE)
            
            if self._texture:
                gl.glEnable(self._texture.target)        # typically target is GL_TEXTURE_2D
                gl.glBindTexture(self._texture.target, self._texture.id)
                gl.glColor4f(1,1,1,1)
            
            gl.glBegin(gl.GL_POLYGON)
            for v in self._vertices:
                if self._texture:
                    gl.glTexCoord2f(v[2], v[3])
                gl.glVertex2f(v[0], v[1])
            gl.glEnd()
            
            if self._texture:
                gl.glDisable(self._texture.target)        # typically target is GL_TEXTURE_2D
            #pyglet.graphics.draw_indexed(
            #        len(self._vertices)//2,
            #        pyglet.gl.GL_POLYGON,
            #        range(len(self._vertices)//2),
            #        ('v2f', self._vertices))
            gl.glEndList()
        
        gl.glCallList(self._display_list)
        gl.glPopMatrix()


class Polygon(object):
    def __init__(self, definition, position=(0,0), angle=0, has_mass=True):
        
        self.definition = definition
        bd=box2d.b2BodyDef() 
        bd.position = position
        bd.angle = angle
        #bd.linearDamping = 0
        #bd.angularDamping = 0
        
        self.body = definition.world.CreateBody(bd) 
        self.body.CreateShape(definition.shape_def)
        if has_mass:
            self.body.SetMassFromShapes()
    
    def update(self, dt):
        pass
    
    def draw(self):
        self.definition.draw(self)
        

class CircleDef(object):
    def __init__(self, world, radius, density=1.0, friction=0.3):
        self.world = world
        self._display_list = None
        
        sd = box2d.b2CircleDef()
        sd.radius = radius
        sd.density = density
        sd.friction = friction
        self.shape_def = sd
        
    def draw(self, instance):
        
        gl = pyglet.gl.gl
        
        gl.glPushMatrix()
        gl.glTranslatef(instance.body.position.x, instance.body.position.y, 0)
        gl.glRotatef(instance.body.angle * (180/math.pi), 0, 0, 1)
        
        if not self._display_list:
            self._display_list = gl.glGenLists(1)
            gl.glNewList(self._display_list, gl.GL_COMPILE)
            
            radius = instance.body.GetShapeList()[0].radius
            
            gl.glBegin(pyglet.gl.GL_POLYGON)
            for i in xrange(0, 360, 20):
                r = i * (math.pi/180.0)
                gl.glVertex2f(math.cos(r)*radius, math.sin(r)*radius)
            gl.glEnd()
            
            #gl.glBegin(pyglet.gl.GL_LINE_STRIP)
            #gl.glVertex2f(0, 0)
            #gl.glVertex2f(0, radius)
            #gl.glEnd()
            
            gl.glEndList()
        
        gl.glCallList(self._display_list)
        gl.glPopMatrix()
        
class Circle(object):
    def __init__(self, definition, position=(0,0), angle=0):
        
        self.definition = definition
        bd=box2d.b2BodyDef() 
        bd.position = position
        bd.angle = angle
        
        self.body = definition.world.CreateBody(bd) 
        self.body.CreateShape(definition.shape_def)
        self.body.SetMassFromShapes()
    
    def update(self, dt):
        pass
    
    def draw(self):
        self.definition.draw(self)