from core import *
from cameras import *
from geometry import *
from material import *

class TestAnimatedTextures(Base):
    
    def initialize(self):

        self.setWindowTitle('Animated Textures')
        self.setWindowSize(800,800)
        
        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25,0.25,0.25)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 0, 7)
        self.cameraControls = FirstPersonController(self.input, self.camera)
        
        gridTexture  = OpenGLUtils.initializeTexture("images/color-grid.png")
        lightMaterial = SurfaceBasicMaterial( color=[1,1,1], texture=gridTexture );

        distortVS = """
        in vec3 vertexPosition;
        in vec2 vertexUV;
        out vec2 UV;
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        void main()
        {
            UV = vertexUV;
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
        }
        """

        distortFS = """
        in vec2 UV;
        uniform sampler2D image;
        uniform sampler2D noise;
        uniform float baseSpeed;
        uniform float noiseScale;
        uniform float time;
        uniform float alpha;
        void main(){
            
            vec2 uvTimeShift = UV + vec2(-0.7,1.5)*time* baseSpeed;
            vec4 noiseGeneratorTimeShift = texture2D(noise, uvTimeShift);
            vec2 uvNoiseTimeShift = UV + noiseScale * vec2(noiseGeneratorTimeShift.r, noiseGeneratorTimeShift.b);
            vec4 baseColor = texture2D(image,uvNoiseTimeShift);

            baseColor.a = alpha;
            gl_FragColor = baseColor;
        }
        """

        noiseTexture = OpenGLUtils.initializeTexture("images/cloud.png")
        waterTexture = OpenGLUtils.initializeTexture("images/water.jpg")
        waterUniforms = [
            [ "sampler2D", "image", waterTexture ],
            [ "sampler2D", "noise", noiseTexture ],
            [ "float", "baseSpeed",   1.15 ],
            [ "float", "noiseScale",  0.20 ],
            [ "float", "time",  1.0 ],
            [ "float", "alpha", 1.0 ] ]

        waterMaterial = Material(distortVS, distortFS, waterUniforms)
        
        self.cube = Mesh( BoxGeometry(), waterMaterial )
        self.cube.transform.translate(1.5, 0, 0, Matrix.LOCAL)        
        self.scene.add(self.cube)
       
        lavaTexture = OpenGLUtils.initializeTexture('images/lava.jpg')
        lavaUniforms = [
            [ "sampler2D", "image", lavaTexture ],
            [ "sampler2D", "noise", noiseTexture ],
            [ "float", "baseSpeed",   0.05 ],
            [ "float", "noiseScale",  0.5337 ],
            [ "float", "time",  1.0 ],
            [ "float", "alpha", 1.0 ] ]

        lavaMaterial = Material(distortVS, distortFS, lavaUniforms)

        self.sphere = Mesh( SphereGeometry(radius=1.25), lavaMaterial )
        self.sphere.transform.translate(-1.5, 0, 0, Matrix.LOCAL)
        self.scene.add(self.sphere)
        
        self.time = 1.0
        
    def update(self):
        
        self.time += self.deltaTime
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
                
        self.cube.transform.rotateX(0.005, Matrix.LOCAL)
        self.cube.transform.rotateY(0.008, Matrix.LOCAL)

        self.sphere.transform.rotateY(0.006, Matrix.LOCAL)

        self.cube.material.setUniform("float", "time", self.time)
        self.sphere.material.setUniform("float", "time", self.time)
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestAnimatedTextures().run()

