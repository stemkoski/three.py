from lights import Light
import numpy as np

class DirectionalLight(Light):

    def __init__(self, color=[1,1,1], strength=1, position=[0,0,0], direction=[0,-1,0]):
        super().__init__()        
        self.isDirectional = 1
        self.color    = color
        self.strength = strength
        self.transform.setPosition( position[0], position[1], position[2] )
        self.direction = np.divide( direction, np.linalg.norm(direction) )
        