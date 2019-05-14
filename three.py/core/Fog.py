from core import *

class Fog(object):

    # fog effect is applied with 0% opacity at startDistance from camera,
    #   increasing linearly to 100% opacity at endDistance from camera
    def __init__(self, startDistance=1, endDistance=10, color=[0,0,0]):
        self.startDistance = startDistance
        self.endDistance   = endDistance
        self.color         = color
