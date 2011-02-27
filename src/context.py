from signal import Signal

class BaseContext(object):
    def __init__(self, name):
        self.name = name
        
        self.switch_requested = Signal()
    
    def on_mouse_press(self, x, y, button, modifiers):
        print "Pressed", x, y, button
    
    def on_mouse_release(self, x, y, button, modifiers):
        print "Released", x, y, button
    
    def on_mouse_motion(self, x, y, dx, dy):
        pass
    
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        pass
    
    def on_mouse_scroll(self, x, y, sx, sy):
        pass
    
    def on_key_press(self, symbol, modifiers):
        pass
    
    def on_activate(self):
        pass
    
    def update(self, dt):
        pass
    
    def predraw(self):
        pass
    
    def draw(self):
        pass
    
    def draw_ui(self):
        pass
    
    def switch_to(self, context_name):
        self.switch_requested(context_name)