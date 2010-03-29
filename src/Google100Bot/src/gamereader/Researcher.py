'''
Created on Feb 11, 2010

@author: trasa
'''
from QuestionDatabase import QuestionDB
from gquery.Wizard import * 

class Researcher(object):
    '''
    Responsible for trying to figure out which answer is correct, using any means necessary.
    '''


    def __init__(self, question, potentialAnswers):
        self.db = QuestionDB()
        self.question = question
        self.potentialAnswers = potentialAnswers
        
    def guess(self):
        ''' Guess which of these answers is correct.  Returns the index of the answer or None if we have got no clue. '''
        i = self.guessDB()
        if i == None:
            i = self.guessWiz()
        return i 
        
    
    def guessDB(self):
        ''' Try to find the answer in the database '''
        ans = self.db.getAnswer(self.question)
        return self.findInList(ans)
        
        
    def guessWiz(self):
        ''' Try to find the answer via the gquery Wizard. '''
        ans = Wizard(self.question, self.potentialAnswers).guess()
        return ans.getValue()
        
        
    def findInList(self, ans):
        if ans == None:
            return None
        try:
            i = self.potentialAnswers.index(ans)
            return i
        except ValueError:
            return None
        
        