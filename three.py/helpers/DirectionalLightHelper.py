from core import *
from geometry import *
from material import *
import numpy as np

class DirectionalLightHelper(Mesh):

    def __init__(self, directionalLight, planeSize=0.5, color=None, lineWidth=1):
  
        vertexPositionData = []
        
        if color is None:
            color = directionalLight.color
        vertexColorData = []
        
        # position = np.array( directionalLight.transform.getPosition() )
        direction = np.array( directionalLight.direction )
        
        scale = 100
        vertexPositionData.append( [0,0,0] )
        vertexPositionData.append( [direction[0] * scale, direction[1] * scale, direction[2] * scale] ) 
        
        n = np.cross( direction, [3.41, 1.26, 2.57] )
        b = np.cross( direction, n )
        
        n = n / np.linalg.norm(n)
        b = b / np.linalg.norm(b)
        
        # build a square (4 segments) perpendicular to direction line
        vertexPositionData.append( n*planeSize + b*planeSize )
        vertexPositionData.append( n*planeSize - b*planeSize )
        vertexPositionData.append( n*planeSize - b*planeSize )
        vertexPositionData.append( -n*planeSize - b*planeSize )
        vertexPositionData.append( -n*planeSize - b*planeSize )
        vertexPositionData.append( -n*planeSize + b*planeSize )
        vertexPositionData.append( -n*planeSize + b*planeSize )
        vertexPositionData.append( n*planeSize + b*planeSize )
        for i in range(10):
            vertexColorData.append( color )
        
        # build a cross (2 segments) within the square
        vertexPositionData.append( b*planeSize )
        vertexPositionData.append( -b*planeSize )
        vertexPositionData.append( n*planeSize )
        vertexPositionData.append( -n*planeSize )
        for i in range(4):
            vertexColorData.append( [0.25,0.25,0.25] )
        
        geo = LineGeometry(vertexPositionData)
        geo.setAttribute("vec3", "vertexColor", vertexColorData)
        
        mat = LineSegmentMaterial()
        mat.setUniform( "bool", "useVertexColors", 1 )
        mat.lineWidth = lineWidth
        
        # initialize the mesh
        super().__init__(geo, mat)
        
        # link up transformation of this mesh and original mesh
        self.transform = directionalLight.transform
