from OpenGL.GL import *
from core import OpenGLUtils

class Material(object):

    def __init__(self, vertexShaderCode, fragmentShaderCode, uniforms=None):

        self.shaderProgramID = OpenGLUtils.initializeShaderFromCode(vertexShaderCode, fragmentShaderCode)
        
        self.uniformData = {}
        
        # options: GL_POINTS, GL_LINE_STRIP, GL_LINE_LOOP, GL_TRIANGLES
        self.drawStyle = GL_TRIANGLES
        
        # customize draw style GL_POINTS
        self.pointSize = 8
        
        # customize draw style GL_LINE_*
        self.lineWidth = 4
        
        # customize draw style GL_TRIANGLES
        # options: GL_LINE, GL_FILL
        self.fillStyle  = GL_FILL
        # which sides of triangles should be rendered?
        self.renderFront = True
        self.renderBack  = True
        
        self.additiveBlending = False
        
        if uniforms is not None:
            for uniform in uniforms:
                self.setUniform(uniform[0], uniform[1], uniform[2])
            
    # name: name of attribute variable in shader
    # value: array of values
    # type: float, vec2, vec3, vec4, bool(0 or 1), sampler2D
    def setUniform(self, type, name, value):
        data = { "type": type, "name": name, "value": value }
        self.uniformData[name] = data
