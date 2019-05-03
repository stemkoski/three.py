from core import Object3D

class Light(Object3D):

    # constructor takes no arguments; set default values in code. extensions have parameterized constructors...
    def __init__(self, position=[0,0,0], color=[1,1,1], strength=1):
    
        super().__init__()
        
        # one of these values should be set to 1 by extending class
        self.isAmbient     = 0
        self.isDirectional = 0
        self.isPoint       = 0
        
        # default light color
        self.color    = color
        # control relative intensity of lights
        self.strength = strength
        
        # store light position in matrix to simplify light movement (PointLight)
        # and to adjust position of helper meshes (DirectionalLightHelper, PointLightHelper)
        # also used in shadow calculations for directional light
        self.transform.setPosition( position[0], position[1], position[2] )
        
        
    def enableShadows(self, strength=0.5):
        pass