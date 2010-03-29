'''
Created on Oct 4, 2009

@author: trasa
'''

import urllib2
import simplejson

class Query(object):
    '''
    Handles making a query to Google Search API via RESTful interface.
    '''
    def __init__(self):
        self.urlBase = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='
        self.headers = {'Referer': 'meancat.com'}

    def execute(self, query):
        ''' Go ask Google for the results to this query. '''
        
        # wrapping in quotes tends to return zero results from google:
        #query = '"' + query + '"'
        
        url = self.urlBase + urllib2.quote(query)
        print url
        request = urllib2.Request(url, None, self.headers)
        response = urllib2.urlopen(request)        
        results = simplejson.load(response)
        
        return [r for r in results['responseData']['results']]
        