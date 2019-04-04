from math import sin, cos, pi, radians
from geometry import Geometry

# TODO: self contained version
class CircleGeometry(Geometry):

    def __init__(self, radius=1, segments=32):
    
        super().__init__()
        vertexPositionData = []
        vertexUVData = []
        vertexNormalData = []
        
        angle = radians(360) / segments
        posCenter = [0,0,0]
        uvCenter = [0.5,0.5]
        normal = [0,0,1]
        for i in range(segments):
            posA = [ radius*cos(i*angle), radius*sin(i*angle), 0 ]
            posB = [ radius*cos((i+1)*angle), radius*sin((i+1)*angle), 0 ]
            vertexPositionData.extend( [posCenter, posA, posB] )
            
            uvA = [ cos(i*angle)*0.5 + 0.5, sin(i*angle)*0.5 + 0.5 ]
            uvB = [ cos((i+1)*angle)*0.5 + 0.5, sin((i+1)*angle)*0.5 + 0.5 ]
            vertexUVData.extend( [uvCenter, uvA, uvB] )
            
            vertexNormalData.extend( [normal,normal,normal] )
        
        self.setAttribute("vec3", "vertexPosition", vertexPositionData)
        self.setAttribute("vec2", "vertexUV", vertexUVData)
        self.setAttribute("vec3", "vertexNormal", vertexNormalData)
        
        self.vertexCount = len(vertexPositionData)    