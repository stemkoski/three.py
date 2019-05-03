import numpy as np
from core import *
from cameras import *
from geometry import *
from material import *
from lights import Light
from math import acos

class DirectionalLight(Light):

    def __init__(self, position=[0,1,0], color=[1,1,1], strength=1, direction=[0,-1,0]):
        super().__init__(position=position, color=color, strength=strength)
        self.isDirectional = 1

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
    
    def enableShadows(self, shadowStrength=0.5, shadowMapSize=[512,512]):
        self.castShadow = True
        # developer may need to call dirLight.shadowCamera.setViewRegion
        #   to configure size according to scene dimensions
        self.shadowCamera = OrthographicCamera(left=-2, right=2, top=2, bottom=-2, near=10, far=0)
        
        # TODO: connect shadowCamera transform directly to this directional light's transform
        #   so that moving the light automatically moves the camera as well
        position = self.transform.getPosition()
        self.shadowCamera.transform.setPosition( position[0], position[1], position[2] )
        direction = self.getDirection()
        lookTarget = [ position[0] + direction[0], position[1] + direction[1], position[2] + direction[2] ]
        self.shadowCamera.transform.lookAt( lookTarget[0], lookTarget[1], lookTarget[2] )
        
        self.shadowStrength = shadowStrength
        self.shadowBias = 0.005
        
        # vertex shader code
        vsCode = """
        in vec3 vertexPosition; 
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;      
        void main()
        {
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
        }
        """
        # fragment shader code
        fsCode = """
        void main()
        {
            gl_FragColor = vec4(gl_FragCoord.z, gl_FragCoord.z, gl_FragCoord.z, 1);
        }
        """
        
        self.shadowMaterial = Material(vsCode, fsCode)
        
        # TODO: why can't RenderTarget be called here?
        #  as a result, is currently set from main program
        # self.shadowRenderTarget = RenderTarget( 1024,1024 )
        
        
        