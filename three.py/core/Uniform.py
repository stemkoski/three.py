from OpenGL.GL import *

# objects that have associated uniforms (that may affect rendering a scene):
#  Material, Mesh, Camera, Fog, Lights
class Uniform(object):

    def __init__(self, type, name, value):
        
        # type: float | vec2 | vec3 | vec4 | mat4 | bool | sampler2D
        self.type = type
        
        # name of corresponding variable in shader program
        self.name = name
        
        # value to be sent to shader.
        #   float/vecN/matN: numeric data
        #   bool: 0 for False, 1 for True
        #   sampler2D: buffer ID where texture was stored 
        self.value = value

        # only used for uniform sampler2D variables;
        #   used to activate a particular texture slot
        self.textureNumber = None
        
        # for each shader program that uses this data,
        #   store the uniform variable's location (for increased performance)
        self.locationTable = {}


    def initializeLocation(self, shaderProgramID):
        location = glGetUniformLocation(shaderProgramID, self.name)
        self.locationTable[shaderProgramID] = location
        
        # DEBUG
        # print("Initializing shader program", shaderProgramID, "variable", self.name, "to location", location )

        
    # transmit currently stored value to corresponding variable in currently active shader
    def update(self, shaderProgramID):

        if shaderProgramID not in self.locationTable:
            self.initializeLocation(shaderProgramID)
        
        location = self.locationTable[shaderProgramID]
        
        # if the shader program does not reference the variable, then exit
        if location == -1:
            return
            
        if self.type == "bool":
            glUniform1i(location, self.value)
        elif self.type == "float":
            glUniform1f(location, self.value)
        elif self.type == "vec2":
            glUniform2f(location, self.value[0], self.value[1])
        elif self.type == "vec3":
            glUniform3f(location, self.value[0], self.value[1], self.value[2])
        elif self.type == "vec4":
            glUniform4f(location, self.value[0], self.value[1], self.value[2], self.value[3])
        elif self.type == "mat4":
            glUniformMatrix4fv(location, 1, GL_TRUE, self.value )
        elif self.type == "sampler2D":
            # the associations are:
            #   shader variable ID <-> texture slot <-> texture buffer ID/reference
            
            # requires textureNumber to be set before update is called
            
            # point uniform variable to get data from specific texture slot
            glUniform1i(location, self.textureNumber)
            # activate texture slot
            glActiveTexture( GL_TEXTURE0 + self.textureNumber )
            # associate texture buffer reference to currently active texture "slot"
            glBindTexture( GL_TEXTURE_2D, self.value )
            
            # textures (other than shadow map) default to repeat
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)    
