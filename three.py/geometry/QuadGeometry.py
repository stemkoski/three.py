from geometry import *

class QuadGeometry(SurfaceGeometry):

    def __init__(self, width=2, height=2, widthResolution=4, heightResolution=4):
    
        super().__init__(  -width/2,  width/2, widthResolution, 
                          -height/2, height/2, heightResolution, 
                          lambda u,v : [u, v, 0] )
