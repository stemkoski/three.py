from geometry import Geometry
from math import sin, cos, pi, radians

class RingGeometry(Geometry):

    def __init__(self, innerRadius=0.25, outerRadius=1, segments=32):

        super().__init__()
        
        vertexPositionData = []
        vertexUVData = []
        vertexNormalData = []
        
        angle = radians(360) / segments
        normal = [0,0,1]
        for i in range(segments):
            posA = [ innerRadius*cos(i*angle), innerRadius*sin(i*angle), 0 ]
            posB = [ outerRadius*cos(i*angle), outerRadius*sin(i*angle), 0 ]
            posC = [ outerRadius*cos((i+1)*angle), outerRadius*sin((i+1)*angle), 0 ]
            posD = [ innerRadius*cos((i+1)*angle), innerRadius*sin((i+1)*angle), 0 ]
            vertexPositionData.extend( [posA,posB,posC, posA,posC,posD] )
            
            uvA = [ innerRadius*cos(i*angle)*0.5 + 0.5, innerRadius*sin(i*angle)*0.5 + 0.5 ]
            uvB = [ outerRadius*cos(i*angle)*0.5 + 0.5, outerRadius*sin(i*angle)*0.5 + 0.5 ]
            uvC = [ outerRadius*cos((i+1)*angle)*0.5 + 0.5, outerRadius*sin((i+1)*angle)*0.5 + 0.5 ]
            uvD = [ innerRadius*cos((i+1)*angle)*0.5 + 0.5, innerRadius*sin((i+1)*angle)*0.5 + 0.5 ]
            vertexUVData.extend( [uvA,uvB,uvC, uvA,uvC,uvD] )
            
            vertexNormalData.extend( [normal,normal,normal, normal,normal,normal] )
        
        self.setAttribute("vec3", "vertexPosition", vertexPositionData)
        self.setAttribute("vec2", "vertexUV", vertexUVData)
        self.setAttribute("vec3", "vertexNormal", vertexNormalData)
        
        self.vertexCount = len(vertexPositionData)
        

