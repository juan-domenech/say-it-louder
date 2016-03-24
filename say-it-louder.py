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

@app.route("/")
def index():

    return redirect("/static/html/index.html", code=302)

# @app.route("/index.html")
# def index_html():
#     return redirect("/static/html/index.html", code=302)

#@app.route("/partials/search.html")
#def search_html():
#    return redirect("/static/html/search.html", code=302)


@app.route('/login', methods=['GET', 'POST'])
def login_html():
    if request.method == 'POST':
        session['user_name'] = request.form['user_name']
        return redirect('/game', code=302)
    return render_template("login.html")


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_name', None)
    return redirect("/login", code=302)


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
    app.run(debug=True,
            host="0.0.0.0",
            port=5000,
            threaded=True,
            #processes=10
            )
