from geometry import SphereGeometry

class OctahedronGeometry(SphereGeometry):

    def __init__(self, radius=1):
        super().__init__(radius=radius, xResolution=4, yResolution=2)
