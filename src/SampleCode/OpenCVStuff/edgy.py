'''
Created on Nov 28, 2009

@author: trasa
'''

#import os; print os.environ['PATH']; 

import Image
import ImageFilter

if __name__ == '__main__':
    img = Image.open('question_no_answer.tif')
    img2 = img.filter(ImageFilter.FIND_EDGES)
    img2.save('edge.tif')    
    