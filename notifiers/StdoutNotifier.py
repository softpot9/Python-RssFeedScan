import html2text

class StdoutNotifier(object):
    '''
    The class is a notifier for RSS Scan Report. It simply outputs the match
    information to the terminal. It relies on the html2text library to produce
    markdown text.
    '''


    def __init__(self, params):
        '''
        Constructor
        '''


    def notify(self, subject, message):
        '''
        Output the subject and message, after converting the message html to
        markdown text.
        '''
        
        print " == " + subject + " == \n"
        
        print html2text.html2text(message)


    def no_matches(self):
        '''
        Handle not having found and matches.
        '''
        
        print "No matches were found"