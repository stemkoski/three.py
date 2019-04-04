import pygame

class Input(object):

    def __init__(self):
        self.keyDownList     = []
        self.keyPressedList  = []
        self.keyUpList       = []
        self.mouseButtonDown    = False
        self.mouseButtonPressed = False
        self.mouseButtonUp      = False
        self.quitStatus         = False
        # did the window resize since the last update?
        self.windowResize       = False
        self.windowWidth        = None
        self.windowHeight       = None
        
    def update(self):
        self.keyDownList = []
        self.keyUpList   = []
        self.mouseButtonDown = False
        self.mouseButtonUp   = False
        self.windowResize    = False
        for event in pygame.event.get(): # checks input events (discrete)
            if event.type == pygame.KEYDOWN:
                self.keyDownList.append( event.key )
                self.keyPressedList.append( event.key )
            elif event.type == pygame.KEYUP:
                self.keyPressedList.remove( event.key )
                self.keyUpList.append( event.key )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseButtonDown = True
                self.mouseButtonPressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseButtonPressed = False
                self.mouseButtonUp = True
            elif event.type == pygame.QUIT:
                self.quitStatus = True
            elif event.type == pygame.VIDEORESIZE:
                self.windowResize = True
                self.windowWidth = event.w
                self.windowHeight = event.h

    def isKeyDown(self, keyCode):
        return keyCode in self.keyDownList
    
    def isKeyPressed(self, keyCode):
        return keyCode in self.keyPressedList

    def isKeyUp(self, keyCode):
        return keyCode in self.keyUpList

    def isMouseDown(self):
        return self.mouseButtonDown

    def isMousePressed(self):
        return self.mouseButtonPressed

    def isMouseUp(self):
        return self.mouseButtonUp

    def getMousePosition(self):
        return pygame.mouse.get_pos()

    def quit(self):
        return self.quitStatus
    
    def resize(self):
        return self.windowResize
        
    def getWindowSize(self):
        return { "width": self.windowWidth, "height": self.windowHeight }
        
