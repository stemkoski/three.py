from core import *
from geometry import *
from material import *

class VertexNormalHelper(Mesh):

    def __init__(self, baseMesh, lineLength=0.5, lineColor=[1,0,0], lineWidth=2):

        if "vertexNormal" not in baseMesh.geometry.attributeData.keys():
            raise Exception("No vertexNormal attribute present in base mesh.")
    
        points = []
        count = len( baseMesh.geometry.attributeData["vertexPosition"]["value"] )        
            
        for index in range(count):
            startPoint = baseMesh.geometry.attributeData["vertexPosition"]["value"][index]
            points.append( startPoint )
                
            normal = baseMesh.geometry.attributeData["vertexNormal"]["value"][index]
            c = np.linalg.norm( np.array(normal) )
            endPoint = np.array(startPoint) + np.array(normal) * lineLength / c
            endPoint = list(endPoint) # convert back to list structure
            points.append( endPoint )
            
        geo = LineGeometry(points)
        
        mat = LineSegmentMaterial(color=lineColor, lineWidth=lineWidth)
        
        # initialize the mesh
        super().__init__(geo, mat)
        
        # link up transformation of this mesh and original mesh
        self.transform = baseMesh.transform
