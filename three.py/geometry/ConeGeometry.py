from geometry import CylinderGeometry

class ConeGeometry(CylinderGeometry):
    def __init__(self, radius=1, radialSegments=32, height=2, heightSegments = 2, closed=True):
        super().__init__(radiusTop=0.0001, radiusBottom=radius, radialSegments=radialSegments, height=height, heightSegments=heightSegments, circleTop=False, circleBottom=closed)