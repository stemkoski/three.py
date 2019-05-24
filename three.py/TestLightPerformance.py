from core import *
from cameras import *
from lights import AmbientLight, DirectionalLight
from geometry import *
from material import *
from helpers import *

import random

class TestLightPerformance(Base):
    
    def initialize(self):

        self.setWindowTitle('Lots of Dynamically Lit Cubes')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)

        # self.renderer.setFog( Fog(startDistance=2, endDistance=20, color=[0,0,0.15]) )
        
        self.scene = Scene()

        self.scene.add( AmbientLight(strength=0.25) )
        self.scene.add( DirectionalLight(direction=[-1,-1,0], color=[1,0,0]) )
        self.scene.add( DirectionalLight(direction=[1,1,0], color=[0,0,1]) )
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0, 15)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        self.boxList = []

        boxGeo = BoxGeometry(width=1, height=1, depth=1)
        boxTexture = OpenGLUtils.initializeTexture("images/color-grid.png")
        boxMat = SurfaceLightMaterial(texture=boxTexture)

        for i in range(100):            
            box = Mesh(boxGeo, boxMat)
            box.transform.setPosition(
                random.uniform(-5,5),random.uniform(-5,5),random.uniform(10,-10))
            box.transform.rotateX( random.uniform(0,6.28), Matrix.LOCAL )
            box.transform.rotateY( random.uniform(0,6.28), Matrix.LOCAL )
            self.scene.add(box)
            self.boxList.append(box)
            
    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        for box in self.boxList:
            box.transform.rotateY(0.02, Matrix.LOCAL)
            box.transform.rotateX(0.03, Matrix.LOCAL)
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestLightPerformance().run()

