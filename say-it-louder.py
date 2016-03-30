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



@app.route('/login', methods=['GET', 'POST'])
def login():
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

            if 'player' in session:
                # Player A detected
                if session['player'] == 'A':
                    if DEBUG:
                        print 'GET /login Player A detected. Redirecting to /challenge/'
                    return redirect('/#/challege/', code=302)
                # Player B detected
                elif session['player'] == 'B':
                    if DEBUG:
                        print 'GET /loging Player B detected. Redirecting to /resolve/'
                    return redirect('/#/resolve/', code=302)

            # user_name present but not player present
            else:
                print "ERROR: User present in the system but not carrying session[player]"
                session.pop('user_name', None)
                return redirect('/#/login', code=302)


        # No session detected and no POST? Render login.html again
        else:
            return render_template('login.html')



@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_name', None)
    return redirect('/', code=302)




@app.route('/status.html')
def status_html():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
    user_name = session['user_name']

    response =  '<h2>Status Page</h2>'
    response += '<h3>Hello '+user_name+'!</h3>'
    response += 'This is the current status:'

    game = ''

    games_raw = db.get_games()

    for item in games_raw:
        game += '<h5>GameID:'+str(item[0])+' Time_Stamp:'+item[1]+' Player_A:'+item[2]
        if item[3:4]:
            game += ' Player_B:'+item[3]
        if item[4:5]:
            game += ' MovieID:'+str(item[4])
        if item[5:6]:
            game += ' Keywords_A:'+str(item[5])
        if item[6:7]:
            game += ' Keywords_B:'+str(item[6])
        if item[7:8]:
            game += ' Solved:'+str(item[7])

        game += '</h5>'

    response += game

    #return render_template('status.html', user_name = user_name, games = games )
    return response




@app.route('/challenge/')
def challenge():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
    user_name = session['user_name']

    return render_template('challenge.html', user_name = user_name )


@app.route('/challenge/search_movie')
def search_movie_challenge():

    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
    #user_name = session['user_name']

    return render_template('search_movie_challenge.html')


@app.route('/challenge/movie_selected/')
def movie_selected_challenge():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
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
            print "Keywords",result

        db.update_keywords_a(result,session['game_id'])

        return redirect("/#/status")

    # Method GET
    else:
        return "Method not allowed"










@app.route('/search_movie')
def search_movie():

    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
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


# API call (Secure) to update the movieID is games extracting it from the URL and the game_id from he session
@app.route('/api/v0/secure/update/movieID/<movieID>')
def imdb_api_update_movieID(movieID):
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
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






@app.route('/welcome')
def welcome():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
    user_name = session['user_name']

    return render_template('welcome.html', user_name = user_name )



@app.route('/welcome/movie/')
def welcome_movie():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
    user_name = session['user_name']

    return render_template('search_movie.html', user_name = user_name )


@app.route('/game')
def game_html():
    if not 'user_name' in session:
        # print "not logged in",session
        #session['stored']= "test"+session['user_name']+"test"
        print "not logged in",session
        return redirect("/login")
        # return 'You are not logged in'

    session['stored']= "test"+session['user_name']+"test"
    print "logged in", session
    return 'Logged in as %s' % escape(session['user_name'])



if __name__ == '__main__':
    app.run(debug=False,
            host="0.0.0.0",
            port=5000,
            threaded=True,
            #processes=10
            )
