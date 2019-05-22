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
        # textureNumber starts at 1 because slot 0 reserved for shadow map (if any)
        textureNumber = 1
        for uniform in self.material.uniformList.values():
            if uniform.type == "sampler2D":
                # used to activate a particular texture slot
                uniform.textureNumber = textureNumber
                # increment textureNumber in case additional textures are in use
                textureNumber += 1
            uniform.update( shaderProgramID )

        # set render parameters
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
        
