import numpy as np
from OpenGL.GL import *

from core import Object3D

class Mesh(Object3D):

    def __init__(self, geometry, material):
        super().__init__()
        self.geometry = geometry
        self.material = material
        self.visible = True
        
    def render(self):

        if not self.visible:
            return
            
        shaderProgramID = self.material.shaderProgramID
        
        glUseProgram( shaderProgramID )

        # set up attribute pointers
        for name, data in self.geometry.attributeData.items():

            # if necessary, obtain an available buffer reference
            if data["bufferID"] is None:
                # return an available (unused) reference value
                data["bufferID"] = glGenBuffers(1)
                
            # if necessary, buffer data to GPU
            if data["needsUpdate"] is True:
                # make current bufferID active
                glBindBuffer(GL_ARRAY_BUFFER, data["bufferID"])
                # convert to a numpy array
                array = np.array( data["value"] ).astype( np.float32 )
                # create empty buffer object if necessary,
                # and send data to the active buffer
                glBufferData(GL_ARRAY_BUFFER, array.ravel(), GL_STATIC_DRAW)
                # all done!
                data["needsUpdate"] = False

            # make current bufferID active
            glBindBuffer(GL_ARRAY_BUFFER, data["bufferID"])

            attributeVarID = glGetAttribLocation(shaderProgramID, data["name"])
            # check if this variable exists in shader program; if so, point it to currently bound bufferID.
            if (attributeVarID != -1):
                glEnableVertexAttribArray(attributeVarID)
                if data["type"] == "float":
                    glVertexAttribPointer(attributeVarID, 1, GL_FLOAT, False, 0, None)
                elif data["type"] == "vec2":
                    glVertexAttribPointer(attributeVarID, 2, GL_FLOAT, False, 0, None)
                elif data["type"] == "vec3":
                    glVertexAttribPointer(attributeVarID, 3, GL_FLOAT, False, 0, None)
                elif data["type"] == "vec4":
                    glVertexAttribPointer(attributeVarID, 4, GL_FLOAT, False, 0, None)
                else:
                    raise Exception("Attribute " + data['name'] + " has unknown type " + data['type'])

        # update uniform matrix data (transform = modelMatrix)        
        modelMatrixVarID = glGetUniformLocation(shaderProgramID, "modelMatrix")
        glUniformMatrix4fv(modelMatrixVarID, 1, GL_TRUE, self.getWorldMatrix() )
                
        # update uniform material data
        textureNumber = 0         
        for name, data in self.material.uniformData.items():

            uniformVarID = glGetUniformLocation(shaderProgramID, data["name"])

            if (uniformVarID != -1):
                if data["type"] == "bool":
                    glUniform1i(uniformVarID, data["value"])
                elif data["type"] == "float":
                    glUniform1f(uniformVarID, data["value"])
                elif data["type"] == "vec2":
                    glUniform2f(uniformVarID, data["value"][0], data["value"][1])
                elif data["type"] == "vec3":
                    glUniform3f(uniformVarID, data["value"][0], data["value"][1], data["value"][2])
                elif data["type"] == "vec4":
                    glUniform4f(uniformVarID, data["value"][0], data["value"][1], data["value"][2], data["value"][3])
                elif data["type"] == "sampler2D":
                    # var <-> slot <-> buffer/ref/ID
                    # point uniform to get data from specific texture slot
                    glUniform1i(uniformVarID, textureNumber)
                    # activate texture slot
                    glActiveTexture( GL_TEXTURE0 + textureNumber )
                    # associate texture data reference to currently active texture "slot" (usually 0 through 15)
                    glBindTexture( GL_TEXTURE_2D, data["value"] )
                    # increment textureNumber in case additional textures are in use
                    textureNumber += 1
                
                else:
                    raise Exception("Uniform " + data['name'] + " has unknown type " + data['type'])


        # render settings
        glPointSize(self.material.pointSize)
        glLineWidth(self.material.lineWidth)
        
        # enable meshes to cull front or back faces
        if self.material.renderFront and self.material.renderBack:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
            if not self.material.renderFront:
                glCullFace(GL_FRONT)
            if not self.material.renderBack:
                glCullFace(GL_BACK)
        
        # apply the fill style to both front and back
        glPolygonMode(GL_FRONT_AND_BACK, self.material.fillStyle)        
        
        # use additive blending or normal blending (default)
        if self.material.additiveBlending:
            # additive
            glBlendFunc(GL_ONE, GL_ONE)
        else: 
            # normal blending
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glDrawArrays(self.material.drawStyle, 0, self.geometry.vertexCount)
        
