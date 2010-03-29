'''
Interactive 'bot' to answer trivia questions using
google and wikipedia.

Created on Oct 4, 2009

@author: trasa
'''
from BotHarness import BotHarness

if __name__ == '__main__':
    print '100Bot awaiting your query.'
    bot = BotHarness()
    bot.guess("who had most home runs in Major League Baseball in 2008?",
          ["Alex Rodriguez", "Ryan Howard", "Prince Fielder"])
    
    bot.guess("who was MVP in the 2008 Major League Baseball All-Star Game?",
          ["J. D. Drew", "Alex Rodriguez", "Prince Fielder"])

    bot.guess("What is the capital of Chile?",
          ["Santiago", "Lima", "San Miguel"])
    
    bot.guess("What is the capital of the United States?",
         ["Washington", "New York", "Los Angeles"])
    bot.printResults()
    
#    while True:    
#        question = raw_input('What\'s the question? ').strip()
#        if isExit(question):
#            print 'Quitting...'
#            break
#        possibleAnswers = raw_input('Possible answers separated by quotes?').strip().split()
#        q = Query()
#        print q.execute(question)

        
def isExit(queryString):
    queryString = queryString.lower()
    return queryString == 'quit' or queryString == 'exit'

