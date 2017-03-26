'''
Created on Jan 21, 2014

This application is, in function, an RSS feed monitoring application, which
when called, fetches the RSS feed, checks each item for matches to a search
dictionary (not to be confused with Python Dictionaries), checks those matches
against all previous matches, skipping them, and finally  notifying the user
of the match.

Ideally, this will become a learning platform for me, so that I can try out and
play with new technologies (databases, in particular), within this simple
framework. 

@author: softpot9
'''

from storage.SQLiteStore import SQLiteStore
import sys
import os
import re
import ConfigParser
from rssparsers import feedburner
from notifiers import EmailNotifier
from notifiers import StdoutNotifier


class RSSScanReport:
    '''
    This didn't have to be a class, I suppose. A set of functions might have
    been sufficient. I'm still trying to break my Java-inspired 'everything
    must be a class' frame of mind. I'm sure you'll agree that this actually
    works just fine as a class.
    '''
    
    config_file = None
    
    config = None
    
    def __init__(self, config_file):
        '''
        Constructor
        
        @param config_file: path to the configuration file.
        '''
        
        #Fetch the configuration file, and parse the RSS parameters.
        self.config_file = config_file
        
        self.config = ConfigParser.ConfigParser()
    
        try:
            
            self.config.readfp(open(config_file))
            
        except IOError:
            
            sys.stderr.write("Configuration file '" + config_file + "' not found")
            
            sys.exit()
            
    
    def run(self):
        '''
        Run the RSS feed scanner, check for matches, compare matches with
        previous-match database, send notifications.
        '''

        rss_url = self.config.get("RSS", "url")

        rss_matches = re.split('/[,\s]*/', self.config.get("RSS", "matches").strip('/'))

        #fetch the RSS feed content
        parser = feedburner.FeedburnerParser(rss_url)
        
        matched_messages = parser.search(rss_matches)
        
        store = SQLiteStore(self.config_file)
        
        #remove previous matches
        for unique_key in matched_messages.keys():
            
            if not store.test(unique_key):
                
                matched_messages.pop(unique_key)

        #handle what's come back
        if len(matched_messages) > 0:
            
            self.handle_matches_found(matched_messages)

        else:
            
            self.handle_no_matches()
        
        
    def active_notifiers(self):
        '''
        Fetches the notifiers which have been activated.
        
        @return: List of notifiers.
        '''
        
        active_notifiers = []
            
        #Stdout Notifier - outputs text to terminal, in 'markdown format'
        if self.config.getboolean("Stdout Notifier", "stdoutNotifications"):
            
            active_notifiers.append(StdoutNotifier.StdoutNotifier(self.config_file))
    
        #SMTP Email Notifier - sends an email
        if self.config.getboolean("Email Notifier", "emailNotifications"):
            
            active_notifiers.append(EmailNotifier.SMTPEmailNotifier(self.config_file))
            
        return active_notifiers


    def handle_matches_found(self, matched_messages):
        '''
        Given the set of matched_messages, send out appropriate notifications
        via the activated notifier methods.
        
        @param matched_messages: A list of the matches to be included in
            the notifications. 
        '''
        
        notification_message = "<p>The following RSS item matches were detected:</p>\n\n" + "\n".join(matched_messages.itervalues())
        
        active_notifiers = self.active_notifiers()
        
        #activate all active notifiers with matches
        for active_notifier in active_notifiers:
            
            active_notifier.notify("RSSScanReport Match Found!", notification_message)


    def handle_no_matches(self):
        '''
        Action to be taken when no results come back
        '''
        
        active_notifiers = self.active_notifiers()
        
        #activate all active notifiers with matches
        for active_notifier in active_notifiers:
            
            active_notifier.no_matches()


if __name__ == '__main__':
    
    rsr = RSSScanReport(os.path.dirname(os.path.realpath(__file__)) + "/RSSScan.conf")
    
    rsr.run()
