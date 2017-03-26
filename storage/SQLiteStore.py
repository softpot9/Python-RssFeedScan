import ConfigParser
import sqlite3
import os

class SQLiteStore(object):
    '''
    This class is an interface to an SQLlite storage engine, for the purposes
    of testing whether a hash_value has been seen before. This class performs
    the necessary lock-safe testing to ensure that a hash value will only be
    interacted with once, by the RSS Scan Report.
    '''

    conn = None

    def __init__(self, config_file):
        '''
        Constructor

        Parses the config file for determining where the storage engine is, and
        how it should be accessed.
        '''

        #Parse the configuration file
        config = ConfigParser.ConfigParser()

        config.readfp(open(config_file))

        self.conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "/rssqlite.db")

        self.conn.execute('CREATE TABLE IF NOT EXISTS rssHashes(hash_value TEXT PRIMARY KEY, tstamp TIMESTAMP)')

    def test(self, hash_value):
        '''
        Checks if the requested hash value is in the database, and either
        stores it it isn't and returns true, or returns false if it's already
        in there.
        
        It's a /little/ bad form to rely on an exception for
        '''

        try:

            insert_params = (hash_value,)

            self.conn.execute("INSERT INTO rssHashes(hash_value, tstamp) VALUES(?, DATETIME('now') )", insert_params)

            self.conn.commit()

        #catch the exception for if the hash_value has previously been detected
        except sqlite3.IntegrityError:

            return False

        #everything turned out better than expected :)
        return True