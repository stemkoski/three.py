from core import *
from cameras import *
from geometry import *
from material import *
from lights import *

class TestPostprocessing1(Base):
    
    def initialize(self):

        self.setWindowTitle('Postprocessing - Sepia and Vignette')
        self.setWindowSize(1024,768)
        
        self.renderer = Renderer()
        self.renderer.setViewportSize(1024,768)
        self.renderer.setClearColor(0.25,0.25,0.25)

        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.setAspectRatio(1024/768)
        self.camera.transform.setPosition(0, 0, 6) 
        self.cameraControls = FirstPersonController(self.input, self.camera)

        self.scene.add( AmbientLight(strength=0.25) )
        self.scene.add( DirectionalLight(direction=[-1,-1,-1]) )

        self.renderTarget = RenderTarget.RenderTarget(1024,768)
        
        crateTexture  = OpenGLUtils.initializeTexture("images/crate.jpg")
        ballTexture  = OpenGLUtils.initializeTexture("images/basketball.png")
        
        self.cube = Mesh( BoxGeometry(), SurfaceLightMaterial(texture=crateTexture) )
        self.cube.transform.translate(1.5, 0, 0, Matrix.LOCAL)        
        self.scene.add(self.cube)
        
        self.sphere = Mesh( SphereGeometry(), SurfaceLightMaterial(texture=ballTexture) )
        self.sphere.transform.translate(-1.5, 0, 0, Matrix.LOCAL)
        self.scene.add(self.sphere)

        # add postprocessing content
        self.postScene = Scene()
        postGeo = Geometry()
        vertexPositionData = [[-1,-1],[1,-1],[1,1], [-1,-1],[1,1],[-1,1]]
        postGeo.setAttribute("vec2", "vertexPosition", vertexPositionData)
        postGeo.vertexCount = 6
        
        vsCode = """
        in vec2 vertexPosition;
        void main()
        {
            gl_Position = vec4(vertexPosition, 0, 1);
        }
        """

        fsCode = """
        uniform sampler2D image;
        uniform vec2 textureSize;
        void main()
        {
            //  gl_FragCoord contains the coordinates of the fragment=pixel being rendered;
            //  divide by window dimensions to get UV coordinates in range [0, 1].
            vec2 UV = gl_FragCoord.xy / textureSize;
            vec4 color = texture(image, UV);

            // convert color to sepia tones
            vec3 sepia = vec3(0,0,0);
            sepia.r = dot(color.rgb, vec3(0.393, 0.769, 0.189));
            sepia.g = dot(color.rgb, vec3(0.349, 0.686, 0.168));   
            sepia.b = dot(color.rgb, vec3(0.272, 0.534, 0.131));
            
            // apply a vignette effect
            // calculate coordinates, assuming (0,0) center, -1<x<1, -1<y<1
            vec2 position = 2 * UV - vec2(1.0, 1.0);
	
            // calculate distance from center, which affects brightness
            float distance = length(position);
    
            float brightness = 1.4 - distance;
            brightness = clamp(brightness, 0.0, 1.0);
            
            // combine sepia tones with vignette
            gl_FragColor = vec4(sepia * brightness, 1.0);
        }
        """

        uniforms = [
            ["vec2", "textureSize", [1024,768]],
            ["sampler2D", "image", self.renderTarget.textureID] ]
        
        postMat = Material(vsCode, fsCode, uniforms)
        
        postMesh = Mesh(postGeo, postMat)
        self.postScene.add(postMesh)

            
    def update(self):
        
        self.cameraControls.update()

        # rotate main scene objects
        self.cube.transform.rotateX(0.005, Matrix.LOCAL)
        self.cube.transform.rotateY(0.008, Matrix.LOCAL)
        self.sphere.transform.rotateY(0.006, Matrix.LOCAL)
        
        # first, render scene into target (texture)
        self.renderer.render(self.scene, self.camera, self.renderTarget)
        # second, render post-processed scene to window.
        # (note: camera irrelevant since projection/view matrices are not used in shader.)
        self.renderer.render(self.postScene, self.camera)

                    
# instantiate and run the program
TestPostprocessing1().run()

