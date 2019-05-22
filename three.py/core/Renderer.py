from core import *
from OpenGL.GL import *
from lights import *

class Renderer(object):

    def __init__(self, viewWidth=512, viewHeight=512, clearColor=[0.75,0.75,0.75]):

        glEnable(GL_DEPTH_TEST)

        # enable transparency
        # glEnable(GL_TEXTURE_2D) # is this even useful?
        # glEnable(GL_ALPHA_TEST) # is this even useful?
        
        # use counterclockwise vertex order on triangles 
        # (consistent with the "right-hand rule" for vector cross product)
        glFrontFace(GL_CCW)
        
        glEnable(GL_BLEND)
        
        # needed for antialiasing; also need to configure in window settings
        glEnable( GL_MULTISAMPLE )        

        # allow setting of point size from vertex shader; needed for point attenuation
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE) 
        glEnable( GL_POINT_SPRITE )

        # set default screen dimensions
        self.setViewport(0,0, viewWidth,viewHeight)

        self.clearColor = clearColor
        
        self.fog = None
        self.shadowMapEnabled = False
        
    # define the location/size of the rendered output in the window
    def setViewport(self, left=0, bottom=0, width=512, height=512):
        self.left = left
        self.bottom = bottom
        self.screenWidth = width
        self.screenHeight = height
        
    def setViewportSize(self, width, height):
        # define the location/size of the rendered output in the window
        self.screenWidth = width
        self.screenHeight = height

    # color(rgba) used for clearing the screen background
    def setClearColor(self, red, green, blue):
        self.clearColor = [red,green,blue]
    
    def setFog(self, fog):
        self.fog = fog
        self.setClearColor(fog.color[0], fog.color[1], fog.color[2])
        
    def render(self, scene, camera, renderTarget=None, clearColor=True, clearDepth=True):

        # shadow rendering pass -------------------------------------------
        if self.shadowMapEnabled:
            
            # render objects in meshList from light's shadowCamera onto light's shadowMap
            
            # note: at present, only one shadow casting directional light is supported
            shadowCastLightList = scene.getObjectsByFilter( lambda x : isinstance(x, Light) and x.castShadow )
            
            # only store depth data for objects which are set to cast a shadow on other objects
            shadowCastMeshList = scene.getObjectsByFilter( lambda x : isinstance(x, Mesh) and x.castShadow )

            for light in shadowCastLightList:
                
                # set render target properties
                glBindFramebuffer(GL_FRAMEBUFFER, light.shadowRenderTarget.framebufferID)
                glViewport(0,0, light.shadowRenderTarget.width, light.shadowRenderTarget.height)
            
                glClearColor(1,0,1,1)
                glClear(GL_COLOR_BUFFER_BIT)
                glClear(GL_DEPTH_BUFFER_BIT)
            
                # activate shader
                shadowProgramID = light.shadowMaterial.shaderProgramID
                glUseProgram( shadowProgramID )
                
                # reduce number of matrix inversions to improve performance
                light.shadowCamera.updateViewMatrix()
                
                light.shadowCamera.uniformList["projectionMatrix"].value = light.shadowCamera.getProjectionMatrix()
                light.shadowCamera.uniformList[      "viewMatrix"].value = light.shadowCamera.getViewMatrix()            
                for uniform in light.shadowCamera.uniformList.values():
                    uniform.update( shadowProgramID )

                for mesh in shadowCastMeshList:
                    mesh.render( shaderProgramID = shadowProgramID )
 
                    
        # standard rendering pass -------------------------------------------
        glClearColor(self.clearColor[0], self.clearColor[1], self.clearColor[2], 1)
        
        # activate render target
        if (renderTarget == None):
            # set render target to window
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glViewport(self.left, self.bottom, self.screenWidth, self.screenHeight)
        else:
            # set render target properties
            glBindFramebuffer(GL_FRAMEBUFFER, renderTarget.framebufferID)
            glViewport(0,0, renderTarget.width, renderTarget.height)

        # clear specified buffers
        if clearColor:
            glClear(GL_COLOR_BUFFER_BIT)
        if clearDepth:
            glClear(GL_DEPTH_BUFFER_BIT)
            
         
        meshList = scene.getObjectsByFilter( lambda x : isinstance(x, Mesh) )
        lightList = scene.getObjectsByFilter( lambda x : isinstance(x, Light) )
        
        # reduce number of matrix inversions (to improve performance)
        camera.updateViewMatrix()
        
        for mesh in meshList:

            # activate correct shader program
            ID = mesh.material.shaderProgramID
            glUseProgram( ID ) 
           
            if self.fog is not None:
               for uniform in self.fog.uniformList.values():
                    uniform.update( ID )

            # in case uniform values may have changed, update value first
            camera.uniformList["projectionMatrix"].value = camera.getProjectionMatrix()
            camera.uniformList[      "viewMatrix"].value = camera.getViewMatrix()            
            for uniform in camera.uniformList.values():
                uniform.update( ID )

            # TODO: move this to Mesh uniformList
            receiveShadowVarID = glGetUniformLocation(ID, "receiveShadow")
            if receiveShadowVarID != -1 and mesh.receiveShadow:
                glUniform1i( receiveShadowVarID, 1 )
            
            # TODO: store light data in Uniform objects also
            # update light data
            lightCount = len(lightList)            
            glUniform1i( glGetUniformLocation(ID, "lightCount"), lightCount )

            # update data for all the lights
            lightIndex = 0
            for light in lightList:
                lightName = "light" + str(lightIndex)
                glUniform1i( glGetUniformLocation(ID, lightName+".isAmbient"), light.isAmbient )
                glUniform1i( glGetUniformLocation(ID, lightName+".isDirectional"), light.isDirectional )
                glUniform1i( glGetUniformLocation(ID, lightName+".isPoint"), light.isPoint )
                glUniform3f( glGetUniformLocation(ID, lightName+".color"), light.color[0], light.color[1], light.color[2] )
                glUniform1f( glGetUniformLocation(ID, lightName+".strength"), light.strength )
                
                position = light.transform.getPosition()
                glUniform3f( glGetUniformLocation(ID, lightName+".position"), position[0], position[1], position[2] )
                
                if light.isDirectional == 1:
                    direction = light.getDirection()
                    glUniform3f( glGetUniformLocation(ID, lightName+".direction"), direction[0], direction[1], direction[2] )
                
                # if castShadow, update variables containing shadow-related data
                # note: at present, only one shadow casting directional light is supported
                if light.castShadow:
                    glUniformMatrix4fv( glGetUniformLocation(ID, "shadowLightProjectionMatrix"), 1, GL_TRUE, light.shadowCamera.getProjectionMatrix() )
                    glUniformMatrix4fv( glGetUniformLocation(ID, "shadowLightViewMatrix"), 1, GL_TRUE, light.shadowCamera.getViewMatrix() )
                    
                    glUniform1f( glGetUniformLocation(ID, "shadowStrength"), light.shadowStrength )
                    glUniform1f( glGetUniformLocation(ID, "shadowBias"), light.shadowBias )
                    
                    direction = light.getDirection()
                    glUniform3f( glGetUniformLocation(ID, "shadowLightDirection"), direction[0], direction[1], direction[2] )
                    
                    # send shadow map texture data (slot 0)
                    glUniform1i( glGetUniformLocation(ID, "shadowMap"), 0 )
                    # activate texture slot
                    glActiveTexture( GL_TEXTURE0 + 0 )
                    # associate texture data reference to currently active texture slot
                    glBindTexture( GL_TEXTURE_2D, light.shadowRenderTarget.textureID )
                    
                    # when rendering shadow map texture, anything fragment out of bounds of the shadow camera frustum 
                    #   should fail the depth test (not be drawn in shadow), so set R component to 1.0
                    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, [1.0, 1.0, 1.0, 1.0]);
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
            
                lightIndex += 1
                
            # update model matrix, other uniforms, etc.
            # and then call the drawArrays function
            mesh.render( shaderProgramID = mesh.material.shaderProgramID )
            
