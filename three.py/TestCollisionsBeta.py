from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *
from components import *
from lights import *
from physics import *
import random
#NOTE: this test was for internal testing, for a more detailed explanation of what is going on
#look at TestCollisionDetection
class TestCollisionsBeta(Base):
    
    def initialize(self):

        self.setWindowTitle('Test')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)

        
        self.scene = Scene()

        light = PointLight(position = [0,20,0])
        self.scene.add(light)

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 6)
        self.camera.transform.lookAt(0, 0, 0)
        self.camera.transform.setPosition(0,1,5)
        self.cameraControls = FirstPersonController(self.input, self.camera)
        
        geometry = SphereGeometry()
        geometry2 = SphereGeometry(radius=5)
        material = SurfaceLightMaterial()
        self.Mesh1 = ComponentMesh(geometry,material)
        sphere = Sphere(radius=1,center=self.Mesh1.transform.getPosition())
        self.Mesh1.addComponent("Sphere",sphere)
        self.Mesh2 = ComponentMesh(geometry,material)
        self.Mesh2.transform.setPosition(-3,0.5,0.5)
        sphere = Sphere(radius=1,center=self.Mesh2.transform.getPosition())
        self.Mesh2.addComponent("Sphere",sphere)
        self.scene.add(self.Mesh1)
        self.scene.add(self.Mesh2)

        #create a plane, not attached to any object/mesh, just floating in space
        self.plane = Plane(normal = (-1,0,0), offset = 3)

       

        
        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)
        self.time = 0
        
    def update(self):

        self.cameraControls.update()
        self.Mesh2.transform.translate(1/60.0,0,0)
        self.Mesh2.componentDict["Sphere"].setPosition(self.Mesh2.transform.getPosition())
        if self.Mesh1.overlaps(self.Mesh2):
            #print('wow')
            self.Mesh1.preventOverlap(self.Mesh2)

        if(self.Mesh2.componentDict["Sphere"].intersectsPlane(self.plane)):
            print('overlapping')

        
        

        

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
        if self.input.isMousePressed():
            #launch the mesh
            self.Mesh2.transform.setPosition(-3,0.5,1)
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestCollisionsBeta().run()

