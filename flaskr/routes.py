from flask import Flask, request, redirect, render_template, g, url_for, session
import wtforms_jsonschema2
from json2html import *
from flaskr.forms import Title
from flaskr.db import MoviebuffDB
from flaskr.cosmos import MoviebuffCosmos
#from flaskr import validate as validate
from flaskr import app
import json
from flaskr import sqls as sqls

db = MoviebuffDB()
cosmos_db = MoviebuffCosmos()

@app.route('/', methods=['GET','POST'])  #Basic Title Search/Home Page
def home():
    if request.method == 'GET':
        return render_template('base.html')
    else:
        query = request.form.get('Title')
        if validate.valid_title(query):
            res = db.query_basic(query)
            return json2html.convert(json=res)
        else:
            return "ERROR: Invalid query. Please try again without quotes or escape characters"

@app.route('/Login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', failedLogin = False)
    if request.method == 'POST':
        if db.login([request.form.get('User'),request.form.get('Password')]):
            session['login'] = True
            return render_template('base.html')
        else:
            return render_template('login.html', failedLogin = True)

@app.route('/SignUp', methods=['GET','POST'])
def newUser():
    if request.method == 'POST':
        if db.addUser([request.form.get('User'), request.form.get('Email'), request.form.get('Password')]):
            return render_template('signup.html', success=0)
        else:
            return render_template('signup.html', success=-1)
    else:
        return render_template('signup.html', success=1)

@app.route('/Logout')
def logout():
    session['login'] = False
    return render_template('base.html')

@app.route('/process', methods=['GET','POST'])
def process():
    query = []
    res = ""
    query.append(int(request.json['yearStart']))
    query.append(int(request.json['yearEnd']))
    query.append(int(request.json['imdbStart']))
    query.append(int(request.json['imdbEnd']))

    Languages = [item for sublist in request.json['languages'] for item in sublist]
    Genres = [item for sublist in request.json['genres'] for item in sublist]
    addLanguages = False
    addGenres = False

    if(len(request.json['languages']) < 19):
        addLanguages = True
    if(len(request.json['genres']) < 17):
        addGenres = True

    if(request.json['sorting'] == 'avg_vote'):
        if(addLanguages and addGenres):
            res = db.filter_query_language_genre(query, Languages,
                                                 Genres)
        elif(addLanguages):
            res = db.filter_query_language(query, Languages)
        elif(addGenres):
            res = db.filter_query_genre(query, Genres)
        else:
            res = db.filter_query(query)
        return render_template('results.html', results = res)
    elif(request.json['sorting'] == 'year'):
        if(addLanguages and addGenres):
            res = db.filter_query_date_language_genre(query, Languages,
                                                      Genres)
        elif(addLanguages):
            res = db.filter_query_date_language(query, Languages)
        elif(addGenres):
            res = db.filter_query_date_genre(query, Genres)
        else:
            res = db.filter_query_date(query)
        return render_template('results.html', results = res)
    else:
        if(addLanguages and addGenres):
            res = db.filter_query_title_language_genre(query, Languages,
                                                       Genres)
        elif(addLanguages):
            res = db.filter_query_title_language(query, Languages)
        elif(addGenres):
            res = db.filter_query_title_genre(query, Genres)
        else:
            res = db.filter_query_title(query)
        return render_template('results.html', results = res)


@app.route('/search', methods=['GET','POST'])   #Test Route for noSQL API
def search():
    if request.method == 'GET':
        return render_template('base-test-nosql.html')
    else:
        #sql,values = sqls.query_enhanced(request.json)  #Uncomment this,next line to test SQL String and Values  
        #return json2html.convert(json = {sql:values})
        res = cosmos_db.query_enhanced(request.json)  
        print(res, file=sys.stderr)
        # print(titleRes, file=sys.stderr)
        return render_template('results.html', results = res) 
    res = {"error": "Test query not working"}   
    return render_template('results.html', results = res)


@app.route('/<moviename>')
def movie(moviename):
    titleId = str(moviename)
    dbRes = db.query_id(titleId)
    imgurl = "https://moviebuffposters.blob.core.windows.net/images/" + titleId + ".jpg"
    if(dbRes):
        remove = []
        for i in dbRes.keys():
            if dbRes[i] == '':
                remove.append(i)
        for i in remove:
            del dbRes[i]
        nmRes = db.query_nm(str(moviename))
        names = dict()
        for i in nmRes:
            names[i['imdb_title_id']] = db.query_rName(str(i['imdb_title_id']))[0]['name']
    return render_template('movie.html', res = json2html.convert(json=dbRes), nmRes = nmRes, names = names, 
                    imgurl = imgurl, title = dbRes['title'], titleId = titleId)

@app.route('/<moviename>/reviews')
def reviews(moviename):
    titleId = str(moviename)
    imgurl = "https://moviebuffposters.blob.core.windows.net/images/" + titleId + ".jpg"
    
    return render_template('reviews.html', imgurl = imgurl, title = db.query_movieName(titleId)['title'], titleId = titleId)

@app.route('/_<personname>')
def person(personname):
    dbRes = db.query_nmData(str(personname))
    titleRes = dict()
    for i in dbRes:
        titleRes[i['imdb_name']] = db.query_movieName(i['imdb_name'])
    # print(dbRes, file=sys.stderr)
    # print(titleRes, file=sys.stderr)
    return render_template('person.html', dbRes = dbRes, titleRes = titleRes)

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'GET':
        return render_template('base.html') #TODO html file required for update procedure
    else:
        res = db.update_record(request.form)
        return json2html.convert(json = res)


@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('base.html')  #TODO html file required insert procedure
    else:
        res = db.create_record(request.form)
        return json2html.convert(json = res)


@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'GET':
        return render_template('base.html') #TODO html file required for delete procedure
    else:
        res = db.delete_record(request.form)
        return json2html.convert(json = res)
