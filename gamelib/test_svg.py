import pyglet
from pyglet.gl import *
import shader

import sys

import squirtle

vs = """

void main()
{
	gl_Position = ftransform();
} 
"""

ps = """

uniform vec2 center;
uniform float radius;

void main()
{
	vec4 texel1, texel2, texel3;
	vec4 result;
	
	//calculate the intensity
	float intensity = 1.0 - (distance(gl_FragCoord.xy, center) / radius);
	
	result.rgb = vec3(intensity);// * texel2.rgb;
	result.a = 1.0;
	
	gl_FragColor = result;
}
"""


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "data/level_.svg"
    
w = pyglet.window.Window(800, 600)
keys = pyglet.window.key.KeyStateHandler()
w.push_handlers(keys)

glClearColor(0,0,1,1)

squirtle.setup_gl()

#shader_program = shader.MakeProgramFromSource(squirtle.vertex_shader_src, squirtle.radial_shader_src)
#shader_program.uniformf("radius", 800.0)
#shader_program.uniformf("center", 400.0, 300.0)
#shader_program.uniformf("stops", 0.66, 0.75, 1.0, 0.0)
#
#shader_program.uniformf("stop0", 1.0, 0.0, 0.0, 1.0)
#shader_program.uniformf("stop1", 0.0, 1.0, 0.0, 1.0)
#shader_program.uniformf("stop2", 0.0, 0.0, 1.0, 1.0)
#shader_program.uniformf("stop3", 0.0, 0.0, 0.0, 1.0)
#shader_program.use()


s = squirtle.SVG(filename)
s.anchor_x, s.anchor_y = s.width/2, s.height/2
print dir(s)

zoom = 1
angle = 0
draw_x = 400
draw_y = 300

def tick(dt):
    global zoom, angle, draw_x, draw_y
    if keys[pyglet.window.key.W]:
        draw_y -= 8
    elif keys[pyglet.window.key.S]:
        draw_y += 8
    elif keys[pyglet.window.key.D]:
        draw_x -= 8
    elif keys[pyglet.window.key.A]:
        draw_x += 8
    elif keys[pyglet.window.key.UP]:
        zoom *= 1.1
    elif keys[pyglet.window.key.DOWN]:
        zoom /= 1.1
    elif keys[pyglet.window.key.LEFT]:
        angle -= 8
    elif keys[pyglet.window.key.RIGHT]:
        angle += 8
        
pyglet.clock.schedule_interval(tick, 1/60.0)


@w.event
def on_draw():
    w.clear()
    s.draw(draw_x, draw_y, scale=zoom, angle=angle)

pyglet.app.run()
