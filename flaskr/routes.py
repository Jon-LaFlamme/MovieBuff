from flask import Flask, request, redirect, render_template, g, url_for
import wtforms_jsonschema2
from json2html import *
from flaskr.forms import Title
from flaskr.db import MoviebuffDB
from flaskr import app
import json

db = MoviebuffDB()

LoggedIn = False

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('base.html', loggedIn = LoggedIn)
    else:
        query = request.form.get('Title')
        res = db.query_basic(query)
        return json2html.convert(json = res)

@app.route('/Login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', failedLogin = False)
    if request.method == 'POST':
        if db.login([request.form.get('User'),request.form.get('Password')]):
            LoggedIn = True
            return render_template('base.html', loggedIn = LoggedIn)
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
    LoggedIn = False
    return render_template('base.html', loggedIn=LoggedIn)

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
        return json2html.convert(json=res)
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
        return json2html.convert(json=res)
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
        return json2html.convert(json=res)


@app.route('/search', methods=['GET','POST'])
def search():
    form = Title()
    if form.validate_on_submit():
        #TODO(Jon) Problem: WTF can be used for form validation, but cannot unpack
        #into primitive data types.
        query = form.data['title']
        res = db.query_basic('Speed')
        return json2html.convert(json = res)
        
    return render_template("basic-title-search.jinja2", form=form,\
                          template="form-template", loggedIn = LoggedIn)

@app.route('/<moviename>')
def movie(moviename):
    dbRes = db.query_id(str(moviename))
    if(dbRes):
        remove = []
        for i in dbRes.keys():
            if dbRes[i] == '':
                remove.append(i)
        for i in remove:
            del dbRes[i]
    return render_template('movie.html', res = json2html.convert(json=dbRes), loggedIn = LoggedIn)

# @app.route('/people/<personname>')
# def movie(personname):
#     dbRes = db.query_id(str(personname))
#     print(dbRes, file=sys.stderr)
#     if(dbRes):
#         remove = []
#         for i in dbRes.keys():
#             if dbRes[i] == '':
#                 remove.append(i)
#         for i in remove:
#             del dbRes[i]
#     return render_template('movie.html', title = "hello", res = json2html.convert(json=dbRes))

