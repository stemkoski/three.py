from core import *
from cameras import *
from lights import AmbientLight, DirectionalLight
from mathutils import *
from geometry import *
from material import *

class TestSurfaceGeometry(Base):
    
    def initialize(self):

        self.setWindowTitle('Surface Geometry')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 9, 12)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        self.scene.add( AmbientLight(strength=0.25) )
        self.scene.add( DirectionalLight(direction=[-1,-1,-1]) )
        
        gridTexture  = OpenGLUtils.initializeTexture("images/color-grid.png")
        gridMaterial = SurfaceLightMaterial(texture=gridTexture)

        self.meshList = []
        
        # pyramid, cone, cylinder, cylinder
        
        pyramid = Mesh( PyramidGeometry(numberSides=4), gridMaterial )
        pyramid.transform.translate(-4.5, 0, 4.5, Matrix.LOCAL)
        self.meshList.append(pyramid)

        cone = Mesh( ConeGeometry(), gridMaterial )
        cone.transform.translate(-1.5, 0, 4.5, Matrix.LOCAL)
        self.meshList.append(cone)

        cylinder2 = Mesh( CylinderGeometry(radiusTop=0.25, radiusBottom=1), gridMaterial )
        cylinder2.transform.translate(1.5, 0, 4.5, Matrix.LOCAL)
        self.meshList.append(cylinder2)

        cylinder = Mesh( CylinderGeometry(), gridMaterial )
        cylinder.transform.translate(4.5, 0, 4.5, Matrix.LOCAL)
        self.meshList.append(cylinder)
        
        # Octahedron, Icosahedron, Prism, Cube
        
        octa = Mesh( OctahedronGeometry(), gridMaterial )
        octa.transform.translate(-4.5, 0, 1.5, Matrix.LOCAL)
        self.meshList.append(octa)
        
        icosa = Mesh( IcosahedronGeometry(), gridMaterial )
        icosa.transform.translate(-1.5, 0, 1.5, Matrix.LOCAL)
        self.meshList.append(icosa)

        prism = Mesh( PrismGeometry(numberSides=6), gridMaterial )
        prism.transform.translate(1.5, 0, 1.5, Matrix.LOCAL)
        self.meshList.append(prism)

        cube = Mesh( BoxGeometry(), gridMaterial )
        cube.transform.translate(4.5, 0, 1.5, Matrix.LOCAL)
        self.meshList.append(cube)
        
        # Circle, Ring, Hexagon, Quad
        
        circle = Mesh( CircleGeometry(), gridMaterial )
        circle.transform.translate(-4.5, 0, -1.5, Matrix.LOCAL)
        self.meshList.append(circle)

        ring = Mesh( RingGeometry(), gridMaterial )
        ring.transform.translate(-1.5, 0, -1.5, Matrix.LOCAL)
        self.meshList.append(ring)

        polygon = Mesh( PolygonGeometry(numberSides=6), gridMaterial )
        polygon.transform.translate(1.5, 0, -1.5, Matrix.LOCAL)
        self.meshList.append(polygon)

        quad = Mesh( QuadGeometry(), gridMaterial )
        quad.transform.translate(4.5, 0, -1.5, Matrix.LOCAL)
        self.meshList.append(quad)

        # Sphere, Torus, Tube(Helix), Tube(Knot)
        
        sphere = Mesh( SphereGeometry(), gridMaterial )
        sphere.transform.translate(-4.5, 0, -4.5, Matrix.LOCAL)
        self.meshList.append(sphere)

        torus = Mesh( TorusGeometry(), gridMaterial )
        torus.transform.translate(-1.5, 0, -4.5, Matrix.LOCAL)
        self.meshList.append(torus)

        curve1 = CurveFactory.makeHelix(radius=0.75)
        helix = Mesh( TubeGeometry(curve1, 0.1, 6), gridMaterial )
        helix.transform.translate(1.5, 0, -4.5, Matrix.GLOBAL)
        self.meshList.append(helix)

        curve2 = CurveFactory.makeTorusKnot(3,5)
        knot = Mesh( TubeGeometry(curve2, 0.1, 6), gridMaterial )
        knot.transform.translate(4.5, 0, -4.5, Matrix.GLOBAL)
        self.meshList.append(knot)

        for mesh in self.meshList:
            self.scene.add(mesh)
        
        
    def update(self):

        # update camera via keyboard
        # self.cameraControls.update()
        # -or-
        # automatically update camera - orbit around scene
        self.camera.transform.rotateY(0.004, Matrix.GLOBAL)
        
        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        for mesh in self.meshList:
            mesh.transform.rotateX(0.030, Matrix.LOCAL)
            mesh.transform.rotateY(0.015, Matrix.LOCAL)
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestSurfaceGeometry().run()

