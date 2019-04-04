from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

# Note: FirstPersonControls can be attached to any Object3D
class TestFirstPersonControls(Base):
    
    def initialize(self):

        self.setWindowTitle('First Person Controls')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0.5, 5)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)
        self.cameraControls.setSpeed(unitsPerSecond=0.5, degreesPerSecond=15)

        skyTexture  = OpenGLUtils.initializeTexture("images/skysphere.jpg")
        sky = Mesh( SphereGeometry(200, 64,64), SurfaceBasicMaterial(texture=skyTexture) )
        self.scene.add(sky)
        
        floorMesh = GridHelper(size=20, divisions=100, gridColor=[0,0,0], centerColor=[1,0,0])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)
        
    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestFirstPersonControls().run()

