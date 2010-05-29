import pyglet
import graphics
import menucontext
import mapcontext
import settings
from contextmanager import ContextManager

# Use psycho if it's installed. Framerate++!
try: 
    import psycho
    psycho.full()
except:
    pass

gl = pyglet.gl.gl

class MurderWindow(pyglet.window.Window):
    scale = settings.scale
    
    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
    
    def init(self):
        try:
            pyglet.resource.add_font('data/fonts/pic.ttf')
        except:
            pass
        settings.world_width = self.width*settings.scale
        settings.world_height = self.height*settings.scale
        self.fps_display = pyglet.clock.ClockDisplay()
        pyglet.clock.set_fps_limit(100)
        
        cursor = self.get_system_mouse_cursor(pyglet.window.Window.CURSOR_CROSSHAIR)
        self.set_mouse_cursor(cursor)    
        
        self.context_manager = ContextManager([
            menucontext.MenuContext(self),
            mapcontext.MapContext(self, "MapContext"),
            mapcontext.WinContext(self)
            ])
        
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        
    def set_viewport(self, width, height):
        gl = pyglet.gl.gl
        gl.glViewport(0, 0, width, height)
        self.set_projection(width, height)
    
    def set_projection(self, w, h):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-w/2, w/2, -h/2, h/2, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    
    def save_projection(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def restore_projection(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def on_resize(self,width, height):
        self.set_viewport(width, height)
        settings.world_width = width * settings.scale
        settings.world_height = height * settings.scale
        print settings.world_width, settings.world_height
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.context_manager.current_context.on_mouse_press(x*self.scale, y*self.scale, button, modifiers)
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.context_manager.current_context.on_mouse_release(x*self.scale, y*self.scale, button, modifiers)
        
    def on_mouse_motion(self, x, y, dx, dy):
        self.context_manager.current_context.on_mouse_motion(x*self.scale, y*self.scale, dx, dy)
    
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.context_manager.current_context.on_mouse_drag(x*self.scale, y*self.scale, dx, dy, button, modifiers)
        
    def on_key_press(self, symbol, modifiers):
        super(MurderWindow, self).on_key_press(symbol, modifiers)
        self.context_manager.current_context.on_key_press(symbol, modifiers)
    
    def step(self):
        #Tick the clock
        dt = pyglet.clock.tick() 
        self.context_manager.current_context.update(dt)
    
    def redraw(self):
        gl = pyglet.gl.gl
        gl.glClearColor(0.15,0.15,0.25,1)
        self.clear()
        gl.glColor4f(1,1,1,1)
        self.context_manager.current_context.predraw()
        self.save_projection()
        self.set_projection(self.width*self.scale, self.height*self.scale)
        self.context_manager.current_context.draw()
        self.restore_projection()
        
        self.context_manager.current_context.draw_ui()
        
        #Gets fps and draw it
        if settings.show_fps:
            self.fps_display.draw()
        self.flip()


def main():
    if settings.fullscreen:
        mw = MurderWindow(vsync=0, fullscreen=settings.fullscreen)
    else:
        mw = MurderWindow(width=settings.width, height=settings.height, vsync=0, fullscreen=settings.fullscreen)
    mw.init()
    
    while not mw.has_exit:
        mw.dispatch_events()
        
        #step the game world
        mw.step()
        
        #draw game world here
        mw.redraw()
        
        if mw.keys[pyglet.window.key.Q]:
            print 'Q'

