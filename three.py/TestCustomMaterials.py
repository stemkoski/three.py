from math import sin, cos

from core import *
from cameras import *
from mathutils import *
from geometry import *
from material import *
from helpers import *

class TestCustomMaterials(Base):
    
    def initialize(self):

        self.setWindowTitle('Custom Materials')
        self.setWindowSize(800,800)
        
        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)

        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 3, 7)
        self.camera.transform.lookAt( 0, 0, 0 )

        # initialize shaders
        vsCode = """
        attribute vec3 vertexPosition;
        attribute vec2 vertexUV;

        varying vec3 position;

        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;      
        
        void main()
        {
            position = vec3( modelMatrix * vec4(vertexPosition, 1) );
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
        }
        """

        fsCode = """

        varying vec3 position;
        uniform float width;
        
        // credit to Laur(link: https://www.laurivan.com/rgb-to-hsv-to-rgb-for-shaders/)
        // for the conversion functions
        // functions for conversion from rgb to hsv and back
        vec3 rgb2hsv(vec3 c)
        {
            vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
            vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
            vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
 
            float d = q.x - min(q.w, q.y);
            float e = 1.0e-10;
            return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
        }

        vec3 hsv2rgb(vec3 c)
        {
            vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
            vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
            return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
        }

        void main(){
            float percent = mod(position.x/width,1.0);
            vec3 color = vec3(percent,1.0,1.0);
            //vec3 color = vec3(0.5,1.0,1.0);
            color = hsv2rgb(color);

            gl_FragColor = vec4(color,1.0);
        }
        """

        # setup the uniforms
        uniforms = [["float","width",2.5]]

        # create a cube to show off the custom material
        self.cube = Mesh( BoxGeometry(), Material(vsCode,fsCode,uniforms) )
        self.scene.add(self.cube)

        self.time = 0

        self.translationFunction = lambda t: [sin(t*2),sin(t),0]
        
        
    def update(self):
    
        self.time += 1/60

        position = self.translationFunction(self.time)
        self.cube.transform.setPosition(position[0], position[1], position[2], Matrix.GLOBAL)
        self.cube.transform.rotateX(0.02,Matrix.LOCAL)
        self.cube.transform.rotateY(0.02,Matrix.LOCAL)
        
        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestCustomMaterials().run()

