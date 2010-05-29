import graphics
import random
import pyglet
import Box2D as box2d
import math
import physics
import settings
import spritey

def make_triangle(size):
    rad = 0
    rad2 = graphics.radian(120)
    rad3 = graphics.radian(240)
    ax, ay = size*math.cos(rad), size*math.sin(rad)
    bx, by = size*math.cos(rad2), size*math.sin(rad2)
    cx, cy = size*math.cos(rad3), size*math.sin(rad3)
    return [(ax, ay), (bx, by), (cx, cy)]

class Murder(object):
    def __init__(self, world):
        self.world_context = world
        if settings.crow_shape == 'triangle':
            self.crow_shape_def = physics.PolygonDef(world.world, make_triangle(settings.crow_size))
        else:
            self.crow_shape_def = physics.CircleDef(world.world, settings.crow_size)
        self.crows = []
        self.batch = pyglet.graphics.Batch()
    
    def add_crow(self, target):
        crow = Crow(self, abs(random.random()) *settings.world_width, abs(random.random())*(settings.world_height/4) + settings.world_height)
        crow.target = target
        self.crows.append(crow)
    
    def update(self, dt):
        for crow in self.crows:
            crow.update(dt)
    
    def draw(self):
        gl = pyglet.gl.gl
        gl.glColor4f(0, 0, 0, 1)
        batch = pyglet.graphics.Batch()
        for crow in self.crows:
            crow.draw(batch)
        batch.draw()
        pyglet.gl.gl.glColor4f(0, 0, 0, 1)
        #self.batch.draw()

class Crow(object):
    def __init__(self, murder, x, y):
        self.size = settings.crow_size
        self.anim = 0
        self.murder = murder
        self.target = None
        self.phys_object = physics.Polygon(murder.crow_shape_def, (x,y) )
        #self.phys_object.body.SetBullet(True)
        self.phys_object.body.userData = self
        self.phys_object.body.massData.mass *= 2
        self.life = 50
        self.speed = settings.crow_idle_speed
        self.blood_lust = 0
        self.resting = False
        self.sprite = spritey.Spritey('data/characters/crow.png', self.phys_object.body, settings.crow_size)
    
    def on_hit(self, contact):
        pass
    
    def on_remove_hit(self, contact):
        pass
    
    def damage(self, contact):
        from person import Person
        if isinstance(contact.shape1.GetBody().userData, Person) or isinstance(contact.shape2.GetBody().userData, Person):
            self.blood_lust = 1.5
            self.resting = True
            self.target = None#box2d.b2Vec2(settings.world_width*random.random(), settings.world_height-(random.random()*settings.world_height*0.3))
            self.speed = settings.crow_idle_speed
    
    def moveTowards(self, x, y):
        if not self.resting: 
            self.target = box2d.b2Vec2(x, y)
    
    def update(self, dt):
        #limit speed
        self.blood_lust -= dt
        if self.blood_lust > 0:
            self.phys_object.body.ApplyTorque(self.blood_lust*80)
        else:
            self.blood_lust = 0
            self.resting = False
        velocity = self.phys_object.body.GetLinearVelocity()
        if velocity.Length() > self.speed:
            velocity.Normalize()
            velocity = velocity*self.speed
            self.phys_object.body.SetLinearVelocity(velocity)
        self.anim += dt
        if self.target:
            nose = self.phys_object.body.GetWorldPoint((0, -self.size))
            
            #self.phys_object.body.SetLinearVelocity( (self.target - self.phys_object.body.position)*40)
            self.phys_object.body.ApplyForce( (self.target - self.phys_object.body.position)*settings.crow_speed, nose)
            #print self.phys_object.body.GetLinearVelocity().Length()
            
        #figure out angle to target
        if self.target:
            body = self.phys_object.body
            v = (body.position - self.target)
            v.Normalize()
            self.sprite.angle = math.atan2(v.y, v.x)
        else:
            self.sprite.angle = None
    
    def draw(self, batch):
        gl = pyglet.gl.gl
        
        gl.glColor4f(0,0,0,1)
        self.phys_object.draw()
        gl.glEnable (gl.GL_BLEND)
        gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        if self.blood_lust > 0:
            gl.glColor4f(self.blood_lust, 0,0, 1-self.blood_lust*0.25)
        else:
            gl.glColor4f(1,1,1,1)
        self.sprite.draw()
        gl.glDisable(gl.GL_BLEND)
        
