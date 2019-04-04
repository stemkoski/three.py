from geometry import Geometry
from math import sqrt, atan2, pi
import numpy as np

class IcosahedronGeometry(Geometry):

    def __init__(self, radius=1):
        super().__init__()
        
        vertexPositionData = []
        vertexUVData = []
        vertexNormalData = []
        
        t = ( 1 + sqrt( 5 ) ) / 2

        v = [ [-1,t,0], [1,t,0], [-1,-t,0], [1,-t,0], [0,-1,t], [0,1,t], 
              [0,-1,-t], [0,1,-t], [t,0,-1], [t,0,1], [-t,0,-1], [-t,0,1] ]

        triangleData = [ 
            v[0],v[11],v[5], v[0],v[5],v[1],  v[0],v[1],v[7],   v[0],v[7],v[10],  v[0],v[10],v[11],
            v[1],v[5],v[9],  v[5],v[11],v[4], v[11],v[10],v[2], v[10],v[7],v[6],  v[7],v[1],v[8],
            v[3],v[9],v[4],  v[3],v[4],v[2],  v[3],v[2],v[6],   v[3],v[6],v[8],   v[3],v[8],v[9],
            v[4],v[9],v[5],  v[2],v[4],v[11], v[6],v[2],v[10],  v[8],v[6],v[7],   v[9],v[8],v[1] ]
            
        # calculate data
        for index in range( len(triangleData) ):
            w = triangleData[index]
            normal = np.divide( w, np.linalg.norm(w) )
            x,y,z = normal
            u = atan2(x, z) / (2*pi) + 0.5
            v = y * 0.5 + 0.5
            uv = [u,v]
            position = np.multiply( normal, radius )

            vertexPositionData.append( position )
            vertexUVData.append( uv )
            vertexNormalData.append( normal )

        self.setAttribute("vec3", "vertexPosition", vertexPositionData)
        self.setAttribute("vec2", "vertexUV", vertexUVData)
        self.setAttribute("vec3", "vertexNormal", vertexNormalData)
        
        self.vertexCount = len(vertexPositionData)
        