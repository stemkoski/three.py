from core import *
from cameras import OrthographicCamera

class ShadowCamera(OrthographicCamera):

    def __init__(self, left=-1, right=1, top=1, bottom=-1, near=1, far=-1):
        super().__init__(left, right, top, bottom, near, far)
        self.setViewRegion(left, right, top, bottom, near, far)
    
        # overwrite uniformList with new naming convention
        self.uniformList = UniformList()
        self.uniformList.addUniform( Uniform("mat4", "shadowProjectionMatrix", self.projectionMatrix) )
        self.uniformList.addUniform( Uniform("mat4", "shadowViewMatrix", self.viewMatrix) )
