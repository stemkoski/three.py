from random import uniform
from math import sin, cos, pi, sqrt

class RandomUtils(object):
        
    @staticmethod
    def randomFloat(center=0.5, spread=0.5):
        return center + uniform(-spread, +spread)

    @staticmethod
    def randomBoxVec3(center=[0,0,0], spread=[1,1,1]):
        return [ center[0] + uniform(-spread[0], +spread[0]), 
                 center[1] + uniform(-spread[1], +spread[1]), 
                 center[2] + uniform(-spread[2], +spread[2]) ]

    @staticmethod
    def randomUnitSphereVec3():
        z = uniform(-1, 1)
        r = sqrt(1 - z**2)
        t = uniform(0, 2*pi)
        x = r*cos(t)
        y = r*sin(t)
        return [x,y,z]

    @staticmethod
    def randomSphereVec3(center=[0,0,0], spread=1):
        x,y,z = RandomGenerator.randomUnitSphereVec3()
        s = uniform(0, spread)
        return [center[0] + s*x, 
                center[1] + s*y, 
                center[2] + s*z]
