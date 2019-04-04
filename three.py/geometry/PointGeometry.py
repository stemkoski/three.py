from geometry import Geometry

class PointGeometry(Geometry):

    def __init__(self, vertexPositionData):
    
        super().__init__()
            
        self.setAttribute("vec3", "vertexPosition", vertexPositionData)
        
        self.vertexCount = len(vertexPositionData)