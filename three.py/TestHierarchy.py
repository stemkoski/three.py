from math import sin, cos, pi, radians
from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

class TestHierarchy(Base):
    
    def initialize(self):

        self.setWindowTitle('Hierarchy (Solar System)')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 3, 9)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)
        
        starTexture  = OpenGLUtils.initializeTexture("images/stars.jpg")
        sunTexture   = OpenGLUtils.initializeTexture("images/sun.jpg")
        earthTexture = OpenGLUtils.initializeTexture("images/earth.jpg")
        moonTexture  = OpenGLUtils.initializeTexture("images/moon.jpg")

        sphere = SphereGeometry()
        
        stars = Mesh( SphereGeometry(200, 64,64), SurfaceBasicMaterial(texture=starTexture) )
        self.scene.add(stars)

        self.sunGroup = Object3D()
        self.sunGroup.add( AxesHelper(2) )
        self.sunGroup.transform.setPosition(0,1,0)
        self.scene.add( self.sunGroup )
        
        self.sun = Mesh( SphereGeometry(1), SurfaceBasicMaterial(texture=sunTexture) )
        self.sunGroup.add( self.sun )

        self.earthGroup = Object3D()
        self.earthGroup.add( AxesHelper(1) )
        self.earthGroup.transform.translate(2,0,0, Matrix.GLOBAL)
        self.sunGroup.add( self.earthGroup )
        
        self.earth = Mesh( SphereGeometry(0.5), SurfaceBasicMaterial(texture=earthTexture) )
        self.earthGroup.add(self.earth) 
        
        self.moon = Mesh( SphereGeometry(0.25), SurfaceBasicMaterial(texture=moonTexture) )
        self.earthGroup.add(self.moon)            
        
        self.time = 0

    def update(self):
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"] / size["height"] )
            self.renderer.setViewportSize( size["width"] , size["height"] )
            
        self.sun.transform.rotateY( radians(-0.11) )
        self.earth.transform.rotateY( radians(-0.41) )
        self.moon.transform.rotateY( radians(-2.3) )

        self.time += self.deltaTime
        
        earthOrbitDistance = 4.0
        earthOrbitDuration = 12
        earthX = earthOrbitDistance * cos(self.time * 2 * pi / earthOrbitDuration)
        earthZ = earthOrbitDistance * sin(self.time * 2 * pi / earthOrbitDuration)
        self.earthGroup.transform.setPosition( earthX, 0, earthZ )

        moonOrbitDistance = 1.0
        moonOrbitDuration = 3
        moonX = moonOrbitDistance * cos(self.time * 2 * pi / moonOrbitDuration)
        moonZ = moonOrbitDistance * sin(self.time * 2 * pi / moonOrbitDuration)
        self.moon.transform.setPosition( moonX, 0, moonZ )
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestHierarchy().run()

