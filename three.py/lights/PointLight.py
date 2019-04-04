from lights import Light

class PointLight(Light):

    def __init__(self, color=[1,1,1], strength=1, position=[0,0,0]):
        super().__init__()
        self.isPoint  = 1
        self.color    = color
        self.strength = strength
        self.transform.setPosition( position[0], position[1], position[2] )
        