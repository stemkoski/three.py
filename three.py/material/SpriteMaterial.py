from OpenGL.GL import *
from core import OpenGLUtils
from material import Material

class SpriteMaterial(Material):
        
    def __init__(self, size=[1,1], anchor=[0.5,0.5], texture=None, color=[1,1,1], alpha=1, alphaTest=0):

        # vertex shader code
        vsCode = """
        in vec2 vertexData;        
        out vec2 UV;
        
        uniform vec2 anchor;
        uniform vec2 size;
        
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;      
        
        void main()
        {
            UV = vertexData;
            vec3 position = vec3( (vertexData.x - anchor.x) * size.x, (vertexData.y - anchor.y) * size.y, 0 );
            mat4 billboardMatrix = viewMatrix * modelMatrix;
            billboardMatrix[0][0] = 1;
            billboardMatrix[0][1] = 0;
            billboardMatrix[0][2] = 0;
            billboardMatrix[1][0] = 0;
            billboardMatrix[1][1] = 1;
            billboardMatrix[1][2] = 0;
            billboardMatrix[2][0] = 0;
            billboardMatrix[2][1] = 0;
            billboardMatrix[2][2] = 1;
            gl_Position = projectionMatrix * billboardMatrix * vec4( position, 1 );
        }
        """

        # fragment shader code
        fsCode = """
        uniform vec3 color;
        uniform float alpha;
        
        in vec2 UV;
        uniform sampler2D image;
        
        uniform float alphaTest;

        void main()
        {
            gl_FragColor = vec4(color, alpha) * texture2D(image, UV);
            
            if (gl_FragColor.a < alphaTest)
                discard;
        }
        """
        
        # initialize shaders
        super().__init__(vsCode, fsCode)
                
        # set default render values
        self.drawStyle = GL_TRIANGLES

        # set default uniform values
        self.setUniform( "vec2", "size", size )
        self.setUniform( "vec2", "anchor", anchor )
        self.setUniform( "sampler2D", "image", texture )
        self.setUniform( "vec3", "color", color )
        self.setUniform( "float", "alpha", alpha )
        self.setUniform( "float", "alphaTest", alphaTest )
        
        

        