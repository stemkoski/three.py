from OpenGL.GL import *
from core import Mesh
from lights import Light

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
        fogColor = fog.uniformList.getUniformValue("fogColor")
        self.setClearColor(fogColor[0], fogColor[1], fogColor[2])
        
    def render(self, scene, camera, renderTarget=None, clearColor=True, clearDepth=True):

        # shadow rendering pass -------------------------------------------
        if self.shadowMapEnabled:
            
            # render objects in meshList from light's shadowCamera onto light's shadowMap
            
            # note: at present, only one shadow casting directional light is supported
            shadowCastLightList = scene.getObjectsByFilter( lambda x : isinstance(x, Light) and x.shadowCamera is not None )
            
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
                light.shadowCamera.uniformList.setUniformValue( "shadowProjectionMatrix", light.shadowCamera.getProjectionMatrix() )
                light.shadowCamera.uniformList.setUniformValue( "shadowViewMatrix", light.shadowCamera.getViewMatrix() )
                light.shadowCamera.uniformList.update( shadowProgramID )

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
                self.fog.uniformList.update( ID )

            # in case uniform values may have changed, update value first
            camera.uniformList.setUniformValue( "projectionMatrix", camera.getProjectionMatrix() )
            camera.uniformList.setUniformValue( "viewMatrix", camera.getViewMatrix() )
            camera.uniformList.update( ID )
 
            # update data for all the lights
            for light in lightList:

                light.uniformList.setUniformValue( "position", light.transform.getPosition() )
                light.uniformList.setUniformValue( "direction", light.getDirection() )
                light.uniformList.update( ID )

                # if castShadow, update variables containing shadow-related data that affect rendering
                # note: at present, only one shadow casting directional light is supported
                if light.shadowCamera is not None:
                    
                    # shadow camera uniform matrix values were updated during the shadow rendering pass,
                    #   here we need to send them to uniform variables in a different shader
                    light.shadowCamera.uniformList.setUniformValue("shadowLightDirection", light.getDirection() )
                    light.shadowCamera.uniformList.update( ID )

            # update model matrix, other uniforms, etc.
            # and then call the drawArrays function
            mesh.render( shaderProgramID = mesh.material.shaderProgramID )
