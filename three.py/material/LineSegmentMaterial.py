from core import *
from material import *

class LineSegmentMaterial(LineBasicMaterial):
        
    def __init__(self, color=[0,0,0], alpha=1, lineWidth=4, useVertexColors=False):

        super().__init__(color=color, alpha=alpha, lineWidth=lineWidth, useVertexColors=useVertexColors)
        
        self.drawStyle = GL_LINES
        
