from OpenGL.GL import *
from core import OpenGLUtils
from material import LineBasicMaterial

class LineDashedMaterial(LineBasicMaterial):
        
    def __init__(self, color=[0,0,0], alpha=1, lineWidth=4, dashLength=0.50, gapLength=0.25, useVertexColors=False):

        super().__init__(color=color, alpha=alpha, lineWidth=lineWidth, useVertexColors=useVertexColors)

        self.setUniform( "bool", "useDashes", 1 )
        self.setUniform( "float", "dashLength", dashLength )
        self.setUniform( "float", "gapLength", gapLength )
