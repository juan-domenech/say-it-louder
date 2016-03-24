from flask import Flask,make_response,render_template,redirect

from mysql import MySQLDatabase

import json

db = MySQLDatabase('imdb','imdb','imdb','localhost')

DEBUG = 1

app = Flask(__name__)
app._static_folder = '/Users/juan/say-it-louder/static/'

@app.route("/")
def index_empty():
    return redirect("/static/html/index.html", code=302)

@app.route("/index.html")
def index_html():
    return redirect("/static/html/index.html", code=302)

#@app.route("/partials/search.html")
#def search_html():
#    return redirect("/static/html/search.html", code=302)



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
@app.route('/api/search/<query>/movie')
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
