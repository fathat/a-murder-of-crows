from common import *
from Box2D import b2Vec2
from pyglet.gl import gl
import settings

class Camera(object):
    def __init__(self, window, world):
        self._look_at = b2Vec2(0, 0)
        self._zoom = 1.0/settings.scale
        self._zoom_target = self._zoom
        self.zoom_rate = 1.0
        self.win = window
        self.world = world
    
    @Property
    def look_at():
        def fset(self, lookat):
            self._look_at = b2Vec2(lookat)
        def fget(self):
            return self._look_at
    
    @Property
    def zoom():
        def fset(self, zoom):
            self._zoom = max(0.05, zoom)
        def fget(self):
            return self._zoom
    
    @Property
    def zoom_target():
        def fset(self, zoom):
            self._zoom_target = max(0.05, zoom)
        def fget(self):
            return self._zoom_target

    def get_window(self):
        p1 = self.pixel_to_world(0, 0)
        p2 = self.pixel_to_world(self.win.width, self.win.height)
        return p1[0], p1[1], p2[0], p2[1]
        
    def set_projection(self):
        w = (self.win.width / 2) / self.zoom
        h = (self.win.height / 2) / self.zoom
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-w, w, -h, h, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslatef(-self.look_at.x, -self.look_at.y, 0)
    
    def move_by(self, dx, dy):
        self.look_at.x += dx/self.zoom
        self.look_at.y += dy/self.zoom
       
    def move_towards(self, wx, wy, speed, dt):
        w = b2Vec2(wx, wy)
        d = w - self.look_at
        current_distance = d.Normalize()
        distance_to_travel = speed*dt
        if distance_to_travel > current_distance:
            distance_to_travel = current_distance
        self.look_at = self.look_at + (d*distance_to_travel)
    
    def pixel_to_world(self, px, py):
        px -= (self.win.width / 2)
        py -= (self.win.height / 2)
        return px/self.zoom + self.look_at.x, py/self.zoom + self.look_at.y

    def zoom_by(self, amt):
        self.zoom_target = self.zoom + amt

    def check_bounds(self,dt=1):
        x1,y1,x2,y2 = self.get_window()
        dx, dy = 0, 0
        if x1 < 0:
            dx = -x1
        if y1 < 0:
            dy = -y1
        if x2 > self.world.world_width:
            dx = -(x2 - self.world.world_width)
        if y2 > self.world.world_height:
            dy = -(y2 - self.world.world_height)
        self.look_at.x += dx
        self.look_at.y += dy

    def check_bounds_soft(self):
        if self.look_at.x < 0:
            self.look_at.x = 0
        if self.look_at.x > self.world.world_width:
            self.look_at.x = self.world.world_width
        if self.look_at.y < 0:
            self.look_at.y = 0
        if self.look_at.y > self.world.world_height:
            self.look_at.y = self.world.world_height
        
    def update(self, dt):
        self._zoom = approach_value(self._zoom_target, self._zoom, dt*self.zoom_rate)
        self.check_bounds_soft()
        

class Projection(object):
    def __init__(self, camera):
        self.camera = camera
    
    def __enter__(self):
        gl.glMatrixMode(gl.GL_PROJECTION); gl.glPushMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW); gl.glPushMatrix()
        self.camera.set_projection()
    
    def __exit__(self, *args):
        gl.glMatrixMode(gl.GL_PROJECTION); gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW); gl.glPopMatrix()
    