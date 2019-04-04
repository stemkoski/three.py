from math import sin, cos, pi
from mathutils import Curve

class CurveFactory(object):

    @staticmethod
    def makeCircle(radius=1, divisions=64):
        return Curve( lambda t : [radius*cos(t), radius*sin(t), 0], 0, 2*pi, divisions )
        
    @staticmethod
    def makePolygon(sides=6, radius=1):
        return Curve( lambda t : [radius*cos(t), radius*sin(t), 0], 0, 2*pi, sides+1 )

    @staticmethod
    def makeHelix(radius=1, height=2, revolutions=3, divisions=128):
        return Curve( lambda t : [radius*cos(t), height*t/(2*pi*revolutions) - height/2, radius*sin(t)], 0, 2*pi*revolutions, divisions )

    @staticmethod
    def makeTorusKnot(p=2, q=3, divisions=128):
        return Curve( lambda t : [0.5*(2 + cos(q*t))*cos(p*t), 0.5*(2 + cos(q*t))*sin(p*t), 0.5*sin(q*t)], 0, 2*pi, divisions )
        
    @staticmethod
    def makeTrefoilKnot(divisions=100):
        return Curve( lambda t : [0.5*(t**3 - 3*t), 0.5*(t**4 - 4*t**2 + 2), 0.1*(t**5 - 10*t)], -2, 2, divisions )

    @staticmethod
    def makeFigureEightKnot(divisions=100):
        return Curve( lambda t : [ 0.5*(t**3 - 3*t), 0.2*t*(t**2 - 1)*(t**2 - 4), 0.02*(t**7 - 42*t)], -2.1, 2.1, divisions )
        