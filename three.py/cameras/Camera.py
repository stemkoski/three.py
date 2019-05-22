import numpy as np
from core import *
from mathutils import MatrixFactory

class Camera(Object3D):

    def __init__(self):
        super().__init__()
        self.projectionMatrix = MatrixFactory.makeIdentity()
        self.viewMatrix = MatrixFactory.makeIdentity()
        
        self.uniformList = {}
        self.uniformList["projectionMatrix"] = Uniform("mat4", "projectionMatrix", self.projectionMatrix)
        self.uniformList["viewMatrix"]       = Uniform("mat4", "viewMatrix", self.viewMatrix)

    def getProjectionMatrix(self):
        return self.projectionMatrix
        
    def updateViewMatrix(self):
        self.viewMatrix = np.linalg.inv(self.transform.matrix)
        
    def getViewMatrix(self):
        return self.viewMatrix
