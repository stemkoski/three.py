from core import *
from material import *

class PointBasicMaterial(Material):

    def __init__(self, color=[1,1,1], alpha=1, texture=None, size=1, 
        usePerspective=True, useVertexColors=False, alphaTest=0.75):
        
        # vertex shader code
        vsCode = """
        in vec3 vertexPosition;
        
        in vec3 vertexColor;
        out vec3 vColor; 
        
        // adjust projected size of sprites
        uniform bool usePerspective;
        uniform float size;
        
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        
        void main()
        {
            vColor = vertexColor;
            vec4 eyePosition = viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
            
            if ( usePerspective )
                gl_PointSize = 500 * size / length(eyePosition);
            else
                gl_PointSize = size;
                
            gl_Position = projectionMatrix * eyePosition;
        }
        """

        # fragment shader code
        fsCode = """
        uniform vec3 color;
        uniform float alpha;

        uniform bool useVertexColors;
        in vec3 vColor;
        
        uniform bool useTexture;
        uniform sampler2D image;
        uniform float alphaTest;
        void main()
        {                
            vec4 baseColor = vec4(color, alpha);
            
            if ( useVertexColors )
                baseColor *= vec4(vColor, 1.0);
            
            if ( useTexture )
                baseColor *= texture(image, gl_PointCoord);
                
            gl_FragColor = baseColor;
            
            if (gl_FragColor.a < alphaTest)
                discard;
        }
        """

        # initialize shaders
        super().__init__(vsCode, fsCode)
        
        # set render values
        self.drawStyle = GL_POINTS

        # set default uniform values
        self.setUniform( "vec3", "color", color )
        self.setUniform( "float", "alpha", alpha )
        self.setUniform( "float", "size", size )
        self.setUniform( "float", "alphaTest", alphaTest )
        
        if useVertexColors:
            self.setUniform( "bool", "useVertexColors", 1 )
        else:
            self.setUniform( "bool", "useVertexColors", 0 )
            
        if usePerspective:
            self.setUniform( "bool", "usePerspective", 1 )
        else:
            self.setUniform( "bool", "usePerspective", 0 )
        
        if texture is None:
            self.setUniform( "bool", "useTexture", 0 )
            self.setUniform( "sampler2D", "image", -1 )
        else:
            self.setUniform( "bool", "useTexture", 1 )
            self.setUniform( "sampler2D", "image", texture )
        