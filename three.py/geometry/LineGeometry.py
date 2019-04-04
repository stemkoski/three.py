from geometry import *
import numpy as np

class LineGeometry(Geometry):

    def __init__(self, vertexPositionData):
        super().__init__()
            
        self.setAttribute("vec3", "vertexPosition", vertexPositionData)

        # calculate arclength parameters; used by LineDashedMaterial
        vertexCount = len(vertexPositionData)
        totalArcLength = 0
        vertexArcLengthData = [0]
        for index in range( 1, vertexCount ):
            segmentLength = np.linalg.norm( np.subtract(vertexPositionData[index], vertexPositionData[index-1]) )
            totalArcLength += segmentLength
            vertexArcLengthData.append( totalArcLength )
            
        self.setAttribute("float", "vertexArcLength", vertexArcLengthData)
        
        self.vertexCount = len(vertexPositionData)