
# http://imdbpy.sourceforge.net/support.html#documentation
import imdb

#from mysql import MySQLDatabase

# For the search&replace of bad characters
import re

DEBUG = 0

#ia = imdb.IMDb()


class IMDataBase:
    def __init__ (self) :
        try:
            self.ia = imdb.IMDb()
            if DEBUG == 1:
                print "Connected to IMDB!"
        except:
            print "ERROR Connecting to IMDB"

    # def __del__( self ):
    #     if hasattr(self, 'db'): # close our connection to free it up in the pool
    #         self.db.close()
    #         if DEBUG == 1:
    #             print "MySQL Connection closed"


    # Free test search in IMDB when the search is not present in the DB
    def get_movies_by_name(self,search):
        #ia = imdb.IMDb()
        s_result = self.ia.search_movie( search )
        if s_result:
            if DEBUG == 1:
                print "s_result:",s_result
                for item in range(0,len(s_result)):
                    print "item:",s_result[item].data
            return s_result
        else:
            if DEBUG == 1:
                print "No movies found!"
            return {}

