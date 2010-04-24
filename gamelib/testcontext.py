from context import BaseContext
import pyglet

class TestContext(BaseContext):
    def __init__(self, window):
        WorldContext.__init__(self, "TestContext")
        
        self._label = pyglet.text.Label('AMG WORDS',
                          font_name='Times New Roman',
                          font_size=18,
                          x=window.width//2, y=window.height-16,
                          anchor_x='center', anchor_y='center')
        
    def draw(self):
        self._label.draw()