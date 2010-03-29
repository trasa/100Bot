'''
Created on Feb 11, 2010

@author: trasa
'''
import unittest
from QuestionDatabase import QuestionDB

class Test(unittest.TestCase):


    def setUp(self):
        self.db = QuestionDB()
        pass


    def tearDown(self):
        pass


    def test_get_answer(self):
        self.assertEqual(self.db.getAnswer('Which 1995 movie used the tagline "A little pig goes a long way"?'), 'Babe')
        
    def test_get_answer_for_unknown_question(self):
        self.assertEqual(self.db.getAnswer('blah blah whatever.  this question doesnt exist.'), None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()