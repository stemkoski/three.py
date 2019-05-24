from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

class TestRenderTarget(Base):
    
    def initialize(self):

        self.setWindowTitle('Render Target')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 5)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        skyTexture  = OpenGLUtils.initializeTexture("images/skysphere.jpg")
        sky = Mesh( SphereGeometry(200, 64,64), SurfaceBasicMaterial(texture=skyTexture) )
        self.scene.add(sky)

        gridTexture = OpenGLUtils.initializeTexture("images/color-grid.png")
        self.sphere = Mesh( SphereGeometry(), SurfaceBasicMaterial(texture=gridTexture) )
        self.sphere.transform.setPosition(-1.2,0,0)
        self.scene.add(self.sphere)
        
        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0], lineWidth=2)
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)

        self.skycam = PerspectiveCamera()
        self.skycam.transform.setPosition(0, 5, 2)
        self.skycam.transform.lookAt(0,0,0)
        self.renderTarget = RenderTarget.RenderTarget(2048,2048)
        self.quad = Mesh( QuadGeometry(), SurfaceBasicMaterial(texture=self.renderTarget.textureID) )
        self.quad.transform.setPosition(1.2,0,0)
        self.scene.add( self.quad )
        
    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        self.sphere.transform.rotateY(0.002, Matrix.LOCAL)

        self.renderer.render(self.scene, self.skycam, self.renderTarget)
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestRenderTarget().run()

