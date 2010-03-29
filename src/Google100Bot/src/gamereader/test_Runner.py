'''
Created on Feb 8, 2010

@author: trasa
'''
import unittest
from Runner import *


class Test(unittest.TestCase):


    def testMouseMoveWhenNotDraggingDoesNothing(self):
        dr = DragRectangle()
        dr.onMouseMove((10, 10))
        self.assertEqual(dr.initialPoint, (0,0))
        self.assertEqual(dr.size,  (0,0))
    
    def testCompleteCycleGeneratesCorrectCoords(self):
        dr = DragRectangle()
        dr.onMouseDown((10, 10))
        dr.onMouseMove((20, 20))
        dr.onMouseUp((30, 30))
        self.assertEqual(dr.initialPoint, (10, 10))
        self.assertEqual(dr.size, (20, 20))
                         
    
    def testWhenStartingAnotherMouseDown_ResetsState(self):
        dr = DragRectangle()
        dr.onMouseDown((10,10)) # start first op
        dr.onMouseMove((15, 15))
        dr.onMouseUp((20, 20))
        
        dr.onMouseDown((50, 50))
        self.assertEqual(dr.size, (0,0))
        self.assertEqual(dr.initialPoint, (50,50))
            

    def testGameAreasReturnsStaticRectangles(self):
        areas = GameAreas()
        state = ScreenState()
        state.currentState = ScreenState.DrawAnswer2
        areas.getDragRectangle(state).size = (50,50)
        self.assertEqual(areas.getDragRectangle(state).size, (50, 50))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()