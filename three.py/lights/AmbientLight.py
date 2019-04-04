from lights import Light

class AmbientLight(Light):

    def __init__(self, color=[1,1,1], strength=1):
        super().__init__()
        self.isAmbient = 1
        self.color     = color
        self.strength  = strength