import numpy as np
from core import Uniform, RenderTarget
from cameras import ShadowCamera
from lights import Light
from material import ShadowMaterial
from mathutils import MatrixFactory
from math import acos

class DirectionalLight(Light):

    def __init__(self, position=[0,1,0], color=[1,1,1], strength=1, direction=[0,-1,0]):
        super().__init__(position=position, color=color, strength=strength)

        self.uniformList.setUniformValue("isDirectional", 1)

        # DEFAULT vector is totally arbitrary.
        # TODO: allow direction to be parallel to DEFAULT vector as well
        self.DEFAULT = [1.001, 0.001, 0.001]
        self.DEFAULT = np.divide( self.DEFAULT, np.linalg.norm(self.DEFAULT) )
        self.setDirection(direction)
        
    def setDirection(self, direction):
    
        # normalize the direction
        direction = np.divide( direction, np.linalg.norm(direction) )
    
        # set the rotational part of the transform matrix
        #   to be the matrix that rotates DEFAULT into direction

        # cross product is perpendicular to DEFAULT and direction
        crossProduct = np.cross(self.DEFAULT, direction)
        # if this magnitude of the crossProduct vector is nonzero, 
        #     then DEFAULT and direction point in different directions
        #     and this transform matrix needs to be updated accordingly
        magnitude = np.linalg.norm(crossProduct)
        if (magnitude > 0.0001):
            # normalize the cross product vector
            crossProduct = np.divide(crossProduct, magnitude)
            # calculate the angle between the vectors
            theta = acos( np.dot(self.DEFAULT, direction) )
            # calculate the matrix the rotates DEFAULT into direction
            rotationMatrix = MatrixFactory.makeRotationAxisAngle(crossProduct, theta)
            # copy rotation data into this object's transformation matrix
            self.transform.setRotationSubmatrix( rotationMatrix )
                    
    def getDirection(self): 
        rotationMatrix = self.transform.getRotationMatrix()
        return list( rotationMatrix @ self.DEFAULT )
    
    def enableShadows(self, strength=0.5, bias=0.005, size=[1024,1024]):
        
        # developer may need to call dirLight.shadowCamera.setViewRegion
        #   to configure size according to scene dimensions
        self.shadowCamera = ShadowCamera(left=-2, right=2, top=2, bottom=-2, near=10, far=0)
        
        self.shadowMaterial = ShadowMaterial()

        # TODO: connect shadowCamera transform directly to this directional light's transform
        #   so that moving the light automatically moves the shadowCamera and shadowLightDirection also
        position = self.transform.getPosition()
        self.shadowCamera.transform.setPosition( position[0], position[1], position[2] )
        direction = self.getDirection()
        lookTarget = [ position[0] + direction[0], position[1] + direction[1], position[2] + direction[2] ]
        self.shadowCamera.transform.lookAt( lookTarget[0], lookTarget[1], lookTarget[2] )
        
        self.shadowCamera.uniformList.addUniform( Uniform("float", "shadowStrength", strength) )
        self.shadowCamera.uniformList.addUniform( Uniform("float", "shadowBias", bias) )
        self.shadowCamera.uniformList.addUniform( Uniform("vec3", "shadowLightDirection", self.getDirection() ) )

        self.shadowRenderTarget = RenderTarget.RenderTarget( size[0], size[1] )
        self.shadowCamera.uniformList.addUniform( Uniform("sampler2D", "shadowMap", self.shadowRenderTarget.textureID ) )
        # texture slot 0 reserved for shadow map texture
        self.shadowCamera.uniformList.data["shadowMap"].textureNumber = 0


        