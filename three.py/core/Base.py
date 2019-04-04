import pygame
import sys
import time

from core import *

class Base(object):

    def __init__(self):

        # initialize the pygame display and OpenGL context
        pygame.display.init()
        pygame.font.init()
        
        # load a custom icon
        pygame.display.set_icon(pygame.image.load("images/icon.png"))
        
        # initialize buffers to perform antialiasing
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
    
        self.setWindowTitle("   ")
        self.setWindowSize(640, 640)

        self.clock = pygame.time.Clock()
        self.deltaTime = 0
        self.input = Input()
        self.running = True

    # set window title
    def setWindowTitle(self, text):
        pygame.display.set_caption(text)

    # WARNING: calling this method loses the original OpenGL context;
    #   only use before calling OpenGL functions
    def setWindowSize(self, width, height):
        self.screenSize = (width, height)
        self.displayFlags = pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE
        self.screen = pygame.display.set_mode( self.screenSize, self.displayFlags )
        
    # implement by extending class
    def initialize(self):
        pass
    
    # implement by extending class
    def update(self):
        pass

    def run(self):

        self.initialize()
        
        while self.running:
        
            # update input state (down, pressed, up)
            self.input.update()
    
            if self.input.quit():
                self.running = False

            # debug tools
            
            # print FPS (Ctrl+F)
            if (self.input.isKeyPressed(pygame.K_LCTRL) or self.input.isKeyPressed(pygame.K_RCTRL)) and self.input.isKeyDown(pygame.K_f):
                fps = self.clock.get_fps()
                print( "FPS: " + str(int(fps)) )
                
            # save screenshot (Ctrl+S)
            if (self.input.isKeyPressed(pygame.K_LCTRL) or self.input.isKeyPressed(pygame.K_RCTRL)) and self.input.isKeyDown(pygame.K_s):
                timeString = str( int(1000 * time.time()) )
                fileName = "image-" + timeString + ".png"
                pygame.image.save(self.screen, fileName)
                
            self.deltaTime = self.clock.get_time() / 1000.0
            
            self.update()
            
            # display image on screen
            pygame.display.flip()

            # limit to 60 FPS
            self.clock.tick(60)

        # end of program
        pygame.quit()
        sys.exit()
        
    
