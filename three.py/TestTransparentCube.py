from core import *
from cameras import *
from geometry import *
from material import *

class TestTransparentCube(Base):
    
    def initialize(self):

        self.setWindowTitle('Transparent Cube')
        self.setWindowSize(800,800)
        
        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)

        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0, 7)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        # note: add meshes back-to-front
        gridTexture  = OpenGLUtils.initializeTexture("images/color-grid.png")
        gridMaterial = SurfaceBasicMaterial(texture=gridTexture)

        floorMesh = Mesh( QuadGeometry(10,10), gridMaterial )
        self.scene.add(floorMesh)

        boxGeo = BoxGeometry(1,1,1)
        
        textureOuter  = OpenGLUtils.initializeTexture("images/border-black.png")
        materialOuter = SurfaceBasicMaterial(texture=textureOuter)
        materialOuter.renderBack = False

        textureInner  = OpenGLUtils.initializeTexture("images/border-dotted.png")
        materialInner = SurfaceBasicMaterial(texture=textureInner)
        materialInner.renderFront = False
        
        self.cubeMesh1 = Mesh( boxGeo, materialOuter )
        self.cubeMesh1.transform.translate(-2, 0, 2, Matrix.LOCAL)        
        self.scene.add(self.cubeMesh1)

        self.cubeMesh2 = Mesh( boxGeo, materialInner )
        self.cubeMesh2.transform.translate(0, 0, 2, Matrix.LOCAL)        
        self.scene.add(self.cubeMesh2)

        self.cubeMeshInner = Mesh( boxGeo, materialInner )
        self.cubeMeshInner.transform.translate(2, 0, 2, Matrix.LOCAL)        
        self.scene.add(self.cubeMeshInner)

        self.cubeMeshOuter = Mesh( boxGeo, materialOuter )
        self.cubeMeshOuter.transform.translate(2, 0, 2, Matrix.LOCAL)        
        self.scene.add(self.cubeMeshOuter)
        


    def update(self):
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
            
        self.cubeMesh1.transform.rotateX(0.02, Matrix.LOCAL)
        self.cubeMesh1.transform.rotateY(0.03, Matrix.LOCAL)

        self.cubeMesh2.transform.rotateX(0.02, Matrix.LOCAL)
        self.cubeMesh2.transform.rotateY(0.03, Matrix.LOCAL)

        self.cubeMeshInner.transform.rotateX(0.02, Matrix.LOCAL)
        self.cubeMeshInner.transform.rotateY(0.03, Matrix.LOCAL)
        self.cubeMeshOuter.transform.rotateX(0.02, Matrix.LOCAL)
        self.cubeMeshOuter.transform.rotateY(0.03, Matrix.LOCAL)

        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestTransparentCube().run()

