import numpy as np
from OpenGL.GL import *

from core import Object3D, Uniform, UniformList

class Mesh(Object3D):

    def __init__(self, geometry, material):
        super().__init__()
        self.geometry = geometry
        self.material = material
        self.visible = True

        self.uniformList = UniformList()
        self.uniformList.addUniform( Uniform("mat4", "modelMatrix", self.transform) )

        # casting shadow stored as a boolean 
        #   because it affects if mesh is included during rendering pass where shadow map texture is generated
        self.castShadow = False
        # receiving shadow stored in a uniform
        #   because it affects appearance of this object when rendered
        self.uniformList.addUniform( Uniform("bool", "receiveShadow", 0) )

    def setCastShadow(self, state=True):
        self.castShadow = state

    def setReceiveShadow(self, state=True):
        if state:
            self.uniformList.setUniformValue("receiveShadow", 1)
        else:
            self.uniformList.setUniformValue("receiveShadow", 0)

    # passing shaderProgramID as a parameter because
    #   usually Mesh will render with it's own Material's shader
    #   but when doing shadow passes, uses a different shader
    def render(self, shaderProgramID=None):

        if not self.visible:
            return

        # automatically activate vertex bindings stored in associated VAO
        vao = self.geometry.getVAO(shaderProgramID)
        glBindVertexArray(vao)

        # update mesh uniform data here, 
        #   otherwise this code is repeated for shadow pass and standard pass in renderer class
        self.uniformList.setUniformValue( "modelMatrix", self.getWorldMatrix() )
        self.uniformList.update( shaderProgramID )

        # update material uniform data
        # textureNumber starts at 1 because slot 0 reserved for shadow map (if any)
        textureNumber = 1
        for uniform in self.material.uniformList.values():
            if uniform.type == "sampler2D":
                # used to activate a particular texture slot
                uniform.textureNumber = textureNumber
                # increment textureNumber in case additional textures are in use
                textureNumber += 1
            uniform.update( shaderProgramID )

        # update material render settings
        self.material.updateRenderSettings()
      
        # draw the mesh
        glDrawArrays(self.material.drawStyle, 0, self.geometry.vertexCount)
        
