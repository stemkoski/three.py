from geometry import CircleGeometry

class PolygonGeometry(CircleGeometry):

    def __init__(self, radius=1, numberSides=6):
        super().__init__(radius=radius, segments=numberSides)
        