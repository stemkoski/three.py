from geometry import *
import numpy as np
from math import sin, cos, pi, radians
from core import *

class TubeGeometry(Geometry):
    def __init__(self, curve, tubeRadius=0.1, radiusSegments=6):
        super().__init__()

        # calculate and store curve data
        lengthSegments = curve.divisions
        curvePoints    = curve.getPoints()
        frames         = curve.getFrames()
        
        # 2D list to store points and normals on tube
        tubePoints = []
        tubeNormals = [] 
        # angle between radial points
        angle = radians(360)/radiusSegments

        for n in range(lengthSegments):
            radialPoints = []
            radialNormals = []
            for i in range(0,radiusSegments+1):
                center  = np.array( curvePoints[n] )
                N = frames["normals"][n]
                B = frames["binormals"][n]
                normal = np.multiply(cos(angle*i), N) + np.multiply(sin(angle*i), B)
                point   = center + tubeRadius * normal
                radialPoints.append( list(point) )
                radialNormals.append( list(normal) )
            tubePoints.append(radialPoints)
            tubeNormals.append(radialNormals)
            
        # group tube points into triangles
        vertexPositionData = []
        vertexUVData = []
        vertexNormalData = []
        uvA, uvB, uvC, uvD = [0,0], [1,0], [1,1], [0,1]
        
        for n in range(lengthSegments-1):
            for r in range(radiusSegments):
                pA = tubePoints[n+0][r+0]
                pB = tubePoints[n+1][r+0]
                pC = tubePoints[n+1][r+1]
                pD = tubePoints[n+0][r+1]
                vertexPositionData += [pA,pB,pC, pA,pC,pD]
                vertexUVData += [uvA,uvB,uvC,uvA,uvC,uvD]
                nA = tubeNormals[n+0][r+0]
                nB = tubeNormals[n+1][r+0]
                nC = tubeNormals[n+1][r+1]
                nD = tubeNormals[n+0][r+1]
                vertexNormalData += [nA,nB,nC, nA,nC,nD]
            
        self.setAttribute("vec3", "vertexPosition", vertexPositionData)
        self.setAttribute("vec2", "vertexUV", vertexUVData)
        self.setAttribute("vec3", "vertexNormal", vertexNormalData)
        self.vertexCount = len(vertexPositionData)
