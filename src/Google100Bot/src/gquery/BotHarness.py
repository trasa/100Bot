'''

Created on Oct 13, 2009

@author: trasa
'''
from Wizard import Wizard

class BotHarness(object):
    '''
    Something to easily test the accuracy of the Wizard, 
    and record the # of questions vs the # of right answers.
    '''
    
    def __init__(self):
        self.totalQuestions, self.correctAnswers = 0, 0

    def guess(self, question, possibleAnswers):
        ''' Determine the correct answer to this question.  
            The 0th Possible Answer should be the true correct one. 
        '''
        print "Question: " + question
        
        self.totalQuestions += 1
        finalAnswer = Wizard(question, possibleAnswers).guess()
        
        print "All Results:"
        for prob in finalAnswer.probabilities:
            print prob
        
        success = ""
        if possibleAnswers[0] == finalAnswer.getValue():
            self.correctAnswers += 1
            success = "Right!"
        else:
            success = "WRONG!"
        
        print 'guess: %s, correct answer: %s, Wizard is %s\n' % (finalAnswer.getValue(),
                                                                   possibleAnswers[0],
                                                                   success)
            
    def printResults(self):
        ''' Display our accuracy percentage.
            Assumes that at least 1 question has been asked.
        '''
        print "out of %d questions, got %d right, success rate %0.2f" % (self.totalQuestions, self.correctAnswers, 
                                                                        float(self.correctAnswers) / self.totalQuestions)
                