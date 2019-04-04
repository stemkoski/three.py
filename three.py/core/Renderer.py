from core import *
from OpenGL.GL import *
from lights import *

class Renderer(object):

    def __init__(self):

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
        self.setViewport(0,0, 512,512)

        self.setClearColor(0.75,0.75,0.75, 1.0)
        
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
    def setClearColor(self, red, green, blue, alpha=1):
        glClearColor(red, green, blue, alpha)
    
    
    def render(self, scene, camera, renderTarget=None, clearColor=True, clearDepth=True):

        # activate render target
        if (renderTarget == None):
            # set render target to window
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glViewport(self.left, self.bottom, self.screenWidth, self.screenHeight)
        else:
            # set render target properties
            glBindFramebuffer(GL_FRAMEBUFFER, renderTarget.framebufferID)
            glViewport(self.left, self.bottom, renderTarget.width, renderTarget.height)

        # clear specified buffers
        if clearColor:
            glClear(GL_COLOR_BUFFER_BIT)
        if clearDepth:
            glClear(GL_DEPTH_BUFFER_BIT)
            
         
        meshList = scene.getObjectsByFilter( lambda x : isinstance(x, Mesh) )
        lightList = scene.getObjectsByFilter( lambda x : isinstance(x, Light) )
        
        for child in meshList: # scene.children:

            # activate correct shader program
            ID = child.material.shaderProgramID
            glUseProgram( ID )
           
            # update projection and view matrix uniforms
            projectionMatrixVarID = glGetUniformLocation(ID, "projectionMatrix")
            if projectionMatrixVarID != -1:
                glUniformMatrix4fv(projectionMatrixVarID, 1, GL_TRUE, camera.getProjectionMatrix() )
                
            viewMatrixVarID = glGetUniformLocation(ID, "viewMatrix")
            if viewMatrixVarID != -1:
                glUniformMatrix4fv(viewMatrixVarID, 1, GL_TRUE, camera.getViewMatrix() )
            
            # update light data
            lightCount = len(lightList)            
            glUniform1i( glGetUniformLocation(ID, "lightCount"), lightCount )

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
                direction = light.direction # apply rotation transform!
                glUniform3f( glGetUniformLocation(ID, lightName+".direction"), direction[0], direction[1], direction[2] )
                

                lightIndex += 1
                
            # update model matrix, other uniforms, etc.
            # and then call the drawArrays function
            child.render()
            
