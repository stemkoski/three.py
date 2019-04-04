from geometry import ConeGeometry

class PyramidGeometry(ConeGeometry):
    def __init__(self, radius=1, numberSides=4, height=2, heightSegments = 8, closed=True):
        super().__init__(radius=radius, radialSegments=numberSides, height=height, heightSegments=heightSegments, closed=closed)