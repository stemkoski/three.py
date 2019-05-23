import pygame

from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *
from mathutils import *

class TestMandlebrot(Base):
    
    def initialize(self):

        self.setWindowTitle('Mandlebrot set')
        self.setWindowSize(640,640)

        self.renderer = Renderer()
        self.renderer.setViewportSize(640,640)
        self.renderer.setClearColor(0.25, 0.25, 0.25)
        
        self.scene = Scene()

        self.camera = OrthographicCamera()
        
        vsCode = """
        in vec3 vertexPosition;
        void main()
        {
            gl_Position = vec4(vertexPosition, 1.0);
        }
        """

        fsCode = """
        vec3 hsv_to_rgb(vec3 c)
        {
            vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
            vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
            return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
        }

        uniform vec2 screenSize;
        uniform vec2 center;
        uniform vec2 viewportSize;
        uniform float time;

        void main()
        {
            
            // convert from pixel coordinates to math coordinates
            vec2 c = (gl_FragCoord.xy / screenSize) * viewportSize + center - viewportSize/2;

            vec2 z = c;	
            
            float power = 0.3;
                
            int i;
            int maxiter = 512;
            for(i=0; i<maxiter; i++) 
            {
                float x = (z.x * z.x - z.y * z.y) + c.x;
                float y = (z.y * z.x + z.x * z.y) + c.y;

                if ((x * x + y * y) > 4.0) break;
                z.x = x;
                z.y = y;
            }

            float amount = i / 128.0;
            
            vec3 color = hsv_to_rgb( vec3(amount + time, 1.0, 1.0) );
            
            if (i < maxiter)
                gl_FragColor = vec4(color, 1); 
            else // does not reach escape value
                gl_FragColor = vec4(0,0,0,1);
        }
        """
        
        geometry = QuadGeometry()

        material = Material(vsCode, fsCode)

        material.setUniform( "vec2", "screenSize", [640, 640] )
        material.setUniform( "vec2", "center", [-0.5, 0] )
        material.setUniform( "vec2", "viewportSize", [4,4] )
        material.setUniform( "float", "time", 0 )
       
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

        self.recenter = False

        print("Controls: ")
        print("W/A/S/D - move")
        print("I/O     - zoom In/Out")
        print("click   - center on mouse cursor")
        print("R       - reset to default size")
        print("C       - cycle colors")
        print("Z       - save screenshot")
        
    def update(self):
        
        if self.input.isKeyDown(pygame.K_ESCAPE):
            self.running = False

        # save screenshot
        if self.input.isKeyDown(pygame.K_z):
            timeString = str( int(1000 * time.time()) )
            fileName = "image-" + timeString + ".png"
            pygame.image.save(self.screen, fileName)
            print("Image saved to: " + fileName)

        uniformData = self.mesh.material.uniformList
        
        # move around
        moveAmountX, moveAmountY = uniformData["viewportSize"].value
        scrollSpeed = 0.005
        moveAmountX *= scrollSpeed
        moveAmountY *= scrollSpeed
        if self.input.isKeyPressed(pygame.K_a):
            uniformData["center"].value[0] -= moveAmountX
        if self.input.isKeyPressed(pygame.K_d):
            uniformData["center"].value[0] += moveAmountX
        if self.input.isKeyPressed(pygame.K_w):
            uniformData["center"].value[1] += moveAmountY
        if self.input.isKeyPressed(pygame.K_s):
            uniformData["center"].value[1] -= moveAmountY

        # zoom in/out
        zoomAmount = 1.01
        if self.input.isKeyPressed(pygame.K_i):
            uniformData["viewportSize"].value[0] /= zoomAmount
            uniformData["viewportSize"].value[1] /= zoomAmount
        if self.input.isKeyPressed(pygame.K_o):
            uniformData["viewportSize"].value[0] *= zoomAmount
            uniformData["viewportSize"].value[1] *= zoomAmount

        # increment time variable (activates color shift)
        if self.input.isKeyPressed(pygame.K_c):
            uniformData["time"].value += 0.001
            
        # reset to default view
        if self.input.isKeyDown(pygame.K_r):
            uniformData["center"].value = [-0.5, 0]
            uniformData["viewportSize"].value = [4,4]
            uniformData["time"].value = 0

        # center on mouse position (press mouse button)
        if self.input.isMouseDown():
            screenSize = uniformData["screenSize"].value
            mouseX, mouseY = self.input.getMousePosition()
            percentX = mouseX / screenSize[0]
            # account for inverted Y-axis
            percentY = (1 - mouseY / screenSize[1])
            center = uniformData["center"].value
            viewportSize = uniformData["viewportSize"].value
            targetX = center[0] + (percentX - 0.5) * viewportSize[0]
            targetY = center[1] + (percentY - 0.5) * viewportSize[1]
            self.recenter = True
            self.moveTimer = 0
            self.moveTween = Tween( timeList=[0,1], valueType="vec2",
                                    valueList=[ center, [targetX, targetY] ] )

        if self.recenter:
            self.moveTimer += self.deltaTime
            uniformData["center"].value = self.moveTween.evaluate(self.moveTimer)
            if self.moveTimer >= 1:
                self.recenter = False
 
        # print window coordinates
        if self.input.isKeyDown(pygame.K_p):
            center = uniformData["center"].value
            viewportSize = uniformData["viewportSize"].value
            xMin = "{:.8f}".format( center[0] - viewportSize[0] )
            xMax = "{:.8f}".format( center[0] + viewportSize[0] )
            yMin = "{:.8f}".format( center[1] - viewportSize[1] )
            yMax = "{:.8f}".format( center[1] + viewportSize[1] )
            print("Current viewport size:")
            print("x-axis: " + xMin + " to " + xMax)
            print("y-axis: " + yMin + " to " + yMax)

        # resize the window
        if self.input.resize():
            newSize = self.input.getWindowSize()
            self.renderer.setViewportSize(newSize["width"], newSize["height"])
            oldSize = uniformData["screenSize"].value
            uniformData["viewportSize"].value[0] *= newSize["width"] / oldSize[0]
            uniformData["viewportSize"].value[1] *= newSize["height"] / oldSize[1]
            uniformData["screenSize"].value = [ newSize["width"], newSize["height"] ]

        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestMandlebrot().run()

