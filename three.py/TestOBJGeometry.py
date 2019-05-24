from math import sin, cos

from core import *
from cameras import *
from lights import AmbientLight, DirectionalLight
from mathutils import *
from geometry import *
from material import *
from helpers import *

class TestOBJGeometry(Base):
    
    def initialize(self):

        self.setWindowTitle('OBJ Model Loader')
        self.setWindowSize(800,800)
        
        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)

        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 3, 7)
        self.camera.transform.lookAt( 0, 0, 0 )
        self.cameraControls = FirstPersonController(self.input, self.camera)
        
        ambientLight = AmbientLight(strength=0.25)
        directionalLight = DirectionalLight(direction=[-1,-1,-1])
        self.scene.add( ambientLight )
        self.scene.add( directionalLight )

        self.floorMesh = GridHelper(size=12, divisions=4, gridColor=[1,1,1], centerColor=[1,0,0])
        self.floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(self.floorMesh)
        
        mushroomTexture = OpenGLUtils.initializeTexture("models/mushroom.png")
        self.mushroom = Mesh(OBJGeometry("models/mushroom.obj", smoothNormals=True),
                             SurfaceLightMaterial(texture=mushroomTexture))
        self.mushroom.transform.translate(-3,0,0)
        self.mushroom.transform.scaleUniform(0.8)
        self.scene.add(self.mushroom)
        
        fireflowerTexture = OpenGLUtils.initializeTexture("models/fireflower.png")
        self.fireflower = Mesh(OBJGeometry("models/fireflower.obj", smoothNormals=False),
                               SurfaceLightMaterial(texture=fireflowerTexture))
        self.fireflower.transform.scaleUniform(0.0005)
        self.scene.add(self.fireflower)
        
        starTexture = OpenGLUtils.initializeTexture("models/star.png")
        self.star = Mesh(OBJGeometry("models/star.obj", smoothNormals=False),
                               SurfaceLightMaterial(texture=starTexture))
        self.star.transform.translate(3,0,0)
        self.star.transform.scaleUniform(0.0005)
        self.scene.add(self.star)
        
    def update(self):

        # update camera via keyboard
        self.cameraControls.update()

        self.mushroom.transform.rotateY(0.03, Matrix.LOCAL)
        self.fireflower.transform.rotateY(0.03, Matrix.LOCAL)
        self.star.transform.rotateY(0.03, Matrix.LOCAL)
        
        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestOBJGeometry().run()

