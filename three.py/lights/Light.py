from core import Object3D

class Light(Object3D):

    # constructor takes no arguments; set default values in code. extensions have parameterized constructors...
    def __init__(self):
    
        super().__init__()
        
        # one of these values should be set to 1 by extending class
        self.isAmbient     = 0
        self.isDirectional = 0
        self.isPoint       = 0
        
        # default light color
        self.color    = [1,1,1]
        # control relative intensity of lights
        self.strength = 1
        
        # store light position in matrix to simplify light movement (PointLight)
        # and to adjust position of helper meshes (DirectionalLightHelper, PointLightHelper)
        self.transform.setPosition(0,0,0)
        # direction of light is constant for DirectionLight; needs to be normalized
        self.direction = [0,-1,0]
        
