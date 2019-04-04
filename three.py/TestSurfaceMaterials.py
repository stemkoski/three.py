from core import *
from cameras import *
from geometry import *
from material import *
from lights import *
from random import random

class TestSurfaceMaterials(Base):
    
    def initialize(self):

        self.setWindowTitle('Surface Materials')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0, 8)
        self.cameraControls = FirstPersonController(self.input, self.camera)
        
        self.scene.add( AmbientLight( strength=0.2 ) )
        self.scene.add( DirectionalLight( direction=[-1,-1,-2] ) )

        self.sphereList = []

        sphereGeom = SphereGeometry(radius=0.9)
        
        gridTexture  = OpenGLUtils.initializeTexture("images/color-grid.png")
        gridMaterial = SurfaceLightMaterial(texture=gridTexture)

        wireMaterial = SurfaceBasicMaterial(color=[0.8,0.8,0.8], wireframe=True, lineWidth=2)

        lightMaterial = SurfaceLightMaterial(color=[0.5,0.5,1.0])
        
        rainbowMaterial = SurfaceLightMaterial(useVertexColors=True)
        vertexColorData = []
        for i in range(sphereGeom.vertexCount):
            color = [random(), random(), random()]
            vertexColorData.append(color)
        sphereGeom.setAttribute("vec3", "vertexColor", vertexColorData)
        
        sphere1 = Mesh( sphereGeom, wireMaterial )
        sphere1.transform.translate(-3, 0, 0, Matrix.LOCAL)
        self.sphereList.append(sphere1)

        sphere2 = Mesh( sphereGeom, lightMaterial )
        sphere2.transform.translate(-1, 0, 0, Matrix.LOCAL)
        self.sphereList.append(sphere2)
        
        sphere3 = Mesh( sphereGeom, rainbowMaterial )
        sphere3.transform.translate(1, 0, 0, Matrix.LOCAL)
        self.sphereList.append(sphere3)

        sphere4 = Mesh( sphereGeom, gridMaterial )
        sphere4.transform.translate(3, 0, 0, Matrix.LOCAL)
        self.sphereList.append(sphere4)

        for sphere in self.sphereList:
            self.scene.add(sphere)
        
    def update(self):
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
                
        for sphere in self.sphereList:
            sphere.transform.rotateY(0.01, Matrix.LOCAL)
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestSurfaceMaterials().run()

