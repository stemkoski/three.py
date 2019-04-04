import pygame
from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

class TestParticleEngine(Base):
    
    def initialize(self):

        self.setWindowTitle('Particle Engine')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 3)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        
        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)

        particleTexture = OpenGLUtils.initializeTexture("images/particle-star.png")

        # rainbow star fountain!
        self.engine = ParticleEngine(style="box",
                             emitterDeathAge=600, particleDeathAge=4,
                             particlesPerSecond=200,
                             positionBase=[0,0,0], positionSpread=[0,0,0],
                             velocityBase=[0,1,0], velocitySpread=[0.4,0.1,0.4],
                             gravity=[0,-0.5,0],
                             colorBase=[0.5,1,1], colorSpread=[0.5,1,1],
                             colorTween = Tween(timeList=[0,4], valueType="vec3", valueList=[ [0,1,1], [0.9,1,1] ]),
                             sizeTween = Tween(timeList=[0,0.5,3,4], valueList=[0,0.20,0.20,0]),
                             additiveBlending=False,
                             particleTexture=particleTexture)

        self.engine.transform.translate(0,0,0)
        
        self.scene.add(self.engine)
        
    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        if self.input.isKeyDown(pygame.K_s):
            self.engine.stop()

        if self.input.isKeyDown(pygame.K_r):
            self.engine.reset()


        self.engine.update( self.deltaTime )
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestParticleEngine().run()

