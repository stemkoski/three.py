from geometry import *
from math import pi, sin, cos, radians

class CylinderGeometry(SurfaceGeometry):
    def __init__(self, radiusTop = 1, radiusBottom = 1, radialSegments = 32, height=2, heightSegments = 2, circleTop=True, circleBottom=True):
        super().__init__(0, 2*pi, radialSegments,
                         0,    1, heightSegments,
                        lambda a,b : [ (b*radiusTop + (1-b)*radiusBottom)*cos(-a),
                                        (b-0.5)*height,
                                        (b*radiusTop + (1-b)*radiusBottom)*sin(-a) ] )

        vertexPositionData = self.attributeData["vertexPosition"]["value"]
        vertexUVData = self.attributeData["vertexUV"]["value"]
        vertexNormalData = self.attributeData["vertexNormal"]["value"]
        
        if circleTop:        
            angle = radians(360) / radialSegments
            posCenter = [0, height/2, 0]
            uvCenter = [0.5,0.5]
            normal = [0,1,0]
            for i in range(radialSegments):
                posA = [ radiusTop*cos(i*angle), height/2, radiusTop*sin(i*angle) ]
                posB = [ radiusTop*cos((i+1)*angle), height/2, radiusTop*sin((i+1)*angle) ]
                vertexPositionData.extend( [posCenter, posA, posB] )
                
                uvA = [ cos(i*angle)*0.5 + 0.5, sin(i*angle)*0.5 + 0.5 ]
                uvB = [ cos((i+1)*angle)*0.5 + 0.5, sin((i+1)*angle)*0.5 + 0.5 ]
                vertexUVData.extend( [uvCenter, uvA, uvB] )
                
                vertexNormalData.extend( [normal,normal,normal] )
                
        if circleBottom:        
            angle = radians(360) / radialSegments
            posCenter = [0, -height/2, 0]
            uvCenter = [0.5,0.5]
            normal = [0,-1,0]
            for i in range(radialSegments):
                posA = [ radiusBottom*cos(i*angle), -height/2, radiusBottom*sin(i*angle) ]
                posB = [ radiusBottom*cos((i+1)*angle), -height/2, radiusBottom*sin((i+1)*angle) ]
                vertexPositionData.extend( [posCenter, posA, posB] )
                
                uvA = [ cos(i*angle)*0.5 + 0.5, sin(i*angle)*0.5 + 0.5 ]
                uvB = [ cos((i+1)*angle)*0.5 + 0.5, sin((i+1)*angle)*0.5 + 0.5 ]
                vertexUVData.extend( [uvCenter, uvA, uvB] )
                
                vertexNormalData.extend( [normal,normal,normal] )
                
        self.vertexCount = len( vertexPositionData )
        
        self.setAttribute("vec3", "vertexPosition", vertexPositionData)
        self.setAttribute("vec2", "vertexUV", vertexUVData)
        self.setAttribute("vec3", "vertexNormal", vertexNormalData)
        

