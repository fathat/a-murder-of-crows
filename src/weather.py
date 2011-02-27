import pyglet
import random
import settings
import math

class FogParticle(object):
    def __init__(self, mapcontext, img, batches):
        self.mapcontext = mapcontext
        self.sprite = pyglet.sprite.Sprite(img, batch=random.choice(batches))
        self.multiplier = 1
        self.remake()
        self.life = 0#abs(random.random())*self.max_life
        self.sprite.opacity = 0#self.life*10
        
    
    def remake(self):
        self.sprite.set_position(abs(random.random()) * self.mapcontext.world_width-self.sprite.image.width*0.5*self.sprite.scale*settings.scale,
                                 abs(random.random()) * self.mapcontext.world_height- self.sprite.image.height*0.5*self.sprite.scale*settings.scale)
        self.sprite.scale = (abs(random.random())+1) * settings.scale * 3
        self.max_life = (random.random() + 1) * 8
        self.life = 0
        self.sprite.opacity = self.life*4
        
    def update(self, dt):
        self.life += (dt * 4) * self.multiplier
        self.sprite.opacity = self.life*3
        if self.life > self.max_life:
            self.multiplier *= -1
        if self.life < 0:
            self.remake()
            self.multiplier *= -1
        
class Weather(object):
    
    def __init__(self, mapcontext):
        img = pyglet.resource.image('data/particles/fog.png')
        
        self.foreground_batch = pyglet.graphics.Batch()
        self.background_batch = pyglet.graphics.Batch()
        batches = [
            #self.foreground_batch,
            self.background_batch,
            self.background_batch,
            self.background_batch
        ]
        
        self.particles = []
        num_particles = int(settings.world_width*1.25)
        print "Fog Particles:", num_particles
        for i in xrange(num_particles):
            p = FogParticle(mapcontext, img, batches)
            self.particles.append(p)
        
    def update(self, dt):
        for p in self.particles:
            p.update(dt)
    
    def draw_foreground(self):
        self.foreground_batch.draw()
        
    def draw_background(self):
        self.background_batch.draw()