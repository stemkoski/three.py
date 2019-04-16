from math import sin, cos, pi
from mathutils import Curve

class CurveFactory(object):

    @staticmethod
    def makeLineSegment(startPoint, endPoint, divisions=2):
        return Curve( lambda t : [(1-t)*startPoint[0]+t*endPoint[0], (1-t)*startPoint[1]+t*endPoint[1], (1-t)*startPoint[2]+t*endPoint[2]], 0, 1, divisions )

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
    
    # create a curve from A to B, with slope AP at A and slope QB at B.
    @staticmethod
    def makeCubicBezier(A, P, Q, B, divisions=100):
        return Curve( lambda t : [ (1-t)*(1-t)*(1-t)*A[0] + 3*(1-t)*(1-t)*t*P[0] + 3*(1-t)*t*t*Q[0] + t*t*t*B[0],
                                   (1-t)*(1-t)*(1-t)*A[1] + 3*(1-t)*(1-t)*t*P[1] + 3*(1-t)*t*t*Q[1] + t*t*t*B[1],
                                   (1-t)*(1-t)*(1-t)*A[2] + 3*(1-t)*(1-t)*t*P[2] + 3*(1-t)*t*t*Q[2] + t*t*t*B[2] ],
                                    0,1, divisions )
          