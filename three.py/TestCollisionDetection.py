from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *
from components import *
from physics import *
from lights import *
import random

class TestCollisionDetection(Base):
    
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
        self.camera.transform.setPosition(0,9,25)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        #seperate geometries for different sized spheres
        geometry = SphereGeometry()
        geometry2 = SphereGeometry(radius=5)
        material = SurfaceLightMaterial()

        #Bigger sphere the others will fall onto
        self.Mesh1 = ComponentMesh(geometry2,material)
        #sphere component: can be used for several things, right now only collisions
        sphere = Sphere(radius=5,center=self.Mesh1.transform.getPosition())
        self.Mesh1.addComponent("Sphere",sphere)
        self.scene.add(self.Mesh1)

        #a list of smaller meshes that will fall onto the larger one
        self.meshList = []
        for x in range(25):
            self.meshList.append(ComponentMesh(geometry,material))
            self.meshList[x].transform.setPosition(random.randint(-5,5),20,random.randint(-5,5))
            self.meshList[x].addComponent("Sphere",Sphere(center =
                                                          self.meshList[x].transform.getPosition()))
            #NOTE: when manually updating transform, make sure to also change bounding circle location, or errors can happen
            self.scene.add(self.meshList[x])

        
        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)
        self.time = 0
        
    def update(self):

        self.cameraControls.update()
        self.time+=1/60.0

        #check for collisions with all of the meshes
        for x in range(25):
            mesh = self.meshList[x]
            
            if mesh.overlaps(self.Mesh1):
                self.Mesh1.preventOverlap(mesh)
            for y in range(25):
                if x == y:
                    continue
                if mesh.overlaps(self.meshList[y]):
                    mesh.preventOverlap(self.meshList[y])

            #move mesh downward, or move to top when it gets low enough
            mesh.transform.translate(0,-1/60.0*5,0)
            if mesh.transform.getPosition()[1] < -10:
                mesh.transform.setPosition(random.randint(-5,5),20,random.randint(-5,5))
            

        

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestCollisionDetection().run()

