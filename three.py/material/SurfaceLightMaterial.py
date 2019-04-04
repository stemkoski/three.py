from core import *
from material import SurfaceBasicMaterial

class SurfaceLightMaterial(SurfaceBasicMaterial):
        
    def __init__(self, color=[1,1,1], alpha=1, texture=None, wireframe=False, lineWidth=1, useVertexColors=False, alphaTest=0):

        super().__init__(color=color, alpha=alpha, texture=texture, wireframe=wireframe, lineWidth=lineWidth, useVertexColors=useVertexColors, alphaTest=alphaTest)
        
        self.setUniform( "bool", "useLight", 1 )
