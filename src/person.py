import physics
import Box2D as box2d
import pyglet
import math
import graphics
import settings
import random
import crow
import gamestats
from ragdoll import RagdollDef
from blood import BloodParticle, BloodFountain

Crow = crow.Crow

class Person(object):
    
    def __init__(self, world, position, speed=0):
        self.world = world
        self.bodies = {}
        self.speed = speed
        self.marked_dead = False
        
        RagdollDef().CreateBodiesOn(self, world, position)
        
        self.time = random.random()
        self.joint_loss_cooldown = None
        for x in self.bodies.values():
            x.userData = self
        self.hit_count = 0
        self.blood = []
        self.blood_fountains = {}
        
    def remove_from_world(self):
        for j in self.joints:
            self.world.DestroyJoint(j)
        
        for b in self.bodies.values():
            self.world.DestroyBody(b)
            
        self.blood = []
        self.blood_fountains = {}
        
        self.joints = []
        self.bodies = {}
    
    def try_add_blood(self, contact):
        if isinstance(contact.shape1.GetBody().userData, Crow) or isinstance(contact.shape2.GetBody().userData, Crow):
            p = box2d.b2Vec2(contact.position.x, contact.position.y)
            if len(self.blood) > settings.max_blood:
                self.blood.pop()
            for i in xrange(1):
                m = p + box2d.b2Vec2(random.random(), random.random())
                self.blood.insert(0, BloodParticle(m, 1))
            
    def on_hit(self, contact):
        self.hit_count += 1
        self.try_add_blood(contact)
        
    
    def on_remove_hit(self, contact):
        self.hit_count -= 1
    
    def damage(self, contact):
        if not self.is_dying: #and contact.velocity.Length() > 0.5:
            self.try_add_blood(contact)
            if self.joint_loss_cooldown == None:
                self.joint_loss_cooldown = 0.05 + abs(random.random()*0.05)
            #if contact.velocity.Length() > 0.5:
            #    self.joint_loss_cooldown = 0
    
    
    def walk(self, dt):
        if self.is_dying: self.joint_loss_cooldown -= dt
        if len(self.joints) > 8:
            self.Head.ApplyForce(box2d.b2Vec2(self.speed*1, 50-self.speed*2), self.Head.position)
        if len(self.joints) >= 8:
            self.Pelvis.ApplyForce(box2d.b2Vec2(self.speed*0.5, 5), self.Pelvis.position)
            self.Chest.ApplyForce(box2d.b2Vec2(self.speed*1, 50-self.speed*2), self.Chest.position)
        
        if int(self.time) % 2 == 0:
            polarity = -1
        else:
            polarity = 1
            
        if len(self.joints) >= 8:
            self.RThigh.ApplyTorque(polarity*20*self.speed)
            self.LThigh.ApplyTorque(-polarity*20*self.speed)
            self.LFoot.ApplyImpulse(box2d.b2Vec2(0, min(0, -polarity)), self.LFoot.GetWorldPoint(box2d.b2Vec2(1, 0)))
            self.RFoot.ApplyImpulse(box2d.b2Vec2(0, min(0, polarity)), self.RFoot.GetWorldPoint(box2d.b2Vec2(1, 0)))

        if len(self.joints) >= 8:
            self.LHand.ApplyForce(box2d.b2Vec2(-polarity, 0), self.LHand.GetWorldPoint(box2d.b2Vec2(1, 0)))
            self.RHand.ApplyForce(box2d.b2Vec2(polarity, 0), self.RHand.GetWorldPoint(box2d.b2Vec2(1, 0)))
    
    def update(self, dt):
        self.time += dt*self.speed
        self.walk(dt)
        
        if self.is_dying and self.joint_loss_cooldown <= 0 and len(self.joints):
            self.joint_loss_cooldown = None
            j = self.joints.pop()
            b1 = j.GetBody1()
            b2 = j.GetBody2()
            self.world.DestroyJoint(j)
            gamestats.add_limb()
            self.blood_fountains[b2] = BloodFountain(b2, self)
            if self.is_dead and not self.marked_dead:
                gamestats.add_life()
                self.marked_dead = True
        
        for body, fountain in self.blood_fountains.items():
            fountain.update(dt)
        for b in self.blood:
            b.update(dt)
        self.blood = [x for x in self.blood if x.t > 0]
    
    @property
    def is_dying(self):
        return self.joint_loss_cooldown != None
    
    @property
    def is_dead(self):
        return len(self.joints) < 9

    def draw(self):
        gl = pyglet.gl.gl
        if self.is_dying:
            gl.glColor4f(.9, .7, .6, 1)
            pass
        else:
            gl.glColor4f(.9, .7, .6, 1)
        for value in self.bodies.values():
            shape = value.GetShapeList()[0]
            if shape.GetType() == 0:
                self.draw_circle(shape)
            else:
                self.draw_poly(shape)
        
        
        if len(self.blood):
            gl.glPointSize(2)
            gl.glBegin(gl.GL_POINTS)
            for b in self.blood:
                gl.glColor4f(*b.color())
                gl.glVertex2f(b.p.x, b.p.y)
            gl.glEnd()
        
        gl.glEnable (gl.GL_BLEND)
        gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glPointSize(2)
        gl.glLineWidth(2)
        for body, fountain in self.blood_fountains.items():
            fountain.draw()
            
    def draw_head(self, poly):
        GL = pyglet.gl.gl
        GL.glPushMatrix()
        GL.glTranslatef(x, y, 0)
        GL.glRotatef(angle * (180/math.pi), 0, 0, 1)
        GL.glBegin(GL.GL_POLYGON)
        for i in xrange(0, 360, 20):
            r = i * (math.pi/180.0)
            GL.glVertex2f(math.cos(r)*radius, math.sin(r)*radius)
        GL.glEnd()
    
    def draw_poly(self, poly):
        GL = pyglet.gl.gl
        body = poly.GetBody()
        drawData = poly.userData
        if not drawData.displayList:
            drawData.displayList = GL.glGenLists(1)
            GL.glNewList(drawData.displayList, GL.GL_COMPILE)
            GL.glColor4f(*drawData.color)
            GL.glLineWidth(4.0)
            GL.glBegin(GL.GL_LINES)
            x1, y1 = poly.vertices[0]
            x2, y2 = poly.vertices[1]
            x3, y3 = poly.vertices[2]
            x4, y4 = poly.vertices[3]
            #average
            GL.glVertex2f((x1+x2)/2, (y1+y2)/2)
            GL.glVertex2f((x3+x4)/2, (y3+y4)/2)
            #for vx, vy in list(poly.vertices):
            #    GL.glVertex2f(vx, vy)
            GL.glEnd()
            GL.glEndList()
        GL.glPushMatrix()
        GL.glTranslatef(body.position.x, body.position.y, 0)
        GL.glRotatef(body.angle * (180/math.pi), 0, 0, 1)
        GL.glCallList(drawData.displayList)
        GL.glPopMatrix()
            
            
    def draw_circle(self, circle):
        graphics.draw_circle_shape(circle)
