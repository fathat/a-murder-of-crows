from mapcontext import MapContext
import pyglet
from crow import Murder, Crow
import Box2D as box2d
import random
import settings
import physics
from person import Person
from crate import Crate

class MenuContext(MapContext):
    song = 'data/music/whistling.mp3'
    ground_data = [
          [(0,  0, 0, 0), (20, 0, 0.1, 1), (30, 20, 0.8, 1), (0, 20, 0, 1)],
          [(30, 0, 0, 0), (100, 0, 4, 0), (100, 12, 4, 1), (60, 12, 2, 1)],
          [(0, 0, 0, 0.5), (settings.world_width, 0, 7, 0.5), (settings.world_width, 8, 7, 1), (0, 8, 0, 1)]]
    
    def __init__(self, window):
        MapContext.__init__(self, window, "MenuContext")
        self.window = window
        img = pyglet.resource.image("data/menu/logo.png")
        
        self._title = pyglet.sprite.Sprite(img,
                                           self.window.width//2-img.width/2,
                                           self.window.height//2-img.height/2+100)
        
        self._instructions = pyglet.text.Label("""""",
                            font_name=settings.font,
                            font_size=12,
                            x=window.width//2, y=window.height-200,
                            anchor_x='center', anchor_y='center',
                            color=(255, 255, 255,255),
                            width=300,
                            multiline=True)
        
        
        self._start = pyglet.text.Label('Press the space key to continue',
                            font_name='Tahoma',
                            font_size=18,
                            x=window.width//2, y=window.height//2,
                            anchor_x='center', anchor_y='center',
                            color=(0, 0, 0, 128))
        self.stage = 0
        self.on_activate()    

    def build_objects(self):
        self.things = [Crate(self.world, (20, 20)),
                       Crate(self.world, (70, 12)),]
        self.people = []

        
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q:
            try:
                self.music.pause()
            except:
                pass
            self.switch_to("MapContext")

        if symbol != pyglet.window.key.SPACE:
            return
        self.stage += 1    
        if self.stage == 1:
            self._title.visible = False
            self._start = None
            self._instructions.text = "(A short tutorial)\n\n[Press space to continue]\n\n[Press Q to skip]"
        elif self.stage == 2:
            self._instructions.text = "Hold down [Left Mouse] to direct the murder of crows to fly to an area.\n\n Try it now.\n\nWhen you release the button the crows will disperse.\n\n[Press space to continue]"
        elif self.stage == 3:
            self._instructions.text = "Often it's useful to move objects around the environment with your murder of crows.\n\nTry moving the crates around.\n\n[Press space to continue]"
        elif self.stage == 4:
            self.man = Person(self.world, box2d.b2Vec2(4, 20))
            
            self.people.append(self.man)
            self._instructions.text = "Look!\n\nA person.\n\nThe goal of the game is to eat as many of these as possible\n\nThey do not want to be eaten and they will run away\n\n[Press space to continue]"
            self.man.speed = .6
        elif self.stage == 5:
            self._instructions.text = "Hold Left-Click over the man to instruct your crows to feed on him\n\n[Press space when you've finished feeding your murder]"
        else:
            self._instructions.text = "[Press Q to continue to the next level]"
    
    def spawn_enemies(self, dt):
        if self.stage < 6:
            return
        self.spawn_countdown -= dt
        if self.spawn_countdown <= 0:
            self.spawn_countdown = 6
            for x in range(int(self.spawn_rate)):
                self.people.append(Person(self.world, (x*2, 30), 3+random.random()))
    
    def draw_ui(self):
        self._title.draw()
        self._instructions.draw()
        if self._start:
            self._start.draw()
