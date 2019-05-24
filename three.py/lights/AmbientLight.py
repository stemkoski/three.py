from lights import Light

class AmbientLight(Light):

    def __init__(self, position=[0,0,0], color=[1,1,1], strength=1):
        super().__init__(position=position, color=color, strength=strength)

        self.uniformList.setUniformValue("isAmbient", 1)