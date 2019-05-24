from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

class TestTemplate(Base):
    
    def initialize(self):

        self.setWindowTitle('Fisheye Demo')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0, 3)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        
        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)

        vsCode = """
        attribute vec3 vertexPosition;
        attribute vec2 vertexUV;

        out vec2 UV;

        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;      
        
        void main()
        {
            UV = vertexUV;
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
        }
        """

        fsCode = """

        in vec2 UV;
        uniform sampler2D image;

        vec2 circle_to_square(vec2 v)
        {
            float x = 0.5 * sqrt(2 + v.x*v.x - v.y*v.y + 2*v.x*sqrt(2)) - 0.5 * sqrt(2 + v.x*v.x - v.y*v.y - 2*v.x*sqrt(2));
            float y = 0.5 * sqrt(2 - v.x*v.x + v.y*v.y + 2*v.y*sqrt(2)) - 0.5 * sqrt(2 - v.x*v.x + v.y*v.y - 2*v.y*sqrt(2));
            return vec2(x,y);
        }

        vec2 f(vec2 v)
        {
            return vec2( v.x * sqrt(1.0 - 0.5*v.y*v.y) , v.y * sqrt(1.0 - 0.5*v.x*v.x) );
        }

        float line(float x1, float y1, float x2, float y2, float x)
        {
            return (y2 - y1)/(x2 - x1) * (x - x1) + y1;
        }
        
        void main()
        {
            vec2 v;
            if (UV.x < 0.5)
            {
                v = ( f(UV * vec2(4.0,2.0) - vec2(1.0,1.0)) + vec2(1.0,1.0) ) * vec2(0.25,0.5);
            }
            else
            {
                v = ( f(UV * vec2(4.0,2.0) - vec2(3.0,1.0)) + vec2(3.0,1.0) ) * vec2(0.25,0.5);
            }

            float e = 0.05;

            vec4 baseColor;
            if (UV.x <= 0.5 - e)
            {
                v = ( f(UV * vec2(4.0,2.0) - vec2(1.0,1.0)) + vec2(1,1) ) * vec2(0.25,0.5);
                baseColor = texture(image, v);
            }
            if (0.5 - e <= UV.x && UV.x <= 0.5)
            {
                v = ( f(UV * vec2(4,2) - vec2(1,1)) + vec2(1,1) ) * vec2(0.25,0.5);
                baseColor = texture(image, v);
                // baseColor = vec4(1,0,0,1);
            }
            if (0.5 <= UV.x && UV.x <= 0.5 + e)
            {
                float t = line(0.45,0.45,0.50,0.55, UV.x);
                v = ( f(vec2(t,UV.y) * vec2(4,2) - vec2(1,1)) + vec2(1,1) ) * vec2(0.25,0.5);
                baseColor = texture(image, v);
                // baseColor = vec4(0,1,0,1);
            }
            if ( UV.x > 0.5 + e )
            {
                v = ( f(UV * vec2(4.0,2.0) - vec2(3.0,1.0)) + vec2(3,1) ) * vec2(0.25,0.5);
                baseColor = texture(image, v);
                baseColor = vec4(0,0,1,1);
            }
                          
            gl_FragColor = baseColor;
            
        }
        """

        material = Material(vsCode, fsCode)

        # texture = OpenGLUtils.initializeTexture("images/color-grid.png")
        texture = OpenGLUtils.initializeTexture("images/frame.jpg")
        material.setUniform("sampler2D", "image", texture)
        
        sphere = Mesh( SphereGeometry(radius=100), material )
        # self.scene.add(sphere)
        quad = Mesh( QuadGeometry(), material )
        self.scene.add(quad)

        # self.scene.add(AxesHelper(axisLength=3))        
        
    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestTemplate().run()

