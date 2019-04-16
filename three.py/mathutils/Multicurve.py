import math
import numpy as np
from mathutils import MatrixFactory


# a multicurve consists of a list of curve objects

class Multicurve(object):

    # divisions = number of line segments. len(points) = divisions+1.
    def __init__(self, curveList, tMin=0, tMax=1, divisions=4, arcLengthDivisions=256):
        self.curveList = curveList
        self.numberCurves = len(curveList)
        
    
                
    # calculates a point according to arclength parameterization
    # u - percentage of total curveList distance traversed, in [0,1]
    # if curveList contains N curves, then the range [I/N, (I+1)/N] corresponds to curve I
    def getPoint(self, u):
        curveIndex = int( u * self.numberCurves )
        curveTime = u * self.numberCurves - curveIndex
        return self.curveList[curveIndex].getPoint(curveTime)
        
    # calculates a list of equally spaced points along the curve
    # size of list specified by divisions parameter in constructor
    def getPoints(self):
        points = []
        for curve in self.curveList:
            points.extend( curve.getPoints() )
        return points
    
    # calculates a tangent vector according to arclength parameterization
    # u - percentage of total curveList distance traversed, in [0,1]
    def getTangent(self, u):
        curveIndex = int( u * self.numberCurves )
        curveTime = u - curveIndex
        return self.curveList[curveIndex].getTangent(curveTime)
    
    
    # returns { "tangents" : list, "normals" : list, "binormals" : list }
    #  length of each list = divisions
    def getFrames(self):
        tangents  = []
        normals   = []
        binormals = []
        for curve in self.curveList:
            frames = curve.getFrames()
            tangents.extend( frames["tangents"] )
            normals.extend( frames["normals"] )
            binormals.extend( frames["binormals"] )
        return { "tangents" : tangents, "normals" : normals, "binormals" : binormals }
        