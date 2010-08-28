from pyglet.graphics import *
from pyglet.gl import *
import ctypes

activeShader = None

class Shader(object):
    """An OpenGL shader object"""
    def __init__( self, shader_type, name="(unnamed shader)" ):
        self.shaderObject = glCreateShaderObjectARB( shader_type )
        self.name = name
        self.program = None
    
    def __del__ (self ):
        print "ARRR!"
        if self.program:
            self.program.detachShader( self )
            self.program = None
        
        glDeleteShader( self.shaderObject )
        print "Shader " + self.name + " deleted"
    
    def source( self, source_string ):
        c = ctypes
        buff = c.create_string_buffer(source_string)
        c_text = c.cast(c.pointer(c.pointer(buff)),
                        c.POINTER(c.POINTER(GLchar))) 
        glShaderSourceARB( self.shaderObject, 1, c_text, None )
    
    def compileShader( self ):
        glCompileShader( self.shaderObject )
        rval = ctypes.c_long()
        glGetObjectParameterivARB (self.shaderObject, GL_OBJECT_COMPILE_STATUS_ARB, ctypes.pointer(rval))
        if rval:
            print "%s compiled successfuly." % (self.name)
        else:
            print "Compile failed on shader %s: " % (self.name)
            self.printInfoLog( ) 
    
    
    def infoLog( self ):
        return glGetInfoLogARB (self.shaderObject )
    
    def printInfoLog( self ):
        print self.infoLog()

class UniformVar(object):
    def __init__(self, set_function, name, value ):
        self.setFunction = set_function
        self.name = name
        self.value = value
    
    def set(self):
        self.setFunction( self.name, self.value )

class Program( object ):
    """An OpenGL shader program"""
    def __init__(self):
        self.programObject = glCreateProgramObjectARB()
        self.shaders = []
        self.uniformVars = {}
    
    def __del__(self):
        glDeleteObjectARB( self.programObject) 
    
    def attachShader( self, shader ):
        self.shaders.append( shader )
        shader.program = self
        glAttachObjectARB( self.programObject, shader.shaderObject )
    
    def detachShader( self, shader ):
        self.shaders.remove( shader )
        glDetachObjectARB( self.programObject, shader.shaderObject )
        print "Shader detached"
    
    def link( self ):
        glLinkProgramARB( self.programObject )
    
    def use( self ):
        global activeShader
        activeShader = self
        glUseProgramObjectARB( self.programObject )
        self.setVars()
        
    
    def stop(self):
        global activeShader
        glUseProgramObjectARB( 0 )
        activeShader = None
    
    def uniform1i( self, name, value ):
        self.uniformVars[name] = UniformVar( self.set_uniform1i, name, value )
        if self == activeShader:
            self.uniformVars[name].set()
    
    def set_uniform1i( self, name, value ):
        location = glGetUniformLocationARB( self.programObject, name )
        glUniform1iARB( location, value )
    
    def setVars(self):
        for name, var in self.uniformVars.iteritems():
            var.set()
    
    def printInfoLog( self ):
        print glGetInfoLogARB (self.programObject )


def MakePixelShaderFromSource ( src ):
    return MakeShaderFromSource( src, GL_FRAGMENT_SHADER_ARB )

def MakeVertexShaderFromSource ( src ):
    return MakeShaderFromSource( src, GL_VERTEX_SHADER_ARB )

def MakeShaderFromSource( src, shader_type ):
        shader =  Shader( shader_type )
        shader.source( src )
        shader.compileShader()
        return shader

def MakeProgramFromSourceFiles( vertex_shader_name, pixel_shader_name ):
    file = open( vertex_shader_name, "r")
    vs_src = file.tostring()
    file.close()
    file = open( pixel_shader_name, "r")
    ps_src = file.tostring()
    file.close()
    return MakeProgramFromSource( vs_src, ps_src )

def MakeProgramFromSource( vertex_shader_src, pixel_shader_src ):
    vs = MakeVertexShaderFromSource( vertex_shader_src )
    ps = MakePixelShaderFromSource ( pixel_shader_src )
    
    p = Program()
    p.attachShader( vs )
    p.attachShader( ps )
    p.link()
    p.use()
    return p

def DisableShaders():
    global activeShader 
    glUseProgramObjectARB( 0 )
    activeShader = None