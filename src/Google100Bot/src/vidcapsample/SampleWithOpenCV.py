from VideoCapture import Device
from PIL import Image, ImageEnhance, ImageDraw
import sys, pygame, time
from pygame.locals import *

import cv

 
def frameiter(cap=None):
    if cap is None:
        # set up capture and tell it to get 640x480
        cap = cv.CaptureFromCAM(0)
        cv.SetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        cv.SetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
    while True:
        img = cv.QueryFrame(cap)
        yield img

def detect(image):
    imgSize = cv.GetSize(image)
    # create grayscale
    grayscale = cv.CreateImage(imgSize, 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
        
     
# main
cascade = cv.LoadHaarClassifierCascade('1v100.xml')

pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption('Webcam')
pygame.font.init()
font = pygame.font.SysFont("Courier",11)
it = frameiter()
storage = cv.CreateMemStorage(0)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
            
    img = it.next()

    #detect(img)
    
    # convert cv image to pygame screen
    camshot = pygame.image.frombuffer(img.tostring(), cv.GetSize(img), "RGB")
    
    screen.blit(camshot, (0,0))
    pygame.display.flip()