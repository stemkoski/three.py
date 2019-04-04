from core import *
from cameras import *
from geometry import *
from material import *

class TestAnimatedVertices(Base):
    
    def initialize(self):

        self.setWindowTitle('Animated Vertices')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0, 4)
        self.cameraControls = FirstPersonController(self.input, self.camera)
        
        # this shader should only be applied to two geometries
        #   derived from the SurfaceGeometry class with the same resolution
        
        morphVS = """
        in vec3 vertexPositionA;
        in vec3 vertexPositionB;
        uniform float percent;
        in vec2 vertexUV;
        out vec2 UV;
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        void main()
        {
            UV = vertexUV;
            vec3 position = mix(vertexPositionA, vertexPositionB, percent);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
        }
        """

        morphFS = """
        in vec2 UV;
        uniform sampler2D imageA;
        uniform sampler2D imageB;
        uniform float percent;
        void main()
        {    
            vec4 baseColorA = texture2D(imageA, UV);
            vec4 baseColorB = texture2D(imageB, UV);
            gl_FragColor = mix(baseColorA, baseColorB, percent);
        }
        """

        textureA = OpenGLUtils.initializeTexture("images/color-grid.png")
        textureB = OpenGLUtils.initializeTexture("images/grid.jpg")
        
        morphUniforms = [
            [ "sampler2D", "imageA", textureA ],
            [ "sampler2D", "imageB", textureB ],
            [ "float", "percent", 1.0 ] ]

        morphMaterial = Material(morphVS, morphFS, morphUniforms)

        morphGeometry = Geometry()
        
        sphere = SphereGeometry(xResolution=16, yResolution=16)
        cone = ConeGeometry(radialSegments=16, heightSegments=16)
        
        morphGeometry.setAttribute("vec3", "vertexPositionA", sphere.attributeData["vertexPosition"]["value"])
        morphGeometry.setAttribute("vec3", "vertexPositionB", cone.attributeData["vertexPosition"]["value"])
        morphGeometry.setAttribute("vec2", "vertexUV", sphere.attributeData["vertexUV"]["value"])
        morphGeometry.vertexCount = sphere.vertexCount
        
        self.shape = Mesh( morphGeometry, morphMaterial )
        self.shape.transform.translate(0, 0, 0, Matrix.LOCAL)        
        self.scene.add(self.shape)
               
        self.time = 1.0
        
    def update(self):
        
        self.time += self.deltaTime
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
                
        percent = sin( 2 * self.time ) * 0.5 + 0.5
        self.shape.material.setUniform("float", "percent", percent)
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestAnimatedVertices().run()

