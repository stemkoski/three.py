from math import sin, cos, pi
from core import *
from cameras import *
from geometry import *
from material import *

# this demo takes a while to start due to all the text images being generated
class TestViewports(Base):
    
    def initialize(self):

        self.w = 800
        self.h = 800
        
        self.setWindowTitle('Multiple Viewports')
        self.setWindowSize(self.w, self.h)

        self.renderer = Renderer()
        self.renderer.setViewportSize(self.w, self.h)
        self.renderer.setClearColor(1,1,1)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0, 5)
        
        starTexture  = OpenGLUtils.initializeTexture("images/stars.jpg")
        stars = Mesh( SphereGeometry(200, 64,64), SurfaceBasicMaterial(texture=starTexture) )
        self.scene.add(stars)

        sunTexture   = OpenGLUtils.initializeTexture("images/sun.jpg")
        earthTexture = OpenGLUtils.initializeTexture("images/earth.jpg")
        
        self.sun = Mesh( SphereGeometry(), SurfaceBasicMaterial(texture=sunTexture) )
        self.scene.add(self.sun)
        
        self.earth = Mesh( SphereGeometry(radius=0.5), SurfaceBasicMaterial(texture=earthTexture) )
        self.scene.add(self.earth)

        self.time = 0
        
        # HUD setup
        self.hudScene = Scene()
        self.hudCamera = OrthographicCamera(left=0, right=self.w, bottom=0, top=self.h)

        hudImage = TextImage(text=" Front View           ",
                          fontFileName="fonts/Souses.otf", fontSize=24,
                          fontColor=[255,255,255], transparent=True)
        hudTexture1 = OpenGLUtils.initializeSurface(hudImage.surface)
        self.quad1 = Sprite( SpriteMaterial( size=[hudImage.width, hudImage.height], anchor=[0,0], texture=hudTexture1) )
        self.quad1.transform.setPosition(0, 0)
        self.hudScene.add( self.quad1 )

        hudImage.text = " Top View "
        hudImage.renderImage()
        hudTexture2 = OpenGLUtils.initializeSurface(hudImage.surface)
        self.quad2 = Sprite( SpriteMaterial( size=[hudImage.width, hudImage.height], anchor=[0,0], texture=hudTexture2) )
        self.quad2.transform.setPosition(0, self.h/2+2)
        self.hudScene.add( self.quad2 )
        
        hudImage.text = " Right View "
        hudImage.renderImage()
        hudTexture3 = OpenGLUtils.initializeSurface(hudImage.surface)
        self.quad3 = Sprite( SpriteMaterial( size=[hudImage.width, hudImage.height], anchor=[0,0], texture=hudTexture3) )
        self.quad3.transform.setPosition(self.w/2+2, 0)
        self.hudScene.add( self.quad3 )

        hudImage.text = " User View "
        hudImage.renderImage()
        hudTexture4 = OpenGLUtils.initializeSurface(hudImage.surface)
        self.quad4 = Sprite( SpriteMaterial( size=[hudImage.width, hudImage.height], anchor=[0,0], texture=hudTexture4) )
        self.quad4.transform.setPosition(self.w/2+2, self.h/2+2)
        self.hudScene.add( self.quad4 )
        
    def update(self):

        if self.input.resize():
            size = self.input.getWindowSize()
            self.w = size["width"]
            self.h = size["height"]
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.hudCamera.setViewRegion( left=0, right=size["width"], bottom=0, top=size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        self.time += self.deltaTime
        
        self.sun.transform.rotateY(0.003, Matrix.LOCAL)
        self.earth.transform.rotateY(0.003, Matrix.LOCAL)
        self.earth.transform.setPosition( 2*cos(self.time), 0, 2*sin(self.time) )

        # viewport spacing chosen to leave a gap between rendering areas
        # do not clear the color buffer, otherwise previous renders disappear
        middleX = int(self.w / 2 + 2)
        middleY = int(self.h / 2 + 2)
        portWidth = int(self.w / 2 - 2)
        portHeight = int(self.h / 2 - 2)

        self.camera.transform.setPosition(0, 0, 7)
        self.camera.transform.lookAt(0,0,0)
        self.renderer.setViewport(0,0, portWidth,portHeight)
        self.renderer.render(self.scene, self.camera)

        self.camera.transform.setPosition(0, 7, 0.01)
        self.camera.transform.lookAt(0,0,0)
        self.renderer.setViewport(0,middleY, portWidth,portHeight)
        self.renderer.render(self.scene, self.camera, clearColor=False)

        self.camera.transform.setPosition(5, 5, 5)
        self.camera.transform.lookAt(0,0,0)
        self.renderer.setViewport(middleX,middleY, portWidth,portHeight)
        self.renderer.render(self.scene, self.camera, clearColor=False)

        self.camera.transform.setPosition(7, 0, 0)
        self.camera.transform.lookAt(0,0,0)
        self.renderer.setViewport(middleX,0, portWidth,portHeight)
        self.renderer.render(self.scene, self.camera, clearColor=False)

        # render the HUD
        self.quad1.transform.setPosition(0, 0)
        self.quad2.transform.setPosition(0, middleY)
        self.quad3.transform.setPosition(middleX, 0)
        self.quad4.transform.setPosition(middleX, middleY)
        self.renderer.setViewport(0,0, int(self.w),int(self.h))
        self.renderer.render(self.hudScene, self.hudCamera, clearColor=False)

# instantiate and run the program
TestViewports().run()

