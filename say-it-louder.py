from flask import Flask,make_response,render_template,redirect,session,escape,request,url_for

from mysql import MySQLDatabase
from imdb_module import IMDataBase

import json

db = MySQLDatabase('imdb','imdb','imdb','localhost')
# imDB = IMDataBase()

DEBUG = 1

# http://flask.pocoo.org/docs/0.10/quickstart/
app = Flask(__name__)
app._static_folder = '/Users/juan/say-it-louder/static/'

# set the secret key.  keep this really secret:
app.secret_key = 'This_is_a_secret'


######################################################################################################################
#                                        Main App and common options                                                 #
######################################################################################################################

@app.route('/')
def index():

    # if not 'user_name' in session:
    #     if DEBUG:
    #         print "Not logged in. Redirecting to /login"
    #     return redirect("/login")
    # user_name = session['user_name']
    #
    # # Check whether the user is already in a game
    # if session.has_key('game_id') :
    #     if DEBUG:
    #         print 'User in session[game_id]',session['game_id']
    #     #
    #     pass
    #     #
    #
    # else:
    #     # We are not in any game yet
    #     # Check DB for current games
    #     game_id = db.check_open_game()
    #     if DEBUG:
    #         print 'Return of check_open_game()',game_id
    #
    #     if game_id:
    #         # There is a game open. Joining!
    #         db.join_game(user_name,game_id)
    #         if DEBUG:
    #             print 'Joining game_id',game_id
    #         you_open_game = False
    #         session['game_id'] = game_id
    #
    #     else:
    #         # No game open. Let's open it!
    #         game_id = db.create_game(user_name)
    #         if DEBUG:
    #             print 'Created game_id',game_id
    #         you_open_game = True
    #         session['game_id'] = game_id
    #
    # return render_template('index.html', user_name = user_name, you_open_game = you_open_game)
    return render_template('index.html')


@app.route('/login')
def login_html():

    return render_template('login.html')


@app.route('/login_post', methods=['GET', 'POST'])
def login_post():
    # Method POST
    if request.method == 'POST':
        session['user_name'] = request.form['user_name']
        user_name = session['user_name']

        # Is the user already in the system?
        if db.check_for_duplicate_user( session['user_name'] ):
            if DEBUG:
                print 'User %s already in the system trying POST. Sending back to /login' % session['user_name']
            # Destroying session and send to retry to /login
            session.pop('user_name', None)
            return redirect('/#/login', code=302)

        # User not in the system
        else:
            # We are not in any game yet
            # Check DB for current games (Where there is no Player_B)
            game_id = db.check_open_game()
            if DEBUG:
                print 'Return of check_open_game()',game_id

            if game_id:
                # There is a game open. Joining!
                db.join_game(user_name,game_id)
                if DEBUG:
                    print 'Joining game_id',game_id
                session['player'] = 'B'
                session['game_id'] = game_id
                #return redirect('/resolve/movie_selected/'+str(game_id), code=302)
                return redirect('/resolve/', code=302)


            else:
                # No game open. Let's open it!
                game_id = db.create_game(user_name)
                if DEBUG:
                    print 'Created game_id',game_id
                session['player'] = 'A'
                session['game_id'] = game_id
                return redirect('/challenge/', code=302)


    # Method GET
    else:
        # User already with session but trying to log-in again
        if 'user_name' in session:
            user_name = session['user_name']
            if DEBUG:
                print "GET /login with user_name %s" % user_name

            return redirect('#/status', code=302)

        # No session detected and no POST? Render login.html
        else:
            #session.pop('user_name', None)
            return render_template('login.html')



@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_name', None)
    return redirect('/', code=302)


# Main Status page
@app.route('/status.html')
def status_html():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)
    user_name = session['user_name']

    response =  '<h2>Status Page</h2>'
    response += '<h3>Hello '+user_name+'!</h3>'
    if session['game_id']:
        response += '<h4>You are Player_'+session['player']+' in Game_ID:'+str(session['game_id'])+'</h4>'
    response += 'This is the current status:'

    game = ''
    games_total = db.get_games()

    response += '<ul>'
    for item in games_total:
        game_id = item['game_id']
        #game += '<h5>GameID:'+str(item['game_id'])+' Time_Stamp:'+item['time_stamp']+' Player_A:'+item['player_a']
        game += '<li>GameID:'+str(game_id)+' Player_A:'+item['player_a']
        if item.has_key('player_b'):
            game += ' Player_B:'+str(item['player_b'])

        if item.has_key('movieID'):
            # game += ' MovieID:'+str(item['movieID'])
            title,year = db.get_movie_title_by_movieID(item['movieID'])
            game += ' Title:"'+str(title)+'" ('+str(year)+')'

        # if item.has_key('keywords_a'):
        #     game += ' Keywords_A:'+str(item['keywords_a'])
        # if item.has_key('keywords_b'):
        #     game += ' Keywords_B:'+str(item['keywords_b'])
        #if item.has_key('solved'):
        #    game += ' Solved:'+str(item['solved'])

        # If the game is solved -> No options
        if (item['solved'] == 2):
            game += ' Solved'

        # When the game is not solved + Player_B is empty + Player_A is a different user-> Option to Join
        elif (item['solved'] != 2) and ( db.get_player_a_by_game_id(game_id) != user_name ) and ( db.get_player_b_by_game_id(game_id) == False ):
            game += ' <a href="/join_game/'+str(game_id)+'">Join</a>'

        # When the game is not solved and user_name is Player_B -> Option to continue playing
        elif (item['solved'] == None ) and ( db.get_player_b_by_game_id(game_id) == user_name ):
            game += ' <a href="/resolve/#/resolve/movie_selected/">Continue</a>'

        game += '</li>'

        response += game
        game = ''
    response += '</ul>'

    # When the games we have started are all of them solved -> Give the option to create a new one
    #if
    
    if DEBUG:
        print response

    return response


@app.route('/search_movie')
def search_movie():

    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)
    #user_name = session['user_name']

    return render_template('search_movie.html')



@app.route('/search/<title>')
def imdb_search(title):

    result = '<!DOCTYPE html><html><head><title></title><style></style></head><body>'

    print 'Search :"'+title+'"'

    movies = db.search(title)

    if DEBUG:
        print movies

    if len(movies) == 0:
        return 'Sorry. No movies found. Please change your search.'

    print 'Total returned:',len(movies)

    for item in movies:

        line = '<div><a href="/search/'+item['title']+'">'+item['title']+' ('+str(item['year'])+')</a></div>'
        result += line
        if DEBUG:
            print line

    result += '</body></html>'

    if DEBUG:
        print result

    return result


# Player_B gives up
@app.route('/give_up')
def give_up():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)
    user_name = session['user_name']
    game_id = session['game_id']
    session['player'] =''
    session['game_id'] =''
    if DEBUG:
        print "User %s is giving up for game_id: %i" % (user_name,game_id)
    db.remove_player_b(game_id)

    return redirect("#/status", code=302)


# Join Game
@app.route('/join_game/<game_id>')
def join_game(game_id):
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)
    user_name = session['user_name']
    game_id = int(game_id)

    db.join_game(user_name,game_id)
    if DEBUG:
        print 'Joining game_id %i from Status Page' % game_id
    session['player'] = 'B'
    session['game_id'] = game_id

    return redirect('/resolve/', code=302)





######################################################################################################################
#                                                  Challenge App                                                     #
######################################################################################################################

@app.route('/challenge/')
def challenge():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)
    user_name = session['user_name']

    return render_template('challenge.html', user_name = user_name )


@app.route('/challenge/search_movie')
def search_movie_challenge():

    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)
    #user_name = session['user_name']

    return render_template('search_movie_challenge.html')


@app.route('/challenge/movie_selected/')
def movie_selected_challenge():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)
    #user_name = session['user_name']
    #game_id = session['game_id']
    #movieID = int(movieID)
    #if DEBUG:
    #    print "Updating game_id %i with movieID %i" % (game_id, movieID)
    #db.update_movieID(movieID,game_id)

    #movieID = db.get_movieID_by_game_id(session['game_id'])
    #if movieID:
    #    title, year = db.get_movie_title_by_movieID(movieID)

    return render_template('movie_selected_challenge.html')


# Recover Keywords from the Challenge
@app.route('/challenge/keywords', methods=['GET', 'POST'])
def challenge_keywords():
    # Method POST
    if request.method == 'POST':

        result = []

        if request.form.has_key('keyword1') and request.form['keyword1'] != '':
            keyword1 = request.form['keyword1']
            result.append(str(keyword1))
            if DEBUG:
                print "Keyword1:",keyword1
        if request.form.has_key('keyword2') and request.form['keyword2'] != '':
            keyword2 = request.form['keyword2']
            result.append(str(keyword2))
            if DEBUG:
                print "Keyword2:",keyword2
        if request.form.has_key('keyword3') and request.form['keyword3'] != '':
            keyword3 = request.form['keyword3']
            result.append(str(keyword3))
            if DEBUG:
                print "Keyword3:",keyword3
        if request.form.has_key('keyword4') and request.form['keyword4'] != '':
            keyword4 = request.form['keyword4']
            result.append(str(keyword4))
            if DEBUG:
                print "Keyword4:",keyword4
        if request.form.has_key('keyword5') and request.form['keyword5'] != '':
            keyword5 = request.form['keyword5']
            result.append(str(keyword5))
            if DEBUG:
                print "Keyword5:",keyword5
        if request.form.has_key('keyword6') and request.form['keyword6'] != '':
            keyword6 = request.form['keyword6']
            result.append(str(keyword6))
            if DEBUG:
                print "Keyword6:",keyword6

        if DEBUG:
            print "Keywords from challenge:",result


        db.update_keywords_a(result,session['game_id'])

        return redirect("#/status", code=302)

    # Method GET
    else:
        return "Method not allowed"



######################################################################################################################
#                                                 Resolve App                                                        #
######################################################################################################################

@app.route('/resolve/')
def resolve():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)
    user_name = session['user_name']

    player_a = db.get_player_a_by_game_id(session['game_id'])

    return render_template('resolve.html', user_name = user_name, player_a = player_a )


@app.route('/resolve/movie_selected/')
def movie_selected_resolve():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)
    user_name = session['user_name']

    player_a = db.get_player_a_by_game_id(session['game_id'])
    keywords = db.get_keywords_player_a_by_game_id( session['game_id'] )

    return render_template('movie_selected_resolve.html',user_name = user_name, player_a = player_a, words = len(keywords) )


# Recover Keywords to Resolve from POST
@app.route('/resolve/movie_selected/keywords/', methods=['GET', 'POST'])
def resolve_keywords():
    # Method POST
    if request.method == 'POST':

        result = []

        if request.form.has_key('keyword1') and request.form['keyword1'] != '':
            keyword1 = request.form['keyword1']
            result.append(str(keyword1))
            if DEBUG:
                print "Keyword1:",keyword1
        if request.form.has_key('keyword2') and request.form['keyword2'] != '':
            keyword2 = request.form['keyword2']
            result.append(str(keyword2))
            if DEBUG:
                print "Keyword2:",keyword2
        if request.form.has_key('keyword3') and request.form['keyword3'] != '':
            keyword3 = request.form['keyword3']
            result.append(str(keyword3))
            if DEBUG:
                print "Keyword3:",keyword3
        if request.form.has_key('keyword4') and request.form['keyword4'] != '':
            keyword4 = request.form['keyword4']
            result.append(str(keyword4))
            if DEBUG:
                print "Keyword4:",keyword4
        if request.form.has_key('keyword5') and request.form['keyword5'] != '':
            keyword5 = request.form['keyword5']
            result.append(str(keyword5))
            if DEBUG:
                print "Keyword5:",keyword5
        if request.form.has_key('keyword6') and request.form['keyword6'] != '':
            keyword6 = request.form['keyword6']
            result.append(str(keyword6))
            if DEBUG:
                print "Keyword6:",keyword6

        if DEBUG:
            print "Keywords from resolve",result

        db.update_keywords_b(result,session['game_id'])

        return redirect("/resolve/#/resolve/movie_selected/keywords/check/", code=302)

    # Method GET
    else:
        return "Method not allowed"


# Compare keywords from player_a and player_b
@app.route('/resolve/movie_selected/keywords/check/')
def resolve_keywords_check():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)
    user_name = session['user_name']
    game_id = session['game_id']

    response = '<br>'
    response += '<h3> Keywords Check for "{{ title }}" ({{ year }})</h3>'

    player_a = db.get_keywords_player_a_by_game_id(game_id)
    player_b = db.get_keywords_player_b_by_game_id(game_id)

    # if len(player_b) == 1:
    #     response += '<div><h4>You selected this single keyword:</h4><ul>'
    #     response += '<li class="thumbnail">"'+str(player_b[0])+'"</li>'
    #     response += '</ul></div>'
    # else:
    #     response += '<div><h4>You selected these '+str(len(player_b))+' keywords:</h4><ul>'
    #     for item in player_b:
    #         response += '<li class="thumbnail">"'+item +'"</li>'
    #     response += '</ul></div>'

    matches = []
    response += '<br><div><h4>Matches:</h4>'
    for item_b in player_b:
        match = ''
        for item_a in player_a:
            if item_b == item_a:
                match = item_a
        if match:
            response += '<li class="bg-success">"'+match+'"</li>'
            matches.append(match)
        else:
            response += '<li class="bg-danger">"'+item_b+'"</li>'

    response += '</ul></div>'

    response += '<h4>Total: '+str(len(matches))+'</h4>'

    if len(player_a) == len(matches):
        # Game solved
        response += '<h2>Congratulations '+user_name+'! You solved game: '+str(game_id)+'</h2>'
        db.update_game_solved(game_id)
    else:
        # Not solved
        response += '<br><a href="/resolve/#/resolve/movie_selected/">Try again!</a>'
        response += '<br><a href="/give_up">Give Up</a>'

    response += '<br><a href="/#/status">Status Page</a>'

    return response




######################################################################################################################
#                                                         API                                                        #
######################################################################################################################

# Search movies by free text
@app.route('/api/v0/search/<query>/movie')
def imdb_api_search(query):

    result = {}

    print 'Search :"'+query+'"'

    movies = db.search(query,kind='movie')

    if DEBUG:
        print movies

    print 'Total returned:',len(movies)

    if len(movies) == 0:
        result = "{ 'error': { 'status': 400, 'message': 'not a valid search' } }"
        result = json.dumps( result, sort_keys=True, indent=4, separators=(',', ': ') )
    else:
        result = json.dumps( movies, sort_keys=True, indent=4, separators=(',', ': ') )
        #result = json.dumps( movies )

    if DEBUG:
        print result

    response = make_response( result )
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


# API call (Secure) to update the movieID is GAMES extracting it from the URL and the game_id from he session
@app.route('/api/v0/secure/update/movieID/<movieID>')
def imdb_api_update_movieID(movieID):
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)
    #user_name = session['user_name']
    game_id = int(session['game_id'])
    movieID = int(movieID)
    if DEBUG:
       print "Updating game_id %i with movieID %i" % (game_id, movieID)
    db.update_movieID(movieID,game_id)

    #result = "{ 'success': { 'status': 100, 'message': 'movieID updated' } }"
    result = '{ "success":  100 }'
    response = make_response( result )
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# API call (Secure) to get the movieID for a game using game_id from SESSION
@app.route('/api/v0/secure/get/game_id/')
def imdb_api_get_game_id_from_session():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)

    result = {}

    game_id = session['game_id']
    if DEBUG:
        print "Getting movieID from game_id:",game_id,"using session[game_id]"
    movieID = db.get_movieID_by_game_id(game_id)

    if DEBUG:
       print "movieID obtained", movieID

    result['movieID'] = movieID

    result = json.dumps( result, sort_keys=True, indent=4, separators=(',', ': ') )
    if DEBUG:
        print result

    response = make_response( result )
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# API call (Secure) to get the movieID for a game using game_id FROM URL
@app.route('/api/v0/secure/get/game_id/<game_id>')
def imdb_api_get_game_id_from_URL(game_id):
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login", code=302)

    result = {}

    if DEBUG:
        print "Getting movieID from game_id:",game_id,"using URLparam."
    movieID = db.get_movieID_by_game_id(game_id)


    if DEBUG:
       print "movieID obtained", movieID

    result['movieID'] = movieID

    result = json.dumps( result, sort_keys=True, indent=4, separators=(',', ': ') )
    if DEBUG:
        print result

    response = make_response( result )
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response



# Get movie title and year by movieID
@app.route('/api/v0/get/title/<movieID>')
def imdb_api_get_title(movieID):

    result = {}
    movieID = int(movieID)
    title, year = db.get_movie_title_by_movieID(movieID)

    result['movieID'] = movieID
    result['title'] = title
    result['year'] = year

    result = json.dumps( result, sort_keys=True, indent=4, separators=(',', ': ') )
    if DEBUG:
        print result

    response = make_response( result )
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response




if __name__ == '__main__':
    app.run(debug=False,
            host="0.0.0.0",
            port=5000,
            threaded=True,
            #processes=10
            )
