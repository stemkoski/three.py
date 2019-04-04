from core import *
from geometry import *
from material import *
import numpy as np

class PointLightHelper(Mesh):

    def __init__(self, pointLight, radius=0.5, color=None, lineWidth=1):
  
        geo = IcosahedronGeometry(radius)
        
        # if no color specified, use the light color
        if color is None:
            color = pointLight.color

        mat = SurfaceBasicMaterial(color=color, wireframe=True, lineWidth=lineWidth)
        
        # initialize the mesh
        super().__init__(geo, mat)
        
        # link up transformation of this mesh and original mesh
        self.transform = pointLight.transform
