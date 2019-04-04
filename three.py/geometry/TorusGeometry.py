from geometry import SurfaceGeometry
from math import pi, cos, sin

class TorusGeometry(SurfaceGeometry):
    def __init__(self, centralRadius=0.60, tubeRadius=0.40 , tubularSegments=32, radialSegments=10, scale=1):
        super().__init__(0, 2*pi, tubularSegments,
                         0, 2*pi, radialSegments,
                         lambda u,v: [((centralRadius + tubeRadius*cos(v))*cos(u)*scale),
                                      ((centralRadius + tubeRadius*cos(v))*sin(u)*scale),
                                      (tubeRadius*sin(v)*scale)] )
