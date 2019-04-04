from geometry import CylinderGeometry

class PrismGeometry(CylinderGeometry):
    def __init__(self, radius=1, numberSides=4, height=2, heightSegments = 1, closed=True):
        super().__init__(radiusTop=radius, radiusBottom=radius, radialSegments=numberSides, height=height, heightSegments=heightSegments, circleTop=True, circleBottom=True)