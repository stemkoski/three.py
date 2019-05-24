from material import Material

class ShadowMaterial(Material):

    def __init__(self):

        # vertex shader code
        vsCode = """
        in vec3 vertexPosition; 
        uniform mat4 shadowProjectionMatrix;
        uniform mat4 shadowViewMatrix;
        uniform mat4 modelMatrix;      
        void main()
        {
            gl_Position = shadowProjectionMatrix * shadowViewMatrix * modelMatrix * vec4(vertexPosition, 1);
        }
        """
        # fragment shader code
        fsCode = """
        void main()
        {
            gl_FragColor = vec4(gl_FragCoord.z, gl_FragCoord.z, gl_FragCoord.z, 1);
        }
        """
        
        # initialize shaders
        super().__init__(vsCode, fsCode)
