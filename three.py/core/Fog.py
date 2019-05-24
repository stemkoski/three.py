from core import Uniform, UniformList

class Fog(object):

    # fog effect is applied with 0% opacity at startDistance from camera,
    #   increasing linearly to 100% opacity at endDistance from camera
    def __init__(self, startDistance=1, endDistance=10, color=[0,0,0]):

        self.uniformList = UniformList()
        self.uniformList.addUniform( Uniform("bool", "useFog", 1) )
        self.uniformList.addUniform( Uniform("float", "fogStartDistance", startDistance) )
        self.uniformList.addUniform( Uniform("float", "fogEndDistance", endDistance) )
        self.uniformList.addUniform( Uniform("vec3", "fogColor", color) )
