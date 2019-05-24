from OpenGL.GL import *

class RenderTarget(object):

    def __init__(self, width=512, height=512):

        self.width = width
        self.height = height
        
        # create a framebuffer - a container for textures
        self.framebufferID = glGenFramebuffers(1)
        
        # "Bind" the newly created framebuffer: 
        #   all following framebuffer functions modify this
        #   until a new framebuffer is bound
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebufferID)
        
        # create a texture to render to
        self.textureID = glGenTextures(1)
        
        # "Bind" the newly created texture : all future texture functions will modify this texture
        glBindTexture(GL_TEXTURE_2D, self.textureID)

        # give an empty image to OpenGL ( the last "None" )
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
            0, GL_RGB, GL_UNSIGNED_BYTE, None)

        # configure simplest filtering
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        # configure framebuffer to store to this texture
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.textureID, 0)
        
        # Since a frame buffer only stores color information by default,
        #   need to generate a buffer to store depth information while rendering the scene
        self.depthBufferID = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.depthBufferID)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height);
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.depthBufferID);

        # Always check that our framebuffer is ok
        if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE):
            raise Exception("Framebuffer status error")
        