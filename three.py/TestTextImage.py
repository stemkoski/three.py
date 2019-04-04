from core import *
from cameras import *
from geometry import *
from material import *
from lights import *

class TestTextImage(Base):
    
    def initialize(self):

        self.setWindowTitle('Text Images and HUD Text')
        self.setWindowSize(600,600)

        self.renderer = Renderer()
        self.renderer.setViewportSize(600,600)
        self.renderer.setClearColor(0.75,0.75,0.75)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 5)
        self.camera.transform.lookAt(0, 0, 0)        
        self.cameraControls = FirstPersonController(self.input, self.camera)

        self.scene.add( AmbientLight(strength=0.25) )
        self.scene.add( DirectionalLight(direction=[-1,-1,-1]) )

        messageImage = TextImage(text="Hello, World!",
                                 fontFileName="fonts/Souses.otf", fontSize=36,
                                 fontColor=[50,0,0], backgroundColor=[200,200,255],
                                 width=256, height=256,
                                 alignHorizontal="CENTER", alignVertical="MIDDLE")
        messageTexture = OpenGLUtils.initializeSurface(messageImage.surface)
        lightMaterial = SurfaceLightMaterial( texture=messageTexture )
        self.cube = Mesh( BoxGeometry(), lightMaterial )
        self.scene.add(self.cube)        

        # set up the HUD (heads-up display)
        self.hudScene = Scene()
        self.hudCamera = OrthographicCamera(left=0, right=600, bottom=0, top=600)

        hudImage = TextImage(text="This is a test of HUD text.",
                          fontFileName="fonts/Souses.otf", fontSize=28,
                          transparent=True)
        hudTexture = OpenGLUtils.initializeSurface(hudImage.surface)
        quad = Sprite( SpriteMaterial( size=[hudImage.width, hudImage.height], anchor=[0,0], texture=hudTexture) )
        quad.transform.setPosition(5,5)
        self.hudScene.add( quad )
        
    def update(self):
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.hudCamera.setViewRegion( left=0, right=size["width"], bottom=0, top=size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
                
        self.cube.transform.rotateX(0.005, Matrix.LOCAL)
        self.cube.transform.rotateY(0.01, Matrix.LOCAL)
        
        self.renderer.render(self.scene, self.camera)

        self.renderer.render(self.hudScene, self.hudCamera, clearColor=False)

# instantiate and run the program
TestTextImage().run()

