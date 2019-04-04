import pygame

# note: font/background color should be specified with ranges [0-255], not [0-1]
# note: if image width/height not declared, will be set according to rendered text size
class TextImage(object):

    def __init__(self, text="Hello, world!", fontFileName=None, fontSize=24,
        fontColor=[0,0,0], backgroundColor=[255,255,255], transparent=False,
        antialias=True, width=None, height=None,
        alignHorizontal="LEFT", alignVertical="TOP"):
        
        self.text = text
        if fontFileName is None:
            self.font = pygame.font.SysFont("Arial", fontSize)
        else:
            self.font = pygame.font.Font(fontFileName, fontSize)

        self.fontColor = fontColor
        self.backgroundColor = backgroundColor
        self.transparent = transparent
        self.antialias = antialias
        self.width = width
        self.height = height
        self.alignHorizontal = alignHorizontal
        self.alignVertical = alignVertical
        
        self.renderImage()
        
    # can call to recaluate surface if text has changed
    def renderImage(self):
    
        # render text to surface
        fontSurface = self.font.render(self.text, self.antialias, self.fontColor)        
        # determine size of rendered text for alignment
        (textWidth, textHeight) = self.font.size(self.text)

        # if image dimensions are not specified, use font surface size as default
        if self.width is None:
            self.width = textWidth
        if self.height is None:
            self.height = textHeight
            
        # create image with transparency channel
        self.surface = pygame.Surface( (self.width, self.height), pygame.SRCALPHA )
        
        # background color used when not transparent
        if not self.transparent:
            self.surface.fill( self.backgroundColor )

        # values used for alignment; 
        #  only has an effect if image size is set larger than rendered text size
        if (self.alignHorizontal == "LEFT"):
            alignX = 0.0
        elif (self.alignHorizontal == "CENTER"):
            alignX = 0.5
        elif (self.alignHorizontal == "RIGHT"):
            alignX = 1.0
        if (self.alignVertical == "TOP"):
            alignY = 0.0
        elif (self.alignVertical == "MIDDLE"):
            alignY = 0.5
        elif (self.alignVertical == "BOTTOM"):
            alignY = 1.0
            
        textRect  = fontSurface.get_rect( topleft=(alignX*(self.width-textWidth),alignY*(self.height-textHeight) ) )

        self.surface.blit( fontSurface, textRect )

