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



@app.route('/challenge/')
def challenge():
    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
    user_name = session['user_name']


    return render_template('challenge.html', user_name = user_name )







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



@app.route('/you-open-game')
def you_open_game():

    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
    user_name = session['user_name']

    open_game = db.check_open_game(user_name )
    if open_game:
        pass
    else:
        pass

    return render_template('index.html', user_name = user_name)






@app.route('/search_movie')
def search_movie():

    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
    #user_name = session['user_name']

    return render_template('search_movie.html')


@app.route('/challenge/search_movie')
def search_movie_challenge():

    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
    #user_name = session['user_name']

    return render_template('search_movie_challenge.html')



@app.route('/challenge/movie_selected')
def movie_selected_challenge():

    if not 'user_name' in session:
        if DEBUG:
            print "Not logged in. Redirecting to /login"
        return redirect("/login")
    #user_name = session['user_name']

    return render_template('movie_selected_challenge.html')








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


#@app.route('/api/search?q=<title>&kind=movie')
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




if __name__ == '__main__':
    app.run(debug=False,
            host="0.0.0.0",
            port=5000,
            threaded=True,
            #processes=10
            )
