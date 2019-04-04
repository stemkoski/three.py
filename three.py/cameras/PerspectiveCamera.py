from cameras import Camera
from mathutils import MatrixFactory

class PerspectiveCamera(Camera):

    def __init__(self, fieldOfView=60, aspectRatio=1, nearDistance=0.1, farDistance=1000):
        super().__init__()
        self.fieldOfView = fieldOfView
        self.aspectRatio = aspectRatio
        self.nearDistance = nearDistance
        self.farDistance = farDistance
        self.projectionMatrix = MatrixFactory.makePerspective(self.fieldOfView, self.aspectRatio, self.nearDistance, self.farDistance)
    
    # call when resizing window/viewport
    def setAspectRatio(self, aspectRatio):
        self.aspectRatio = aspectRatio
        self.projectionMatrix = MatrixFactory.makePerspective(self.fieldOfView, self.aspectRatio, self.nearDistance, self.farDistance)
