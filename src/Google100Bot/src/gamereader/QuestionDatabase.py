'''
QuestionDatabase - records of questions we've seen and (hopefully) what the correct answer was.

Uses adodbapi to access SQL Server via ODBC,
which implements Python DB API v2.0 
included as part of Python for Windows Extensions - http://sourceforge.net/projects/pywin32/

Created on Feb 9, 2010

@author: trasa
'''
import sys
import adodbapi

class QuestionDB(object):
    
    def __init__(self):
        self.conn = adodbapi.connect('DSN=100Bot;Uid=QuestionUser;Pwd=Quest') 
    
    def addQuestion(self, question, answer, position):
        self.conn.cursor().callproc('addQuestion', (question, answer, position))

    def getAnswer(self, question):
        cur = self.conn.cursor()
        cur.execute('SELECT KnownAnswer FROM Questions WHERE QuestionText = ?', [question])
        row = cur.fetchone()
        if row == None:
            return None
        return row[0]

if __name__ == '__main__':
    conn = adodbapi.connect('DSN=100Bot;Uid=QuestionUser;Pwd=Quest')
    crsr = conn.cursor()
    crsr.execute('SELECT * FROM Questions')
    rs = crsr.fetchone()
    print rs