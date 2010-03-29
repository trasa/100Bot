'''
Created on Oct 4, 2009

@author: trasa
'''
from Query import Query
import urllib2

class Wizard(object):
    '''
    A Wizard figures out the most likely answer to a question.
    '''
    def __init__(self, question, possible_answers):
        self.question, self.possible_answers = question, possible_answers
        
    def guess(self):
        ''' Determine which answer is most likely, returning the percentage likelihood for each. '''
        pageData = self.execute_query()
        return self.determine_probabilities(pageData)
        
    
    def execute_query(self):
        ''' execute a GoogleQuery and return the list of PageData '''
        pageData = []
        for r in Query().execute(self.question):
            pageData.append(PageData(r['content'], self.get_page(r['url'])))
        return pageData
    
    def determine_probabilities(self, pageData):
        ''' Check each page in the list, figure out if the right answer is in there. '''
        probabilities = []
        for answer in self.possible_answers:
            prob = AnswerProbability(answer)
            probabilities.append(prob)
            for page in pageData:
                # include count of the word in the google summary:
                prob.search_context_count += page.context.count(answer)
                # determine if the answer is in the page itself:
                prob.page_count += page.fullPage.count(answer)
        return FinalAnswer(probabilities)
    
        
    def get_page(self, url):
        ''' retrieve the full text of the page. '''
        print 'getting %s' % url
        p = ""
        try:
            # TODO replace with better user agent..
            request = urllib2.Request(url, None, {'User-Agent' : 'PythonProject'} )
            response = urllib2.urlopen(request)        
            p = response.read()
            response.close()
        except urllib2.URLError, e:
                if hasattr(e, 'reason'):
                    print 'We failed to reach a server: ', e.reason
                elif hasattr(e, 'code'):
                    print "The server couldn't fulfill the request: ", e.code   
        finally:
            return p
        
        
class AnswerProbability(object):
    ''' Statistics about how likely this answer string is to be correct. '''    
    def __init__(self, answer):
        self.answer = answer
        self.search_context_count, self.page_count = 0, 0
    
    
    def total_count(self):
        return self.search_context_count + self.page_count
    
    def __str__(self):
        return "For Answer '%s', %d in contexts, %d in pages" % (self.answer,  self.search_context_count,  self.page_count)
    
    def __cmp__(self, other):
        return self.total_count() - other.total_count()


class FinalAnswer(object):
    ''' The list of AnswerProbabilities and the one that we think is the right answer. '''
    def __init__(self, probabilities):
        probabilities.sort()
        self.probabilities = probabilities
    
    def getValue(self):
        return self.probabilities[-1:][0].answer
    
    
class PageData(object):
    ''' Information about a page retrieved as part of the answer-finding process. '''
    def __init__(self, context, fullPage):
        self.context, self.fullPage = context, fullPage
            
        