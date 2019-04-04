from core import *
from geometry import *
from material import *

class AxesHelper(Mesh):

    def __init__(self, axisLength=1, lineWidth=4):
  
        vertexPositionData = [[0,0,0], [axisLength,0,0], [0,0,0], [0,axisLength,0], [0,0,0], [0,0,axisLength]]
        vertexColorData = [[0.5,0,0], [1,0.2,0.2], [0,0.5,0], [0.2,1,0.2], [0,0,0.5], [0.2,0.2,1]]

        geo = LineGeometry( vertexPositionData )
        geo.setAttribute("vec3", "vertexColor", vertexColorData)
        
        mat = LineSegmentMaterial(lineWidth=lineWidth, useVertexColors=True)
        # initialize the mesh
        super().__init__(geo, mat)
