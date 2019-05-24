# static methods to load and compile OpenGL shader programs
from OpenGL.GL import *

import pygame # for loading images / texture data

class OpenGLUtils(object):

    @staticmethod
    def initializeShader(shaderCode, shaderType):
        
        extension = '#extension GL_ARB_shading_language_420pack : require\n'
        shaderCode = '#version 130\n' + extension + shaderCode
        
        # create empty shader object and return reference value
        shaderID = glCreateShader(shaderType)
        # stores the source code in the shader
        glShaderSource(shaderID, shaderCode)
        # compiles source code previously stored in the shader object
        glCompileShader(shaderID)

        # queries whether shader compile was successful
        compileSuccess = glGetShaderiv(shaderID, GL_COMPILE_STATUS)
        if not compileSuccess:
            # retreive error message
            errorMessage = glGetShaderInfoLog(shaderID)
            # free memory used to store shader program
            glDeleteShader(shaderID)
            # TODO: parse str(errorMessage) for better printing
            raise Exception(errorMessage)  
            
        # compilation was successful; return shader reference value
        return shaderID

    @staticmethod
    def initializeShaderFromCode(vertexShaderCode, fragmentShaderCode):
        
        vertexShaderID   = OpenGLUtils.initializeShader(vertexShaderCode,   GL_VERTEX_SHADER)
        fragmentShaderID = OpenGLUtils.initializeShader(fragmentShaderCode, GL_FRAGMENT_SHADER)
    
        programID = glCreateProgram()
        glAttachShader(programID, vertexShaderID)
        glAttachShader(programID, fragmentShaderID)
        glLinkProgram(programID)
        
        return programID

    """
    @staticmethod
    def initializeShaderFromFiles(vertexShaderFileName, fragmentShaderFileName):

        vertexShaderFile = open(vertexShaderFileName, mode='r')
        vertexShaderCode = vertexShaderFile.read()
        vertexShaderFile.close()

        fragmentShaderFile = open(fragmentShaderFileName, mode='r')
        fragmentShaderCode = fragmentShaderFile.read()
        fragmentShaderFile.close()
        
        return OpenGLUtils.initializeShaderFromCode(vertexShaderCode, fragmentShaderCode)
    """
    
    @staticmethod
    def initializeTexture(imageFileName):
        # load image from file
        surface = pygame.image.load(imageFileName)
        return OpenGLUtils.initializeSurface(surface)
        
    @staticmethod
    def initializeSurface(surface):
        # transfer image to string buffer
        textureData = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()
        # glEnable(GL_TEXTURE_2D)
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)

        # send image data to texture buffer
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
                     
        # generate a mipmap for use with 2d textures
        glGenerateMipmap(GL_TEXTURE_2D)
        
        # default: use smooth interpolated color sampling when textures magnified
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # use the mip map filter rather than standard filter
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        
        return texid

    @staticmethod
    def updateSurface(surface, textureID):
        textureData = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height() 
        glBindTexture(GL_TEXTURE_2D, textureID)
        # send image data to texture buffer
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
                     