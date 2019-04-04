from core import Mesh
from geometry import Geometry

class Sprite(Mesh):

    def __init__(self, material):
    
        geometry = Geometry()
        # position and UV data are the same
        vertexData = [[0,0], [1,0], [1,1], [0,0], [1,1], [0,1]]
        geometry.setAttribute("vec2", "vertexData", vertexData)
        geometry.vertexCount = 6
        
        super().__init__(geometry, material)
        