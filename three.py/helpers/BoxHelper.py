from core import *
from geometry import *
from material import *

class BoxHelper(Mesh):

    def __init__(self, baseMesh, lineColor=[1,0,0], lineWidth=2):

        if "vertexPosition" not in baseMesh.geometry.attributeData.keys():
            raise Exception("No vertexPosition attribute present in base mesh.")
    
        xMin = +999999
        yMin = +999999
        zMin = +999999
        xMax = -999999
        yMax = -999999
        zMax = -999999
        
        vertexPositionData = baseMesh.geometry.attributeData["vertexPosition"]["value"]
        for position in vertexPositionData:
            x,y,z = position
            if x > xMax:
                xMax = x 
            if y > yMax:
                yMax = y 
            if z > zMax:
                zMax = z 
            if x < xMin:
                xMin = x 
            if y < yMin:
                yMin = y 
            if z < zMin:
                zMin = z
        
        # add 12 pairs of points (line segments for cube)
        points = []
        # bottom square
        points.extend( [[xMin,yMin,zMin], [xMax,yMin,zMin]] )
        points.extend( [[xMin,yMin,zMin], [xMin,yMin,zMax]] )
        points.extend( [[xMin,yMin,zMax], [xMax,yMin,zMax]] )
        points.extend( [[xMax,yMin,zMin], [xMax,yMin,zMax]] )
        # vertical edges
        points.extend( [[xMin,yMin,zMin], [xMin,yMax,zMin]] )
        points.extend( [[xMax,yMin,zMin], [xMax,yMax,zMin]] )
        points.extend( [[xMin,yMin,zMax], [xMin,yMax,zMax]] )
        points.extend( [[xMax,yMin,zMax], [xMax,yMax,zMax]] )
        # top square
        points.extend( [[xMin,yMax,zMin], [xMax,yMax,zMin]] )
        points.extend( [[xMax,yMax,zMin], [xMax,yMax,zMax]] )
        points.extend( [[xMax,yMax,zMax], [xMin,yMax,zMax]] )
        points.extend( [[xMin,yMax,zMax], [xMin,yMax,zMin]] )
        
        geo = LineGeometry(points)
        
        mat = LineSegmentMaterial(color=lineColor, lineWidth=lineWidth)
        
        # initialize the mesh
        super().__init__(geo, mat)
        
        # link up transformation of this mesh and original mesh
        self.transform = baseMesh.transform
