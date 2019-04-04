from core import *
from cameras import *
from geometry import *
from material import *
from mathutils import *

import colorsys

class TestLineCurveGeometry(Base):
    
    def initialize(self):

        self.setWindowTitle('Line and Curve Geometry')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 5, 10)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraController = FirstPersonController(self.input, self.camera)

        rainbowMat = LineBasicMaterial(useVertexColors=True)
        rainbowMat.setUniform("bool", "useVertexColors", 1)

        # vertex colors for most geometries
        rainbowColors = []
        for i in range(256):
            rainbowColors.append( colorsys.hsv_to_rgb(i/256,1,1) )        

        # line-based geometry
        linePoints = [[-6,0,-4],[6,0,-4],[6,0,4],[-6,0,4],[-6,0,-4]]
        lineGeo = LineGeometry(linePoints)
        lineMesh = Mesh(lineGeo, LineBasicMaterial())
        self.scene.add(lineMesh)

        self.meshList = []
        
        # curve-based geometries
        tk2Geo = CurveGeometry( CurveFactory.makeTorusKnot(5,7, 256) )
        tk2Geo.setAttribute("vec3", "vertexColor", rainbowColors)
        tk2 = Mesh(tk2Geo, rainbowMat)
        tk2.transform.translate(4,0,-2)
        self.meshList.append(tk2)

        helixGeo = CurveGeometry( CurveFactory.makeHelix(divisions=256) )
        helixGeo.setAttribute("vec3", "vertexColor", rainbowColors)
        helix = Mesh(helixGeo, rainbowMat)
        helix.transform.translate(0,0,-2)
        self.meshList.append(helix)
        
        tk1Geo = CurveGeometry( CurveFactory.makeTorusKnot(2,3, 256) )
        tk1Geo.setAttribute("vec3", "vertexColor", rainbowColors)
        tk1 = Mesh(tk1Geo, rainbowMat)
        tk1.transform.translate(-4,0,-2)
        self.meshList.append(tk1)

        trefGeo = CurveGeometry( CurveFactory.makeTrefoilKnot(divisions=256) )
        trefGeo.setAttribute("vec3", "vertexColor", rainbowColors)
        trefoil = Mesh(trefGeo, rainbowMat)
        trefoil.transform.translate(-4,0,2)
        self.meshList.append(trefoil)

        fig8Geo = CurveGeometry( CurveFactory.makeFigureEightKnot(divisions=256) )
        fig8Geo.setAttribute("vec3", "vertexColor", rainbowColors)
        figure8 = Mesh(fig8Geo, rainbowMat)
        figure8.transform.translate(4,0,2)
        self.meshList.append(figure8)

        hilbertPoints = Hilbert3D(size=1, iterations=1)
        hilbertGeo = LineGeometry(hilbertPoints)
        n = hilbertGeo.vertexCount
        vertexColorData = []
        for i in range(n):
            vertexColorData.append( colorsys.hsv_to_rgb(i/n, 1, 1) )        
        hilbertGeo.setAttribute("vec3", "vertexColor", vertexColorData)
        hilbertMesh = Mesh(hilbertGeo,rainbowMat)
        hilbertMesh.transform.translate(0,0,2)
        self.meshList.append(hilbertMesh)

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
TestLineCurveGeometry().run()

