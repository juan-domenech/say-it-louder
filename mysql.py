import MySQLdb as _mysql

# http://imdbpy.sourceforge.net/support.html#documentation
#import imdb

#import imdb_module
from imdb_module import IMDataBase

# For the search&replace of bad characters
import re

DEBUG = 1

imDB = IMDataBase()

#ia = imdb.IMDb()

class MySQLDatabase:
    def __init__ (self, database_name, username, password, host='localhost') :
        try:
            self.db = _mysql.connect(db=database_name,
                                     host=host,
                                     user=username,
                                     passwd=password,
                                     use_unicode=True,
                                     charset="utf8")
            self.database_name=database_name
            if DEBUG == 1:
                print "Connected to MySQL!"
        except _mysql.Error, e:
            print e


    def __del__( self ):
        if hasattr(self, 'db'): # close our connection to free it up in the pool
            self.db.close()
            if DEBUG == 1:
                print "MySQL Connection closed"


    # Check whether this search string is stored in DB
    def check_search(self,search):
        self.db.commit()
        # Compare the search string with all the previous stored searches and return the search_id
        sql = "SELECT search_id FROM searches WHERE search='"+search+"';"
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        search_id = cursor.fetchone()
        if search_id:
            if DEBUG == 1:
                print "Found search_id:",search_id
            cursor.close()
            return search_id[0]
        else:
            if DEBUG == 1:
                print "Search not found in DB"
            cursor.close()
            return False


    # # Free test search in IMDB when the search is not present in the DB
    # def get_movies_by_name(self,search):
    #     ia = imdb.IMDb()
    #     s_result = ia.search_movie( search )
    #     if s_result:
    #         if DEBUG == 1:
    #             print "s_result:",s_result
    #             for item in range(0,len(s_result)):
    #                 print "item:",s_result[item].data
    #         return s_result
    #     else:
    #         if DEBUG == 1:
    #             print "No movies found!"
    #         return {}


    # Get from DB all the movies under the same search_id
    def get_movies_by_stored_search(self, search_id, kind):
        self.db.commit()
        movies_clean = []
        #sql = "SELECT * FROM movies WHERE search_id='"+str(search_id)+"';"
        sql = "SELECT * FROM movies INNER JOIN movies_searches on movies.movieID = movies_searches.movieID and movies_searches.search_id = '"+str(search_id)+"' and movies.kind ='"+str(kind)+"';"
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        movies = cursor.fetchall()
        cursor.close()
        if len(movies):
            if DEBUG == 1:
                print "Return from DB"
                for item in range(0,len(movies)):
                    print movies[item]
            for movie in movies:
                movies_clean.append(self.movie_from_tuple_to_dictionary(movie))
            if DEBUG == 1:
                print "movies_clean:",movies_clean
            return movies_clean
        else:
            if DEBUG == 1:
                print "Something went wrong. No movies stored under this search_id:", search_id
            # Delete invalid search ID as workaround
            self.remove_invalid_search_id(search_id)
            return False


    # Remove search_id that has no associated movies
    def remove_invalid_search_id(self,search_id):
        sql = "DELETE FROM searches WHERE search_id='"+str(search_id)+"';"
        if DEBUG == 1:
            print "Removing search_id from searches:", search_id
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        #self.db.commit()

        sql = "DELETE FROM movies_searches WHERE search_id='"+str(search_id)+"';"
        if DEBUG == 1:
            print "Removing search_id from movies_searches:", search_id
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)

        cursor.close()

        self.db.commit()
        return


    # Convert a tupple containing the movie information to an object following IMDB module format
    def movie_from_tuple_to_dictionary(self, movie):
        result = {}
        result['movieID'] = int(str(movie[0]))
        result['title'] = movie[1]
        result['year'] = movie[2]
        result['time_stamp'] = str(movie[7])
        if movie[3]:
            result['kind'] = movie[3]
        if movie[4]:
            result['episode of'] = movie[4]
        if movie[5]:
            result['series year'] = movie[5]
        if movie[6]:
            result['akas'] = movie[6]
        return result


    #
    def insert_search(self, search):
        sql = "INSERT INTO searches (search) VALUES ('"+str(search)+"');"
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)

        cursor.close()

        # Let's do commit as a last step instead
        #self.db.commit()

        # Recover search_id that the autoincrement has created for us from the last Insert
        return self.check_search(search)


    # Create simplified object with only the properties we are interested on
    def normalize_imdb_response(self, s_result):
        movies = []
        for item in s_result:
            movie = {}
            movie['movieID'] = int(item.movieID)
            movie['year'] = 2155
            if DEBUG == 1:
                print "item.data:",item.data
            for item_data in item.data:
                # Add new property&value to the object that are present in .data object
                movie[item_data] = item.data[item_data]
                if DEBUG == 1:
                    print "item_data:",item_data, "item.data[item_data]:",item.data[item_data]

            # Deal with the akas field format issue: Store only the first one
            if movie.has_key('akas'):
                movie['akas'] = movie['akas'][0]

            # Replace single quotes
            movie['title'] = re.sub("'", "\\'", movie['title'] )
            if movie.has_key('episode of'):
                movie['episode of'] = re.sub("'", "\\'", movie['episode of'] )
            if movie.has_key('akas'):
                movie['akas'] = re.sub("'", "\\'", movie['akas'] )

            movies.append(movie)
        return movies


    # Insert movies into DB
    def insert_movies_into_db(self, search_id, movies):

        if len(movies) == 0:
            print "ERROR: Something went terribly wrong. No movies present at insert_movies_into_db()"
            return False

        for movie in movies:

            # Using IGNORE to avoid duplicates (To Improve)
            sql = "INSERT IGNORE INTO movies ("
            # Let's try using REPLACE
            #sql = "REPLACE INTO movies ("
            sql_values = "VALUES ("

            for item in movie:
                if DEBUG == 1:
                    print "item:",item

                sql += "`"+str(item)+"`,"

                # Is the item and integer?
                if isinstance( movie[item], int):
                    sql_values += "'"+str(movie[item])+"',"
                else:
                    sql_values += "'"+movie[item]+"',"
                #sql_values += "'"+movie[item]+"',"

            sql = sql[:-1]+") "+(sql_values[:-1])+");"

            if DEBUG == 1:
                print sql
            cursor = self.db.cursor()
            cursor.execute(sql)

            # Update Join Table
            sql = "INSERT INTO movies_searches (movieID, search_id) VALUES ('"+str( movie['movieID'] )+"','"+str(search_id)+"');"
            if DEBUG == 1:
                print sql
            cursor = self.db.cursor()
            cursor.execute(sql)

            cursor.close()

        self.db.commit()

        return True


    # Search for similar movies in DB using LIKE and add to the final list
    def get_movies_by_like(self, search, movies ):

        self.db.commit()
        if not movies:
            movies = []

        movies_clean = []

        sql = "SELECT * FROM movies WHERE title LIKE '%"+search+"%';"
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        movies_from_db = cursor.fetchall()
        if len(movies_from_db):
            if DEBUG == 1:
                print "Return from DB:", len(movies_from_db)
                for item in range(0,len(movies_from_db)):
                    print movies_from_db[item]
            # Convert tuples to IMDB format
            for movie in movies_from_db:
                movies_clean.append(self.movie_from_tuple_to_dictionary(movie))

            if DEBUG == 1:
                if movies:
                    print "What we have from search_id:",len(movies)
                    for movie in sorted(movies):
                        print movie
                else:
                    print "ERROR: No movies from search:",search
                print "What we have from LIKE search:",len(movies_clean)
                for movie in sorted(movies_clean):
                    print movie

            # Add to movies the new additions from movie_clean
            movies_new = []
            for movie_clean in movies_clean:
                if movie_clean not in movies:
                    if DEBUG == 1:
                        print "Match found", movie_clean
                    movies_new.append(movie_clean)
            movies = movies + movies_new

            if DEBUG == 1:
                print "What we have combined:",len(movies)
                for movie in sorted(movies):
                    print movie

            cursor.close()
            return movies

        # Nothing to add from DB. Return what we already have.
        cursor.close()
        return movies


    #
    # Main "search by string" function
    #
    def search(self,search,kind='movie'):

        # Check whether this search already exists
        search_id = self.check_search(search)

        # The movie search exits in DB -> get the list of associated movies + return them
        if search_id:

            print "Cache Hit: #"+str(search_id)

            if DEBUG == 1:
                print "Search '"+search+"' found in DB with search_id:",search_id

            movies = self.get_movies_by_stored_search(search_id,kind)

            # We got and orphan search_id. get_movies_by_stored_search() will take care of it and delete it. Let's hope that get_movies_by_like() has something to offer
            if not movies:
                print "EXCEPTION: Orphan search_id:",search_id

            # Search for similar movies in DB using LIKE and add them to the final list
            movies = self.get_movies_by_like(search, movies)

            if movies:
                if DEBUG == 1:
                    print sorted(movies)
                return movies
            else:
                if DEBUG == 0 or DEBUG == 1:
                    print "ERROR: Something went wrong. No movies from a present search_id:", search_id
                # Exit with empty due error
                return []

        # The movie search doesn't exist in the DB -> Search IMDB + update DB + search by LIKE in DB + return them
        else:

            print "Cache Miss: '"+search+"'"

            if DEBUG == 1:
                print "Search '"+search+"' not found. Connecting to IMDB..."

            # Send search to IMDB
            # s_result = self.get_movies_by_name(search)
            s_result = imDB.get_movies_by_name(search)

            # No results -> break
            if len(s_result) == 0:
                if DEBUG == 0 or DEBUG == 1:
                    print "No movies found in IMDB, weird..."
                return []

            # Normalize response from IMDB API
            movies = self.normalize_imdb_response(s_result)

            # Store search string and get search_id that it belongs to
            search_id = self.insert_search(search)
            if search_id:
                if DEBUG == 1:
                    print "New search_id: %i for Search: %s" % ( search_id, search)
            else:
                if DEBUG == 0 or DEBUG == 1:
                    print "ERROR: Something went wrong: No search_id returned after INSERT"
                # Exit with empty due error
                return []

            # Insert Movies into DB and commit and check the exit status
            if self.insert_movies_into_db(search_id, movies):
                #self.db.commit()
                if DEBUG == 1:
                    for item in movies:
                        print item
                return movies
            else:
                return []


    def get_game_id_by_player_a(self,user_name):
        self.db.commit()
        sql = "SELECT game_id FROM games WHERE player_a ='"+user_name+"';"
        if DEBUG:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        game_id = cursor.fetchone()

        if game_id:
            game_id = game_id[0]

        if game_id:
            if DEBUG:
                print "Found game_id:",game_id
            cursor.close()
            return game_id
        else:
            if DEBUG:
                print "ERROR: Game_ID not found in DB"
            cursor.close()
            return False


    def create_game(self,user_name):
        sql = "INSERT INTO games (player_a) VALUES ('"+str(user_name)+"');"
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        cursor.close()
        self.db.commit()
        # Recover game_id that the autoincrement has created for us from the last Insert
        return self.get_game_id_by_player_a(user_name)


    def check_open_game(self):
        # Check for games where where is no Player B
        self.db.commit()
        sql = "SELECT game_id FROM games WHERE player_b IS NULL;"
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        # Let's get only one (in case more than one game is empty)
        game_id = cursor.fetchone()
        cursor.close()

        if game_id:
            game_id = game_id[0]

        if DEBUG:
            print 'Found open game:',game_id

        if game_id:
            # There is a game waiting.
            return game_id
        else:
            # No game waiting
            if DEBUG:
                print 'No open game. Creating a new one...'
            #game_id = self.create_game(user_name)
            return False


    # Join game as Player B
    def join_game(self,user_name,game_id):
        sql = "UPDATE `games` SET `player_b`='"+str(user_name)+"' WHERE `game_id`='"+str(game_id)+"';"
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        cursor.close()
        self.db.commit()
        return


    # Player B gives up
    def remove_player_b(self,game_id):
        sql = "UPDATE `games` SET `player_b`= NULL WHERE `game_id`='"+str(game_id)+"';"
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        cursor.close()
        self.db.commit()
        return

    def check_for_duplicate_user(self,user_name):
        self.db.commit()
        if DEBUG:
            print 'Checking wether player %s is already in the system...' % user_name
        sql = "SELECT game_id FROM games WHERE player_a ='"+user_name+"';"
        if DEBUG:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        game_id = cursor.fetchone()
        cursor.close()

        if game_id:
            if DEBUG:
                print "User already playing as Player A:"
            game_id = game_id[0]
            return game_id

        sql = "SELECT game_id FROM games WHERE player_b ='"+user_name+"';"
        if DEBUG:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        game_id = cursor.fetchone()
        cursor.close()

        if game_id:
            if DEBUG:
                print "User already playing as Player B:"
            game_id = game_id[0]
            return game_id

        if DEBUG:
            print 'This is a new user'
        return False


    # Update movieID
    def update_movieID(self,movieID, game_id):
        sql = "UPDATE `games` SET `movieID`= "+str(movieID)+" WHERE `game_id`= "+str(game_id)+";"
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()
        return


    # Update Keywords for A
    def update_keywords_a(self,keywords, game_id):
        sql = 'UPDATE `games` SET `keywords_a`="'+str(keywords)+'" WHERE `game_id`= '+str(game_id)+';'
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()
        return


    # Update Keywords for B
    def update_keywords_b(self,keywords, game_id):
        sql = 'UPDATE `games` SET `keywords_b`="'+str(keywords)+'" WHERE `game_id`= '+str(game_id)+';'
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()
        return


    def get_keywords_player_a_by_game_id(self, game_id):
        self.db.commit()
        sql = "SELECT keywords_a FROM games WHERE game_id = "+str(game_id)+";"
        if DEBUG:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()

        keywords = eval(result[0])
        if DEBUG:
            print "Keywords:",keywords
        return keywords


    def get_keywords_player_b_by_game_id(self, game_id):
        self.db.commit()
        sql = "SELECT keywords_b FROM games WHERE game_id = "+str(game_id)+";"
        if DEBUG:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()

        keywords = eval(result[0])
        if DEBUG:
            print "Keywords:",keywords
        return keywords


    # Update game solved
    def update_game_solved(self,game_id):
        sql = 'UPDATE `games` SET `solved`= 2 WHERE `game_id`= '+str(game_id)+';'
        if DEBUG == 1:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()
        return


    def get_movieID_by_game_id(self, game_id):
        self.db.commit()
        sql = "SELECT movieID FROM games WHERE game_id = "+str(game_id)+";"
        if DEBUG:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        movieID = cursor.fetchone()
        cursor.close()

        if movieID:
            movieID = movieID[0]

        if movieID:
            if DEBUG:
                print "Found movieID:",movieID
            return movieID
        else:
            if DEBUG:
                print "ERROR: movieID not found in DB"
            return False


    def get_movie_title_by_movieID(self,movieID):

        # Not necessary at the moment. We should have this information into MySQL
        #title, year = imDB.get_movie_title_by_movieID(movieID)

        self.db.commit()
        sql = "SELECT title, year FROM movies WHERE movieID = "+str(movieID)+";"
        if DEBUG:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()

        title = str(result[0])
        year = int(result[1])

        if DEBUG:
            print "From movieID: %i we got title: %s (%i)" % (movieID,title,year)

        return title,year



    # Get full list of games to provide Status
    def get_games(self):

        self.db.commit()
        sql = "SELECT * FROM games;"
        if DEBUG:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        result_temp = cursor.fetchall()
        cursor.close()

        if DEBUG:
            print result_temp

        result = []

        if result_temp:
            for item in result_temp:
                game = {}
                if item[0]:
                    game['game_id'] = int(item[0])
                else:
                    game['game_id'] = None
                if item[1]:
                    game['time_stamp'] = str(item[1])
                else:
                    game['time_stamp'] = None
                if item[2]:
                    game['player_a'] = str(item[2])
                else:
                    game['player_a'] = None
                if item[3]:
                    game['player_b'] = str(item[3])
                else:
                    game['player_b'] = None
                if item[4]:
                    game['movieID'] = int(item[4])
                else:
                    game['movieID'] = None
                if item[5]:
                    game['keywords_a'] = str(item[5])
                else:
                    game['keywords_a'] = None
                if item[6]:
                    game['keywords_b'] = str(item[6])
                else:
                    game['keywords_b'] = None
                if item[7]:
                    game['solved'] = int(item[7])
                else:
                    game['solved'] = None

                result.append(game)

        if DEBUG:
            print "Games:",result

        return result


    def get_player_a_by_game_id(self, game_id):
        self.db.commit()
        sql = "SELECT player_a FROM games WHERE game_id = "+str(game_id)+";"
        if DEBUG:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        player_a = result[0]
        if player_a:
            return player_a
        else:
            return False


    def get_player_b_by_game_id(self, game_id):
        self.db.commit()
        sql = "SELECT player_b FROM games WHERE game_id = "+str(game_id)+";"
        if DEBUG:
            print sql
        cursor = self.db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        player_b = result[0]
        if player_b:
            return player_b
        else:
            return False


