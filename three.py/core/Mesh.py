import numpy as np
from OpenGL.GL import *

from core import Object3D

class Mesh(Object3D):

    def __init__(self, geometry, material):
        super().__init__()
        self.geometry = geometry
        self.material = material
        self.visible = True
         
    # passing shaderProgramID as a parameter because
    #   usually Mesh will render with it's own Material's shader
    #   but when doing shadow passes, uses a different shader
    def render(self, shaderProgramID=None):

        if not self.visible:
            return

         # automatically activate vertex bindings stored in associated VAO
        vao = self.geometry.getVAO(shaderProgramID)
        glBindVertexArray(vao)
        
        # update uniform matrix data (transform = modelMatrix)        
        modelMatrixVarID = glGetUniformLocation(shaderProgramID, "modelMatrix")
        glUniformMatrix4fv(modelMatrixVarID, 1, GL_TRUE, self.getWorldMatrix() )
                
        # update uniform material data
        # textureNumber starts at 1 because slot 0 will be reserved for shadow map (if any)
        textureNumber = 1         
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
                    # when rendering normal textures, set coordinates to repeat
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
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
        
