'''
Created on Nov 28, 2009

@author: trasa
'''
import sys
import pygame
from pygame.locals import *
from VideoCapture import *
from pytesser import *
from PIL import ImageEnhance
from Researcher import Researcher

# colors...
RED = (255, 0, 0)
BLUE = (0, 0, 255)

DISPLAY_PROPERTIES_POPUP = True  # use the camera's properties screen to set the resolution, instead of calling setResolution()
#CAMERA_RES = (960, 720)  # max res we can push out of this webcam  (the smaller logitech camera)
CAMERA_RES = (1280, 800)  # max res we can push out of this webcam (Microsoft LifeCam HD)


class QuestionScreen(object):
    
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
    
    def displayText(self, phrase, loc):
        s = self.font.render(phrase, True, (200, 200, 200))
        sh = self.font.render(phrase, True, (50, 50, 50))
        self.screen.blit(sh, (loc[0] + 1, loc[1] + 1))
        self.screen.blit(s, loc)


    def readImageText(self, rect):
        ''' Extract a rectangle from a surface, convert to an image, and OCR that image. '''
        r = rect.getRect()
        subsurface =self.screen.subsurface(r)
        print subsurface 
        pygame.image.save(subsurface, 'imgreader.png')
        return image_file_to_string('imgreader.png').strip()
    
    
class GameAreas(object):
    '''
    Describes the rectangles that make up the important parts of the question screen.
    ''' 
    
    def __init__(self):
        self.screenState = ScreenState()
        
        self.rects = {
                    ScreenState.DrawQuestion: DragRectangle(),
                    ScreenState.DrawAnswer0: DragRectangle(),
                    ScreenState.DrawAnswer1: DragRectangle(),
                    ScreenState.DrawAnswer2: DragRectangle()
                }         
    
    def getDragRectangle(self):
        return self.rects.get(self.screenState.currentState, None)
    
    def onMouseDown(self, currentPoint):
        dragRect = self.getDragRectangle()
        if dragRect != None:
            dragRect.onMouseDown(currentPoint)
    
    def onMouseMove(self, currentPoint):
        dragRect = self.getDragRectangle()
        if dragRect != None:
            dragRect.onMouseMove(currentPoint)
            
    def onMouseUp(self, currentPoint):
        dragRect = self.getDragRectangle()
        if dragRect != None: 
            dragRect.onMouseUp(currentPoint)
        
    def drawRectangles(self, screen):
        [pygame.draw.rect(screen, RED, dragRect.getRect(), 2)
         for dragRect in self.rects.values() if dragRect.isValid()]
        
    def isValid(self):
        return all([rect.isValid() for rect in self.rects.values()])

    def readyToCapture(self):
        return self.screenState.currentState == ScreenState.Capturing and self.isValid()
    

class DragRectangle(object):
    '''
    Enables Drag-n-Drop of Rectangles on the current screen surface.
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.mouseDrag = False
        self.initialPoint = (0, 0)
        self.size = (0, 0)

    def onMouseDown(self, currentPoint):
        self.mouseDrag = True
        self.initialPoint = currentPoint
        self.size = (0, 0)
        
        
    def onMouseMove(self, currentPoint):
        if self.mouseDrag:
            self.setEndPoints(currentPoint)
            
    def onMouseUp(self, currentPoint):
        self.mouseDrag = False
        self.setEndPoints(currentPoint)
        
    def getRect(self):
        return Rect(self.initialPoint, self.size)

    def setEndPoints(self, currentPoint): 
        self.size = (currentPoint[0] - self.initialPoint[0], currentPoint[1] - self.initialPoint[1]) 

    def isValid(self):
        return self.size != (0, 0)
   
        
class ScreenState(object):
    ''' Describes the State that the screen can be in. '''
    
    Waiting = 0
    DrawQuestion = 1
    DrawAnswer0 = 2
    DrawAnswer1 = 3
    DrawAnswer2 = 4
    Capturing = 5
    
    def __init__(self):
        self.currentState = ScreenState.Waiting
        self.descriptions = {
                             ScreenState.Waiting:       "Waiting",
                             ScreenState.DrawQuestion:  "Drawing Question",
                             ScreenState.DrawAnswer0:   "Drawing First Answer",
                             ScreenState.DrawAnswer1:   "Drawing Second Answer",
                             ScreenState.DrawAnswer2:   "Drawing Third Answer",
                             ScreenState.Capturing:     "Capturing Screen"
                             }
    def __str__(self):
        return self.descriptions[self.currentState]
            
class ImageCapture(object):
    
    def __init__(self):
        self.reset()
        self.cam = Device()
         
        # note: setResolution() doesn't, on the Microsoft LifeCam HD
        # instead you have to manually pick the correct resolution, otherwise you get an error.
        if DISPLAY_PROPERTIES_POPUP:
            self.cam.displayCapturePinProperties()
        else:
            self.cam.setResolution(CAMERA_RES[0], CAMERA_RES[1])


    def getImage(self):
        camshot = self._getImageFromCamera()
        camshot = ImageEnhance.Brightness(camshot).enhance(self.brightness)
        camshot = ImageEnhance.Contrast(camshot).enhance(self.contrast)
        return camshot
    
    def brightnessUp(self):
        self.brightness += 0.1
    
    def brightnessDown(self):
        self.brightness -= 0.1
        
    def contrastUp(self):
        self.contrast += 0.1
    
    def contrastDown(self):
        self.contrast -= 0.1

    def reset(self):
        self.brightness = 1.0
        self.contrast = 1.0

    def _getImageFromCamera(self):
        camshot = self.cam.getImage()
        # deal with race condition where getImage() might return none
        # if its called befor the camera is ready (problem happens with 
        # MS Lifecam images)
        while camshot == None: 
            camshot = self.cam.getImage()
        return camshot
    






if __name__ == '__main__':
    # initialize pygame, cameras, fonts, and the surface
    pygame.init()
    imgCapture = ImageCapture()

    screen = pygame.display.set_mode(CAMERA_RES)
    pygame.display.set_caption('1 vs 100 Game Reader')
    pygame.font.init()
    
    questionScreen = QuestionScreen(screen, pygame.font.SysFont("Courier", 20))
    gameAreas = GameAreas()
    
    while 1:
        camshot = imgCapture.getImage()
        camshot = pygame.image.frombuffer(camshot.tostring(), camshot.size, "RGB")
        screen.blit(camshot, (0, 0))
        
        # event handlers:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    gameAreas.screenState.currentState = ScreenState.Waiting
                    imgCapture.reset()
                elif event.key == pygame.K_1:
                    gameAreas.screenState.currentState = ScreenState.DrawQuestion
                elif event.key == pygame.K_2:
                    gameAreas.screenState.currentState = ScreenState.DrawAnswer0
                elif event.key == pygame.K_3:
                    gameAreas.screenState.currentState = ScreenState.DrawAnswer1
                elif event.key == pygame.K_4:
                    gameAreas.screenState.currentState = ScreenState.DrawAnswer2
                elif event.key == pygame.K_SPACE:
                    gameAreas.screenState.currentState = ScreenState.Capturing
                elif event.key == pygame.K_a:
                    imgCapture.brightnessUp()
                elif event.key == pygame.K_z:
                    imgCapture.brightnessDown()
                elif event.key == pygame.K_s:
                    imgCapture.contrastUp()
                elif event.key == pygame.K_x:
                    imgCapture.contrastDown()
                    
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gameAreas.onMouseDown(pygame.mouse.get_pos())
                
            elif event.type == pygame.MOUSEMOTION:
                gameAreas.onMouseMove(pygame.mouse.get_pos())
                
            elif event.type == pygame.MOUSEBUTTONUP:
                gameAreas.onMouseUp(pygame.mouse.get_pos())
            
        # draw our question/answer rectangles on the screen
        gameAreas.drawRectangles(screen)
        # note what mode we are currently in
        questionScreen.displayText("Mode: " + str(gameAreas.screenState), (10, 4))
        pygame.display.flip()
        
        # if we're capturing a question/answers, get the data and figure out what it is.
        if gameAreas.readyToCapture():
            
            rectText = [questionScreen.readImageText(rect) for rect in gameAreas.rects.values()]
            print rectText
            
            # Figure out what the correct answer is.
            res = Researcher(rectText[0], rectText[1:])
            print "my guess: " + res.guess()

            # and we go back to waiting.
            gameAreas.screenState.currentState = ScreenState.Waiting
            
            
        
        
