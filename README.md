three.py
========

#### Python 3D library ####

The aim of this project is to create an easy to use 3D library for Python.

This project was inspired by [Three.js](https://threejs.org/), and attempts to follow the effective and reliable class structure from that project whenever possible.

Three.py was originally designed for educational purposes, and rendering efficiency and optimization will occasionally be sacrificed for simplicity and clarity.

To see what the Three.py library is capable of, see the [list of examples](https://github.com/stemkoski/three.py/wiki/Examples) or watch the [sample projects video](https://www.youtube.com/watch?v=vs6LdP6pWKI).

[![Three.py video](https://raw.githubusercontent.com/stemkoski/three.py/master/three.py/docs/youtube-preview.png)](https://www.youtube.com/watch?v=vs6LdP6pWKI)

This project uses the MIT license.

### Usage ###

Three.py uses the Python libraries [pygame](https://www.pygame.org/), [PyOpenGL](http://pyopengl.sourceforge.net/), and [NumPy](http://www.numpy.org/). 

The following code creates a scene, a camera, ambient and directional lights, and adds a light blue cube to the scene. It animates (spins) the cube, and allows the user to move the camera with first-person controls.

```python
from core import *
from cameras import *
from lights import *
from geometry import *
from material import *

class TestCube(Base):
    
    def initialize(self):

        self.setWindowTitle('Cube')
        self.setWindowSize(800,600)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,600)
        self.renderer.setClearColor(0.25,0.25,0.25)
        
        self.scene = Scene()
        
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 7)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        self.scene.add( AmbientLight(strength=0.25) )
        self.scene.add( DirectionalLight(direction=[-1,-1,-1]) )

        self.cube = Mesh( BoxGeometry(), SurfaceLightMaterial(color=[0.5,0.5,1.0]) )
        self.scene.add(self.cube)
        
    def update(self):
        
        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
                
        self.cube.transform.rotateX(0.02, Matrix.LOCAL)
        self.cube.transform.rotateY(0.03, Matrix.LOCAL)
        
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestCube().run()
```
