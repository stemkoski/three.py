from core import *
from lights import AmbientLight, DirectionalLight
from cameras import *
from geometry import *
from material import *
from helpers import *

class TestHelpers(Base):
    
    def initialize(self):

        self.setWindowTitle('Helpers')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 5)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        self.scene.add( AmbientLight(strength=0.25) )
        directionalLight = DirectionalLight(direction=[-1,-1,-1], position=[3,4,-3])
        self.scene.add( directionalLight )
        self.scene.add( DirectionalLightHelper(directionalLight) )
        
        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)
        
        gridTexture  = OpenGLUtils.initializeTexture("images/color-grid.png")
        gridMaterial = SurfaceLightMaterial(texture=gridTexture)
        self.cylinder = Mesh( CylinderGeometry(radiusTop=0.25, radiusBottom=1, heightSegments=6), gridMaterial )
        self.cylinder.transform.translate(0, 1, 0, Matrix.LOCAL)
        self.scene.add(self.cylinder)

        self.cylinder.add( AxesHelper(axisLength=2, lineWidth=4) )
        
        self.scene.add( BoxHelper(self.cylinder, lineColor=[1,1,0], lineWidth=4) )
        self.scene.add( VertexNormalHelper(self.cylinder, lineLength=0.25, lineColor=[0.5,0.5,1], lineWidth=2) )
        
    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        self.cylinder.transform.rotateX(0.015, Matrix.LOCAL)
        self.cylinder.transform.rotateY(0.008, Matrix.LOCAL)
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestHelpers().run()

