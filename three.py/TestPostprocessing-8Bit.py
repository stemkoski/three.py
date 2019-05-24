from core import *
from cameras import *
from geometry import *
from material import *
from lights import *

class TestPostprocessing2(Base):
    
    def initialize(self):

        self.setWindowTitle('Pixellation and Reduced Color Palette')
        self.setWindowSize(1024,768)
        
        self.renderer = Renderer()
        self.renderer.setViewportSize(1024,768)
        self.renderer.setClearColor(0.5,0.5,0.5)

        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.setAspectRatio(1024/768)
        self.camera.transform.setPosition(0, 0, 6)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        self.renderTarget = RenderTarget.RenderTarget(1024,768)
        
        crateTexture  = OpenGLUtils.initializeTexture("images/crate.jpg")
        ballTexture  = OpenGLUtils.initializeTexture("images/basketball.png")
        
        self.cube = Mesh( BoxGeometry(), SurfaceLightMaterial(texture=crateTexture) )
        self.cube.transform.translate(1.5, 0, 0, Matrix.LOCAL)        
        self.scene.add(self.cube)
        
        self.sphere = Mesh( SphereGeometry(), SurfaceLightMaterial(texture=ballTexture) )
        self.sphere.transform.translate(-1.5, 0, 0, Matrix.LOCAL)
        self.scene.add(self.sphere)
        

        ambientLight = AmbientLight(color=[0.1,0.1,0.2])
        self.scene.add( ambientLight )
        
        directionalLight = DirectionalLight(color=[1,1,1], position=[4,4,-2], direction=[-1,-1,-1])
        self.scene.add( directionalLight )
        

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
        
        // round x to the nearest 1/denominator
        float roundFrac(float x, float denominator)
        {
            return round(x*denominator) / denominator;
        }

        void main()
        {
            // pixellate original image
            int k = 8;
            vec2 rounded = k * floor(gl_FragCoord.xy / k);
            vec2 UV = rounded / textureSize;
            vec4 color = vec4(0,0,0,0);
	
            for (int x = 0; x < k; x++)
            {
		for (int y = 0; y < k; y++)
		{
		    color += texture(image, UV + vec2(x,y)/textureSize);
		}    
            }
            color /= (k*k);

            // reduce color to a smaller palette
            color.r = roundFrac(color.r, 8);
            color.g = roundFrac(color.g, 8);
            color.b = roundFrac(color.b, 8);
            
            // combine sepia tones with vignette
            gl_FragColor = color;
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
        self.sphere.transform.rotateX(0.005, Matrix.LOCAL)
        self.sphere.transform.rotateY(0.008, Matrix.LOCAL)
        
        # first, render scene into target (texture)
        self.renderer.render(self.scene, self.camera, self.renderTarget)
        # second, render post-processed scene to window.
        # (note: camera irrelevant since projection/view matrices are not used in shader.)
        self.renderer.render(self.postScene, self.camera)

                    
# instantiate and run the program
TestPostprocessing2().run()

