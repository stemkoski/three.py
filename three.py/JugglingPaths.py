from core import *
from cameras import *
from lights import AmbientLight, DirectionalLight
from geometry import *
from material import *
from mathutils import *
from helpers import *

class JugglingPaths(Base):
    
    def initialize(self):

        self.setWindowTitle('Juggling Paths')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 5)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        self.scene.add( AmbientLight(strength=0.25) )
        self.scene.add( DirectionalLight(direction=[-1,-1,-2]) )

        starTexture  = OpenGLUtils.initializeTexture("images/stars.jpg")
        stars = Mesh( SphereGeometry(200, 64,64), SurfaceBasicMaterial(texture=starTexture) )
        self.scene.add(stars)
        
        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0.5,0.5,0.5], centerColor=[1,1,1])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)

        ballGeometry = SphereGeometry(radius=0.1)
        self.ball1 = Mesh( ballGeometry, SurfaceLightMaterial(color=[1,0.2,0.2]) )
        self.ball3 = Mesh( ballGeometry, SurfaceLightMaterial(color=[0.2,1,0.2]) )
        self.ball2 = Mesh( ballGeometry, SurfaceLightMaterial(color=[0.2,0.2,1]) )
        self.scene.add(self.ball1)
        self.scene.add(self.ball2)
        self.scene.add(self.ball3)

        handGeometry = BoxGeometry(width=0.4, height=0.1, depth=0.4)
        self.handL = Mesh( handGeometry, SurfaceLightMaterial(color=[0.9,0.9,0.9]) )
        self.handR = Mesh( handGeometry, SurfaceLightMaterial(color=[0.9,0.9,0.9]) )
        self.scene.add(self.handL)
        self.scene.add(self.handR)
        
        ballHeight = 3
        carryDepth = 0.5
        # all throw/catch occurs at y=0
        throwPosition = 2
        catchPosition = 3
        midPosition = (throwPosition + catchPosition)/2
        
        A = [ throwPosition,           0, 0]
        B = [  -midPosition,  ballHeight, 0]
        C = [-catchPosition,  ballHeight, 0]
        D = [-catchPosition,           0, 0]
        E = [-catchPosition, -carryDepth, 0]
        F = [  -midPosition, -carryDepth, 0]
        G = [-throwPosition,           0, 0]
        H = [   midPosition,  ballHeight, 0]
        I = [ catchPosition,  ballHeight, 0]
        J = [ catchPosition,           0, 0]
        K = [ catchPosition, -carryDepth, 0]
        L = [   midPosition, -carryDepth, 0]
        
        curve1 = CurveFactory.makeCubicBezier(A, B, C, D)
        curve2 = CurveFactory.makeCubicBezier(D, E, F, G)
        curve3 = CurveFactory.makeCubicBezier(G, H, I, J)
        curve4 = CurveFactory.makeCubicBezier(J, K, L, A)
        
        self.ballCurve = Multicurve( [curve1, curve2, curve3, curve4] )
        self.handCurveL = Multicurve( [CurveFactory.makeLineSegment(G,D), curve2] )
        self.handCurveR = Multicurve( [CurveFactory.makeLineSegment(A,J), curve4] )

        # draw ball curve path for illustration
        path = Mesh(CurveGeometry(self.ballCurve), LineDashedMaterial(color=[1,1,0.5], dashLength=0.05, gapLength=0.05, lineWidth=1))
        self.scene.add(path)

        scale = 0.8
        airTime = 3 * scale
        holdTime = 1 * scale
        self.orbitTime = 2 * (airTime + holdTime)
        self.ballTimeTween = Tween(
                timeList=[0, airTime, airTime+holdTime, 2*airTime+holdTime, self.orbitTime],
                valueList=[0, 0.25, 0.50, 0.75, 1],
                loop=True)

        self.handTimeTween = Tween(
                timeList=[0, self.orbitTime/3 - holdTime, self.orbitTime/3],
                valueList=[0, 0.5, 1],
                loop=True)

        self.time = 0

        
    def update(self):

        self.time += self.deltaTime
        
        t1 = self.ballTimeTween.evaluate(self.time)
        p1 = self.ballCurve.getPoint(t1)
        self.ball1.transform.setPosition(p1[0], p1[1], p1[2])

        t2 = self.ballTimeTween.evaluate(self.time - 1/3*self.orbitTime)
        p2 = self.ballCurve.getPoint(t2)
        self.ball2.transform.setPosition(p2[0], p2[1], p2[2])

        t3 = self.ballTimeTween.evaluate(self.time - 2/3*self.orbitTime)
        p3 = self.ballCurve.getPoint(t3)
        self.ball3.transform.setPosition(p3[0], p3[1], p3[2])

        t4 = self.handTimeTween.evaluate(self.time)
        p4 = self.handCurveR.getPoint(t4)
        self.handR.transform.setPosition(p4[0], p4[1]-0.12, p4[2])

        t5 = self.handTimeTween.evaluate(self.time - 1/2*self.orbitTime)
        p5 = self.handCurveL.getPoint(t5)
        self.handL.transform.setPosition(p5[0], p5[1]-0.12, p5[2])
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
JugglingPaths().run()

