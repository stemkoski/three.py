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
        
        uniform bool useFog;
        out float cameraDistance; 
        
        uniform bool receiveShadow;
        
        // assume that at most one light casts shadows
        //   and its values have been passed in here
        uniform mat4 shadowProjectionMatrix;
        uniform mat4 shadowViewMatrix;
        out vec4 positionFromShadowLight;
        
        void main()
        {
            // out values being sent to fragment shader
            position = vec3( modelMatrix * vec4(vertexPosition, 1) );
            UV = vertexUV;
            normal = normalize(mat3(modelMatrix) * vertexNormal); // normalize in case of model scaling
            vColor = vertexColor;
            
            if (receiveShadow)
            {
                // multiply by modelMatrix works for directly overhead light
                positionFromShadowLight = shadowProjectionMatrix * shadowViewMatrix * modelMatrix * vec4(vertexPosition, 1);
            }
            
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
            
            if (useFog)
            {
                cameraDistance = gl_Position.w;
            }
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
            
            // used by point light
            vec3 position;

            // used by directional light
            vec3 direction;
        };

        uniform Light light0;
        uniform Light light1;
        uniform Light light2;
        uniform Light light3;
        
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
            else // occurs if no data set for this light; bool values default to 0
            {
                return vec3(0,0,0);
            }
        }
        
        // parameters for fog calculations
        uniform bool useFog;
        uniform vec3 fogColor;
        uniform float fogStartDistance;
        uniform float fogEndDistance;
        in float cameraDistance;
        
        // assume that at most one light casts shadows
        //   and its values have been passed in here
        uniform bool receiveShadow;
        in vec4 positionFromShadowLight;
        uniform sampler2D shadowMap;
        uniform float shadowStrength;
        uniform float shadowBias;
        uniform vec3 shadowLightDirection;
        
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
                for (int n = 0; n < 4; n++)
                    totalLight += lightCalculation( lightArray[n], position, normal );
                totalLight = min( totalLight, vec3(1,1,1) );
                baseColor *= vec4( totalLight, 1 );
            }

            if ( useFog )
            {
                float fogFactor = clamp( (fogEndDistance - cameraDistance)/(fogEndDistance - fogStartDistance), 0.0, 1.0 );
                baseColor = mix( vec4(fogColor,1.0), baseColor, fogFactor );
            }
            
            if ( receiveShadow )
            {
                // do not apply shadow if surface is facing away from directional light
                vec3 unitNormal = normalize(normal);
                float cosAngle = dot(unitNormal, shadowLightDirection);
                bool facingLight = (cosAngle < -0.05);
                
                vec3 shadowCoord = ( positionFromShadowLight.xyz / positionFromShadowLight.w ) / 2.0 + 0.5;
                float closestDistanceToLight = texture2D(shadowMap, shadowCoord.xy).r;
                float fragmentDistanceToLight = shadowCoord.z;
                // is this fragment in shadow?
                if (facingLight && fragmentDistanceToLight > closestDistanceToLight + shadowBias)
                    baseColor *= vec4( shadowStrength, shadowStrength, shadowStrength, 1.0 );
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

        