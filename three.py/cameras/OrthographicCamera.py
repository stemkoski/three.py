from cameras import Camera
from mathutils import MatrixFactory

class OrthographicCamera(Camera):

    def __init__(self, left=-1, right=1, top=1, bottom=-1, near=1, far=-1):
        super().__init__()
        self.setViewRegion(left, right, top, bottom, near, far)
    
    # call when resizing window/viewport
    def setViewRegion(self, left=-1, right=1, top=1, bottom=-1, near=1, far=-1):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.near = near
        self.far = far
        self.projectionMatrix = MatrixFactory.makeOrthographic(left, right, top, bottom, near, far)
        