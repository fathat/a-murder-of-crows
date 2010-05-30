from common import *
from Box2D import b2Vec2
from pyglet.gl import gl
import settings

class Camera(object):
    def __init__(self, window):
        self._look_at = b2Vec2(0, 0)
        self._zoom = 1.0/settings.scale
        self._zoom_target = self._zoom
        self.zoom_rate = 1.0
        self.win = window
    
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
    
    def update(self, dt):
        self._zoom = approach_value(self._zoom_target, self._zoom, dt*self.zoom_rate)

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
    