from __future__ import with_statement
import pyglet
from pprint import pprint
import Box2D as box2d
from Box2D import b2Vec2
from camera import Camera, Projection
from context import BaseContext
from crow import Murder, Crow
from crate import Crate
from person import Person
import physics
import random
import person
import settings
import math
import gamestats
import tweak
import squirtle

try:
    import psyco
    psyco.full()
except:
    pass

from weather import Weather

def decrow(e1, e2, cls):
    if isinstance(e1, cls):
        return e1
    elif isinstance(e2, cls):
        return e2
    return None
    
class ContactListener(box2d.b2ContactListener):
    
    def Add(self, point):
        e1 = point.shape1.GetBody().userData
        e2 = point.shape2.GetBody().userData
        crow, person = decrow(e1, e2, Crow), decrow(e1, e2, Person)
        if e1: e1.on_hit(point)
        if e2: e2.on_hit(point)
    
    def Remove(self, point):
        e1 = point.shape1.GetBody().userData
        e2 = point.shape2.GetBody().userData
        if e1: e1.on_remove_hit(point)
        if e2: e2.on_remove_hit(point)
    
    def Persist(self, point):
        e1 = point.shape1.GetBody().userData
        e2 = point.shape2.GetBody().userData
        crow = decrow(e1, e2, Crow)
        person = decrow(e1, e2, Person)
        if crow and person:
            if point.velocity.Length() < 10*settings.scale:
                e1.damage(point)
                e2.damage(point)

class WinContext(BaseContext):
    def __init__(self, window):
        BaseContext.__init__(self, "WinContext")
        self.window = window
        self.labels = []
        
    
    def on_activate(self):
        window = self.window
        self.labels.append( pyglet.text.Label("""You are made of win!""",
                            font_name="Tahoma",
                            font_size=12,
                            x=window.width//2, y=window.height//2,
                            anchor_x='center', anchor_y='center',
                            color=(255, 255, 255,255)))
        self.labels.append( pyglet.text.Label("""Lives Taken: """ + str(gamestats.lives_taken),
                            font_name="Tahoma",
                            font_size=12,
                            x=window.width//2, y=window.height//2-20,
                            anchor_x='center', anchor_y='center',
                            color=(255, 255, 255,255)))
        self.labels.append( pyglet.text.Label("""Limbs Consumed: """ + str(gamestats.limbs_taken),
                            font_name="Tahoma",
                            font_size=12,
                            x=window.width//2, y=window.height//2-40,
                            anchor_x='center', anchor_y='center',
                            color=(255, 255, 255,255)))
        
        self.labels.append( pyglet.text.Label("""Survivors: """ + str(gamestats.survivors),
                            font_name="Tahoma",
                            font_size=12,
                            x=window.width//2, y=window.height//2-60,
                            anchor_x='center', anchor_y='center',
                            color=(255, 255, 255,255)))
    
    def draw_ui(self):
        for x in self.labels:
            x.draw()
        
class MapContext(BaseContext):
    song = 'data/music/surfin_bird.mp3'
    level_data = 'data/level_.svg'
    
    def __init__(self, window, name):
        BaseContext.__init__(self, name)
        self.window = window
        self.camera = Camera(window, self)
        self.camera.look_at = (64, 32)
        self.mouse_down = False
        self.init_world()
        self.time = 0
        self.spawn_countdown = 6
        self.spawn_rate = 1
        self.spawn_time = 10
        self.average_speed = tweak.average_speed
        self.bg = pyglet.resource.image('data/bg/city_burning.jpg')
        
    
    def on_activate(self):
        if settings.music:
            self.music = pyglet.resource.media(self.song)
            self.music = self.music.play()
    
    def init_world(self):
        self.svg = squirtle.SVG(self.level_data, invert_y=True)
        self.world_width = self.svg.width * settings.scale * settings.svgscale
        self.world_height = self.svg.height * settings.scale * settings.svgscale
        self.init_physics()
        self.murder = Murder(self)

        for i in range(settings.crow_count):
            self.murder.add_crow(box2d.b2Vec2(random.random()*self.world_width, random.randint(int(self.world_height*1.2), int(self.world_height*1.5))))
    
    def init_physics(self):
        # Box2D Initialization
        self.worldAABB = box2d.b2AABB()
        self.worldAABB.lowerBound = (-self.window.width*4, -self.window.height*4)
        self.worldAABB.upperBound = (self.window.width*8, self.window.height*8)
        gravity = (0.0, -21.0)
        
        doSleep = True
        self.contact_listener = ContactListener()
        self.world = box2d.b2World(self.worldAABB, gravity, doSleep)
        self.world.SetContactListener(self.contact_listener)
        self.build_map_container()
        self.build_ground()
        self.build_objects()        
        self.weather = Weather(self)
        
    def build_map_container(self):
        bd=box2d.b2BodyDef() 
        sd=box2d.b2PolygonDef()
        bd.position = (self.world_width//2, self.world_height//2)
        self.container = self.world.CreateBody(bd)
        
        sd.SetAsBox(self.world_width, 10.0*settings.scale, box2d.b2Vec2(0, -self.world_height/2-5*settings.scale), 0 )
        self.container.CreateShape(sd)
        
        #top?
        #sd.SetAsBox(settings.world_width, 10.0*settings.scale, box2d.b2Vec2(0, settings.world_height/2+5*settings.scale), 0 )
        #self.container.CreateShape(sd)
        
        sd.SetAsBox(10.0*settings.scale, self.world_width, box2d.b2Vec2(self.world_width/2+5*settings.scale, 0), 0 )
        self.container.CreateShape(sd)
        
        sd.SetAsBox(10.0*settings.scale, self.world_width, box2d.b2Vec2(-self.world_width/2-5*settings.scale, 0), 0 )
        self.container.CreateShape(sd)
    
    def build_ground(self):        
        def make_edge(svgpath):
            r = []
            #print svgpath.transform
            #if not svgpath.id.startswith('ground'): return None
            for loop in svgpath.path:
                bd = box2d.b2BodyDef()
                bd.position = (0,0)
                sd = box2d.b2EdgeChainDef()
                data = [svgpath.transform((x[0], x[1])) for x in list(reversed(loop))]
                data = [(x[0]*settings.scale, x[1]*settings.scale) for x in data]
                #pprint(data)
                sd.setVertices(data)
                sd.isALoop = False
                sd.density = 1.0
                sd.friction = 1.75
                sd.restitution = 0.1
                body = self.world.CreateBody(bd)
                shape = body.CreateShape(sd)
                r.append((body,shape))
            return r

        self.ground = [make_edge(x) for x in self.svg.paths]
    
    def build_objects(self):
        #cd = physics.CircleDef(self.world, 3.0, density=0.2)
        self.things = [Crate(self.world, (105, 60)),
                       Crate(self.world, (105, 65)),
                       Crate(self.world, (110,  60)),
                       Crate(self.world, (115, 60))]
        self.people = []
    
    def on_key_press(self, symbol, modifiers):
        pass

    def focus_crows(self, x, y):
        pass
        
    
    def on_mouse_scroll(self, x, y, sx, sy):
        self.camera.zoom_by(sy*0.5)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button != 1: return
        self.mouse_down = True
        speed = settings.crow_fast_speed
        wx, wy = self.camera.pixel_to_world(x, y)
        self.mx, self.my = wx, wy
        #self.camera.zoom_target = 1.5/settings.scale
        #self.camera.zoom_rate = 7.5
        for crow in self.murder.crows:
            crow.resting = False
            crow.speed = speed
            crow.moveTowards(random.random() * 4 + wx, random.random() * 4 + wy )

    def on_mouse_release(self, x, y, button, modifiers):
        if button == 1:
            wx, wy = self.camera.pixel_to_world(x, y)
            for crow in self.murder.crows:
                crow.resting = False
                crow.target = box2d.b2Vec2(
                                random.randint(int(wx)-3, int(wx)+3),
                                self.world_height*1.2)
                crow.speed = settings.crow_idle_speed
            #self.camera.zoom_target = 0.75/settings.scale
            #self.camera.zoom_rate = 7.5
        self.mouse_down = False
    
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if button == 1:
            wx, wy = self.camera.pixel_to_world(x, y)
            self.mx, self.my = wx, wy
            for crow in self.murder.crows:
                crow.moveTowards(random.random() + wx, random.random() + wy )
        else:
            self.camera.move_by(-dx, -dy)
    
    @property
    def width(self): return self.worldAABB.upperBound.x
    
    @property
    def height(self): return self.worldAABB.upperBound.y
    
    def spawn_enemies(self, dt):
        self.spawn_countdown -= dt
        if self.spawn_countdown <= 0:
            self.spawn_countdown = self.spawn_time
            if self.spawn_countdown < 3.5: self.spawn_countdown = 3.5
            self.average_speed += 0.2
            self.spawn_time -= 0.15
            if self.spawn_time < 2: self.spawn_countdown = 2
            for x in range(int(self.spawn_rate)):
                self.people.append(person.Person(self.world, (x*2, 70), self.average_speed + random.random()))
            self.spawn_rate += 0.15
            print "Spawn Countdown:", self.spawn_countdown,
            print ", Spawn Rate:", self.spawn_rate,
            print ", Average Speed:", self.average_speed
    
    def update(self, dt):
        if self.time >= 140:
            self.switch_requested("WinContext")
        
        self.time += dt
        self.spawn_enemies(dt)
        for thing in self.things:
            thing.update(dt)
        people_to_remove = []
        for person in self.people:
            person.update(dt)
            if len(self.people) > settings.max_people and len(person.joints) <= 3:
                people_to_remove.append(person)
            elif person.Chest.position.x >= self.world_width - 2 and not person.is_dead:
                person.remove_from_world()
                gamestats.add_survivor()
        
        #Only remove one of the People To Remove
        if len(people_to_remove):
            people_to_remove[-1].remove_from_world()
            self.people.remove(people_to_remove[-1])
        
        if self.mouse_down:
            d = (b2Vec2(self.mx, self.my) - self.camera.look_at).Length()
            self.camera.move_towards(self.mx, self.my, max(d, 2), dt)
        
        self.murder.update(dt)
        self.weather.update(dt)
        self.camera.update(dt)
        self.world.SetContinuousPhysics(True)
        
        # Tell Box2D to step
        if dt > .1: dt = .1
        self.world.Step(dt, 10, 10)
        self.world.Validate()
    
    def predraw(self): pass

    def draw(self):
        with Projection(self.camera) as projection:
            self.weather.draw_background()
            self.svg.draw(0,0, 0, 0, settings.scale*settings.svgscale)
            pyglet.gl.gl.glColor4f(0,0,0,1)

            self.murder.draw()
            for thing in self.things:
                thing.draw()
            for person in self.people:
                person.draw()
            self.weather.draw_foreground()
        