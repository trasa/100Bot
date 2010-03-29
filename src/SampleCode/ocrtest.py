'''
Created on Jan 6, 2010

@author: trasa
'''
from pytesser import *
import pygame
import sys
from pygame.locals import *

import StringIO

def printText(im):
    print image_to_string(im)
    

if __name__ == '__main__':
    RED = (255, 0, 0)
    pygame.init()
    screen = pygame.display.set_mode((2048,1536))
    pygame.display.set_caption('Webcam')
    
    img = pygame.image.load('IMG_1060.jpg')
    screen.blit(img, (0,0))
    
    # coordinates for the main question area.
    topLeft = (134, 586)
    bottomLeft= (134, topLeft[1]+396)
    topRight = (topLeft[0]+1870, topLeft[1])
    
    bottomRight = (topRight[0], bottomLeft[1])
    
    #pygame.draw.line(screen, RED, topLeft, bottomLeft)
    #pygame.draw.line(screen, RED, topLeft, topRight)
    #pygame.draw.line(screen, RED, bottomLeft, bottomRight)
    #pygame.draw.line(screen, RED, topRight, bottomRight)
    
    # extract the question part
    # we dont want to save this as an image to disk...need to extract a PIL image i think..?
    # or to a string buffer?
    rect = Rect(134, 586, 1870, 396) 
    questionSurface = screen.subsurface(rect)
    pygame.image.save(questionSurface, 'test.png')
    
    print image_file_to_string('test.png')
    
    pygame.display.flip()
    
    
    
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
    
    
    #screen = pygame.display.set_mode((2048,1536))
    
        
                
    
    #printText(Image.open('phototest.tif'))
    
    #printText(Image.open('../testImages/question_no_answer.png'))
    #printText(Image.open('test_question.png'))
    #printText(Image.open('test_question.png').convert('L'))
    #printText(Image.open('just_question_cropped_inverted.png').convert('L'))
    #printText(Image.open('v_sharpen.png').convert('L'))
    #printText(Image.open('v_sharpen_desaturate.png').convert('L'))
    #printText(Image.open('v_sharpen_desaturate.tiff').convert('L'))
    #printText(Image.open('v_sharpen_desaturate_invert.tiff').convert('L'))
#    printText(Image.open('v_sharpen_levels_contrast.tiff'))
#    printText(Image.open('v_sharpen_levels_x2.tiff'))
 
#    printText(Image.open('img_1056.jpg').convert('L'))
#    printText(Image.open('brady1.jpg'));
#    printText(Image.open('racing.jpg'));
#    printText(Image.open('clark1.jpg'));
#    printText(Image.open('pig1.jpg'));

