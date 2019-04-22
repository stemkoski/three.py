from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

class TestShadows(Base):
    
    def initialize(self):

        self.setWindowTitle('Test')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.5,0.5,0.75)
        self.renderer.shadowMapEnabled = True
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 5)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        self.scene.add( AmbientLight(strength=0.25) )
        directionalLight = DirectionalLight(position=[2,2,0], direction=[-1,-1,-1])
        directionalLight.castShadow = True
        self.scene.add( directionalLight )
        self.scene.add( DirectionalLightHelper(directionalLight) )


        gridTexture  = OpenGLUtils.initializeTexture("images/color-grid.png")
        gridMaterial = SurfaceLightMaterial(texture=gridTexture)

        floor = Mesh( BoxGeometry(10,0.1,10), gridMaterial )
        floor.receiveShadow = True
        self.scene.add( floor )

        self.box = Mesh( BoxGeometry(1,1,1), gridMaterial )
        self.box.transform.setPosition(0,1,0)
        self.box.castShadow = True
        self.scene.add( self.box )
        
    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestShadows().run()

