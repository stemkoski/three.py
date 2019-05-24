from core import Mesh
from geometry import LineGeometry
from material import LineSegmentMaterial

from cameras import OrthographicCamera

class OrthographicCameraHelper(Mesh):

    def __init__(self, orthoCamera, lineColor=[0.5, 0, 0], lineWidth=3):

        xMin = orthoCamera.left
        xMax = orthoCamera.right
        yMin = orthoCamera.bottom
        yMax = orthoCamera.top
        zMin = -orthoCamera.near
        zMax = -orthoCamera.far
        
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
        self.transform = orthoCamera.transform
