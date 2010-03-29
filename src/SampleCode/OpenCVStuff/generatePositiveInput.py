'''
Check a directory for *.png files, generate a text file describing what's in there.

for use with opencv_createsamples, so we can merge
the images together into a .vec file.

Created on Dec 6, 2009

@author: trasa
'''
import os
import Image

rootDir = "C:/Projects/meancat/misc/100Bot/trunk/training/positive"
if __name__ == '__main__':
    for pngName in os.listdir(rootDir):
        #print pngName
        if pngName.split('.')[-1] == 'png':
            img = Image.open(rootDir + '/' + pngName)
            print '{name} 1 0 0 {width} {height}'.format(name=pngName, width=img.size[0], height=img.size[1])
        