from OpenGL.GL import *
from core import OpenGLUtils, Uniform

class Material(object):

    def __init__(self, vertexShaderCode, fragmentShaderCode, uniforms=None, name="Material"):

        self.shaderProgramID = OpenGLUtils.initializeShaderFromCode(vertexShaderCode, fragmentShaderCode)
        self.name = name

        # DEBUG
        # print("Initializing Shader Program #", self.shaderProgramID, "for material:", self.name)

        self.uniformList = {}
        
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
            
    # type:  float, vec2, vec3, vec4, bool(0 or 1), sampler2D, mat4
    # name:  name of attribute variable in shader
    # value: array of values
    def setUniform(self, type, name, value):
        self.uniformList[name] = Uniform(type, name, value)
