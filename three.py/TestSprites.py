from math import sin, cos, pi
from core import *
from cameras import *
from geometry import *
from material import *
import colorsys

class TestSprites(Base):
    
    def initialize(self):

        self.setWindowTitle('Sprites')
        self.setWindowSize(800,800)
        
        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)

        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 5)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        gridTexture  = OpenGLUtils.initializeTexture("images/color-grid.png")
        floorMesh = Mesh( QuadGeometry(width=10, height=10),
                          SurfaceBasicMaterial(texture=gridTexture))
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)

        circleTexture  = OpenGLUtils.initializeTexture("images/circle-white.png")

        self.spriteContainer = Object3D()
        self.spriteContainer.transform.translate(0,1.25,0)
        
        self.scene.add( self.spriteContainer )
        # generate sprites with different material colors
        for i in range(16):
            color = colorsys.hsv_to_rgb(i/16,1,1)
            spriteMaterial = SpriteMaterial( size=[0.5,0.5], texture=circleTexture, color=color, alphaTest=0.25)
            sprite = Sprite( spriteMaterial )
            angle = 2 * pi * i / 16
            sprite.transform.setPosition(cos(angle), 0.75, sin(angle))
            self.spriteContainer.add(sprite)
        
    def update(self):
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
                
        self.spriteContainer.transform.rotateX(0.015, Matrix.LOCAL)
        self.spriteContainer.transform.rotateY(0.019, Matrix.LOCAL)
        self.spriteContainer.transform.rotateZ(-0.011, Matrix.LOCAL)
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestSprites().run()

