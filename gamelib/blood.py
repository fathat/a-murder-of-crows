#!/usr/bin/env python
import pyglet
import settings
import Box2D as box2d
import random

class BloodParticle(object):
    def __init__(self, p, t):
        self.p = p
        self.lp = p+box2d.b2Vec2(0, 0.1)
        self.t = t
    
    def color(self):
        t = max(self.t, 0)
        return [1*t, 0, 0, t]
    
        
    def update(self, dt):
        self.t -= dt
        self.lp = box2d.b2Vec2(self.p)
        self.p.y -= dt*20*settings.scale
        
    def draw_batch(self, batch):
        if not settings.draw_blood: return
        gl = pyglet.gl.gl
        t = max(self.t, 0)
        batch.add(1,
                  gl.GL_POINTS,
                  None,
                  ('v2f', (self.p.x, self.p.y)),
                  ('c4f', (t,0,0,t)))


class BloodFountain(object):
    interval = 0.07
    max_life = 10
    def __init__(self, body, person):
        self.body = body
        self.blood = []
        self.person = person
        self.delay = self.interval
        self.life = 5
    
    def update(self, dt):
        self.delay -= dt
        if self.person.is_dead: self.life -= dt
        self.life = max(0, self.life)
        if self.delay <= 0 and self.life > 0:
            self.delay = self.interval
            p = box2d.b2Vec2(self.body.GetWorldCenter())
            p.x += random.random()*5* settings.scale
            self.blood.append(BloodParticle(p, 1))
        for b in self.blood:
            b.update(dt)
        self.blood = [x for x in self.blood if x.t > 0]
        
    def draw(self):
        if not settings.draw_blood: return
        gl = pyglet.gl.gl
        gl.glEnable (gl.GL_BLEND)
        gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        if len(self.blood):
            gl.glPointSize(2)
            gl.glLineWidth(2)
            gl.glBegin(gl.GL_LINE_STRIP)
            for b in self.blood:
                gl.glColor4f(*b.color())
                gl.glVertex2f(b.p.x, b.p.y)
            gl.glEnd()
    
    def draw_batch(self, batch):
        if len(self.blood) < 2:
            return
        #if not settings.draw_blood: return
        gl = pyglet.gl.gl
        p = []
        c = []
        for b in self.blood:
            p.extend([b.p.x, b.p.y])
            c.extend(b.color())
        pyglet.graphics.draw(len(self.blood),
                  gl.GL_LINE_STRIP,
                  ('v2f', p),
                  ('c4f', c))
        
