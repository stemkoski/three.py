from core import *
from cameras import *
from geometry import *
from material import *

"""
Credit to Gregg Tavares:
https://greggman.com/downloads/examples/three.js/examples/webgl_shader_earth.html
"""

class TestAnimatedDayNight(Base):
    
    def initialize(self):

        self.setWindowTitle('Day and Night Shaders')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0, 4)
        self.cameraControls = FirstPersonController(self.input, self.camera)
        
        starTexture  = OpenGLUtils.initializeTexture("images/stars.jpg")      
        stars = Mesh( SphereGeometry(200, 64,64), SurfaceBasicMaterial(texture=starTexture) )
        self.scene.add(stars)

        sunTexture   = OpenGLUtils.initializeTexture("images/sun.jpg")
        self.sun = Mesh( SphereGeometry(radius=0.25), SurfaceBasicMaterial(texture=sunTexture) )
        self.sun.transform.setPosition(2, 1.5, 0)
        self.scene.add(self.sun)
        
        vsCode = """
        in vec3 vertexPosition;
        in vec2 vertexUV;
        in vec3 vertexNormal;
        out vec2 UV;
        out vec3 normal;
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;              
        void main()
        {
            UV = vertexUV;
            normal = normalize(mat3(modelMatrix) * vertexNormal);
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
        }
        """
        
        fsCode = """
        in vec2 UV;
        in vec3 normal;
        uniform sampler2D imageDay;
        uniform sampler2D imageNight;
        uniform vec3 lightDirection;
        void main()
        {     
            vec3 dayColor = texture2D( imageDay, UV ).rgb;
            vec3 nightColor = texture2D( imageNight, UV ).rgb;

            // compute cosine light to normal so -1 is away from sun and +1 is toward sun.
            float cosAngleLightToNormal = dot(normalize(normal), normalize(-lightDirection));

            // sharpen the edge beween the transition
            cosAngleLightToNormal = clamp( cosAngleLightToNormal * 10.0, -1.0, 1.0);

            // convert to 0 to 1 for mixing
            float mixAmount = cosAngleLightToNormal * 0.5 + 0.5;

            // Select day or night texture based on mix
            vec3 color = mix( nightColor, dayColor, mixAmount );

            gl_FragColor = vec4( color, 1.0 );
        }
        """

        dayTexture = OpenGLUtils.initializeTexture("images/earth-day.jpg")
        nightTexture = OpenGLUtils.initializeTexture("images/earth-night.jpg")
        uniforms = [
            [ "sampler2D", "imageDay", dayTexture ],
            [ "sampler2D", "imageNight", nightTexture ],
            [ "vec3", "lightDirection", [-4, -1, 0] ] ]

        dayNightMaterial = Material(vsCode, fsCode, uniforms)
        
        self.sphere = Mesh( SphereGeometry(), dayNightMaterial )
        self.scene.add(self.sphere)
        
        self.time = 1.0
        
    def update(self):
        
        self.time += self.deltaTime
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
                
        self.sphere.transform.rotateY(0.01, Matrix.LOCAL)
        self.sun.transform.rotateY(0.002, Matrix.LOCAL)
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestAnimatedDayNight().run()

