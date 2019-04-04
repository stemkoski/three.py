from OpenGL.GL import *
from core import OpenGLUtils
from material import Material

class SurfaceBasicMaterial(Material):
        
    def __init__(self, color=[1,1,1], alpha=1, texture=None, wireframe=False, lineWidth=1, useVertexColors=False, alphaTest=0):

        # vertex shader code
        vsCode = """
        in vec3 vertexPosition;
        in vec2 vertexUV;
        in vec3 vertexNormal;
        in vec3 vertexColor;
        
        out vec3 position;
        out vec2 UV;
        out vec3 normal;
        out vec3 vColor;
        
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;      
        
        void main()
        {
            position = vec3( modelMatrix * vec4(vertexPosition, 1) );
            UV = vertexUV;
            normal = normalize(mat3(modelMatrix) * vertexNormal); // normalize in case of model scaling
            vColor = vertexColor;
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
        }
        """

        # fragment shader code
        fsCode = """
        uniform vec3 color;
        uniform float alpha;
        
        in vec3 position;
        in vec2 UV;
        in vec3 normal;
        
        uniform bool useVertexColors;
        in vec3 vColor;
        
        uniform bool useTexture;
        uniform sampler2D image;
        
        uniform float alphaTest;
        
        uniform bool useLight;
        
        struct Light
        {
            bool isAmbient;
            bool isDirectional;
            bool isPoint;
            
            // used by all lights
            float strength;
            vec3 color;
            
            // used by directional light
            vec3 direction;
            
            // used by point light
            vec3 position;
            
        };

        uniform Light light0;
        uniform Light light1;
        uniform Light light2;
        uniform Light light3;
        
        uniform int lightCount;
        
        vec3 lightCalculation(Light light, vec3 fragPosition, vec3 fragNormal)
        {
            if ( light.isAmbient )
            {
                return light.color * light.strength;
            }
            else if ( light.isDirectional )
            {
                vec3 unitNormal = normalize(fragNormal);
                float cosAngle = max( dot(unitNormal, -light.direction), 0.0 );
                return light.color * light.strength * cosAngle;
            }
            else if ( light.isPoint )
            {
                vec3 lightDirection = normalize(light.position - fragPosition);
                float lightDistance = length(light.position - fragPosition);
                vec3 unitNormal = normalize(fragNormal);
                float cosAngle = max( dot(unitNormal, lightDirection), 0.0 );
                float attenuation = 1.0;
                return light.color * light.strength * cosAngle * attenuation;
            }
            else
            {
                return vec3(0,0,0);
            }
            
        }
        
        void main()
        {
            vec4 baseColor = vec4(color, alpha);
            
            if ( useVertexColors )
                baseColor *= vec4(vColor, 1);
                
            if ( useTexture )
                baseColor *= texture2D(image, UV);

            if ( useLight )
            {
                Light lightArray[4] = {light0, light1, light2, light3};
                vec3 totalLight = vec3(0,0,0);
                for (int n = 0; n < lightCount; n++)
                    totalLight += lightCalculation( lightArray[n], position, normal );
                totalLight = min( totalLight, vec3(1,1,1) );
                baseColor *= vec4( totalLight, 1 );
            }

            gl_FragColor = baseColor;
            
            if (gl_FragColor.a < alphaTest)
                discard;
        }
        """
        
        # initialize shaders
        super().__init__(vsCode, fsCode)
                
        # set default uniform values
        self.setUniform( "vec3", "color", color )
        self.setUniform( "float", "alpha", alpha )
        
        if useVertexColors:
            self.setUniform( "bool", "useVertexColors", 1 )
        else:
            self.setUniform( "bool", "useVertexColors", 0 )
            
        if texture is None:
            self.setUniform( "bool", "useTexture", 0 )
            self.setUniform( "sampler2D", "image", -1 )
        else:
            self.setUniform( "bool", "useTexture", 1 )
            self.setUniform( "sampler2D", "image", texture )
            
        self.setUniform( "bool", "useLight", 0 )
        
        # set default render values
        self.drawStyle = GL_TRIANGLES
        
        # used for wireframe rendering
        self.lineWidth = lineWidth
        
        # customize draw style GL_TRIANGLES
        if wireframe:
            self.fillStyle  = GL_LINE
        else:
            self.fillStyle  = GL_FILL

        