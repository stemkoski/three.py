from core import Object3D, Uniform, UniformList

class Light(Object3D):

    # global variable used to track number of lights and create unique names
    lightCount = 0

    def __init__(self, position=[0,0,0], color=[1,1,1], strength=1):
    
        super().__init__()

        self.name = "light" + str(Light.lightCount)
        Light.lightCount += 1

        self.uniformList = UniformList()

        # one of these uniform values should be set to 1 by extending class
        self.uniformList.addUniform( Uniform("bool", self.name + ".isAmbient", 0),     indexName="isAmbient" )
        self.uniformList.addUniform( Uniform("bool", self.name + ".isDirectional", 0), indexName="isDirectional" )
        self.uniformList.addUniform( Uniform("bool", self.name + ".isPoint", 0),       indexName="isPoint" )
        
        # default light color
        self.uniformList.addUniform( Uniform("float", self.name + ".strength", strength), indexName="strength" )
        
        # control relative intensity of lights
        self.uniformList.addUniform( Uniform("vec3", self.name + ".color", color), indexName="color" )

        # store position and direction in uniforms
        self.uniformList.addUniform( Uniform("vec3", self.name + ".position", position), indexName="position" )
        self.uniformList.addUniform( Uniform("vec3", self.name + ".direction", [0,0,0]), indexName="direction" )
        
        # store light position in matrix to simplify light movement (PointLight)
        # and to adjust position of helper meshes (DirectionalLightHelper, PointLightHelper)
        # also used in shadow calculations for directional light
        self.transform.setPosition( position[0], position[1], position[2] )

        # set by DirectionalLight if shadows are enabled
        self.shadowCamera = None

    # overridden by DirectionalLight class
    def getDirection(self):
        return [0,0,0]

    # overridden by DirectionalLight class
    def enableShadows(self, strength=0.5):
        pass