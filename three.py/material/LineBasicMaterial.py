from core import *
from material import *

class LineBasicMaterial(Material):
        
    def __init__(self, color=[0,0,0], alpha=1, lineWidth=4, useVertexColors=False):

        # vertex shader code
        vsCode = """
        in vec3 vertexPosition;

        in vec3 vertexColor;
        out vec3 vColor; 
        
        in float vertexArcLength;
        out float arcLength;

        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;        
        void main()
        {
            arcLength = vertexArcLength;
            vColor = vertexColor;
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
        }
        """

        # fragment shader code
        fsCode = """
        
        uniform vec3 color;
        uniform float alpha;

        uniform bool useVertexColors;
        in vec3 vColor;
        
        uniform bool useDashes;
        uniform float dashLength;
        uniform float gapLength;
        in float arcLength;
        
        void main()
        {                
            if ( useDashes )
            {
                float modLength = mod(arcLength, dashLength + gapLength);
                if ( modLength > dashLength )
                    discard;
            }

            if ( useVertexColors )
                gl_FragColor = vec4(vColor, alpha);
            else
                gl_FragColor = vec4(color, alpha);
            
        }
        """

        # initialize shaders
        super().__init__(vsCode, fsCode)
        
        # set render values
        self.drawStyle = GL_LINE_STRIP
        self.lineWidth = lineWidth
        
        # set default uniform values
        self.setUniform( "vec3", "color", color )
        self.setUniform( "float", "alpha", alpha )
        
        if useVertexColors:
            self.setUniform( "bool", "useVertexColors", 1 )
        else:
            self.setUniform( "bool", "useVertexColors", 0 )
        
        self.setUniform( "bool", "useDashes", 0 )
        self.setUniform( "float", "dashLength", 0 )
        self.setUniform( "float", "gapLength", 0 )
        