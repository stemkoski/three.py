from geometry import *

class CurveGeometry(LineGeometry):

    def __init__(self, curve):
        super().__init__( curve.getPoints() )
            