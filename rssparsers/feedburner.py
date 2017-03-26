import feedparser
import re
import sha

class FeedburnerParser(object):
    '''
    This class will parse an RSS into 'matched items', based on the url given
    to it, and the 'matches list' of regular expressions against which the
    items are compared. 
    '''

    parser = None

    def __init__(self, url):
        '''
        Constructor
        '''

        self.parsed = feedparser.parse(url)


    def search(self, matches_list):
        '''
        @param regex: a regular express which should be matched against each
                    component of an item should be matched
        '''
        
        matchable_fields = ['title','link','comments','description']

        #the messages for all matches.
        messages = {}
        
        #check each item for a match.
        for item in self.parsed['items']:

            unique_key = sha.new(item['link']).hexdigest()

            message = "<p><ul>\n"

            #flag for tracking matches            
            is_match = False

            #check each matchable field...
            for key in matchable_fields:

                #...if that field even existed
                try:
                    
                    #check if this item makes a match.
                    for match_candidate in matches_list:
                        
                        if not is_match and re.search(match_candidate, item[key], re.IGNORECASE):
                            
                            is_match = True
                            
                    #add this item component to the message string
                    message += "<li>"+key+": "+item[key]+"</li>\n"
                
                #ignore if the field didn't exist.
                except KeyError:
                    None

            #check the match
            if is_match:
                messages[unique_key] = message + "</ul></p>\n"
                
        
            
        return messages
