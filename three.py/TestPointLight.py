from core import *
from cameras import *
from geometry import *
from material import *
from lights import *
from helpers import *

class TestPointLight(Base):
    
    def initialize(self):

        self.setWindowTitle('Point Light')
        self.setWindowSize(800,800)
        
        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)

        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0, 4)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        ambientLight = AmbientLight(color=[1,1,1], strength=0.25)
        self.scene.add( ambientLight )

        moonTexture  = OpenGLUtils.initializeTexture("images/moon.jpg")
        moon = Mesh( SphereGeometry(), SurfaceLightMaterial( color=[1,1,1], texture=moonTexture ) )
        self.scene.add(moon)        

        self.redLight = PointLight(color=[1,0,0], position=[1,1,1])
        self.scene.add( self.redLight )
        self.scene.add( PointLightHelper(self.redLight, radius=0.1) )

        self.greenLight = PointLight(color=[0,1,0], position=[1,-1,-1])
        self.scene.add( self.greenLight )
        self.scene.add( PointLightHelper(self.greenLight, radius=0.1) )

        self.blueLight = PointLight(color=[0,0,1], position=[-1,1,-1])
        self.scene.add( self.blueLight )
        self.scene.add( PointLightHelper(self.blueLight, radius=0.1) )
        
    def update(self):
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        self.redLight.transform.rotateX(0.013, Matrix.GLOBAL)
        self.redLight.transform.rotateY(0.007, Matrix.GLOBAL)

        self.greenLight.transform.rotateX(-0.009, Matrix.GLOBAL)
        self.greenLight.transform.rotateY(0.011, Matrix.GLOBAL)

        self.blueLight.transform.rotateX(0.017, Matrix.GLOBAL)
        self.blueLight.transform.rotateY(-0.015, Matrix.GLOBAL)
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestPointLight().run()

