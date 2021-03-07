from flask import Flask, request, redirect, render_template, g, url_for
import wtforms_jsonschema2
from json2html import *
from flaskr.forms import Title
from flaskr.db import MoviebuffDB
from flaskr import validate as validate
from flaskr import app

db = MoviebuffDB()


@app.route('/', methods=['GET','POST'])  #Basic Title Search/Home Page
def home():
    if request.method == 'GET':
        return render_template('base.html') 
    else:
        query = request.form.get('Title')
        if validate.valid_title(query):
            res = db.query_basic(query)
            return json2html.convert(json = res)
        else:
            return "ERROR: Invalid query. Please try again without quotes or escape characters"
        
@app.route('/process', methods=['GET','POST'])
def process():
    query = []
    res = ""
    query.append(int(request.json['yearStart']))
    query.append(int(request.json['yearEnd']))
    query.append(int(request.json['imdbStart']))
    query.append(int(request.json['imdbEnd']))

    print(request.json['languages'], file=sys.stderr)
    print(request.json['genres'], file=sys.stderr)

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
    if request.method == 'GET':
        return render_template('base.html') #TODO Change to html file with enhanced filter/search form
    else:
        #TODO Validate form @ validate.py
        res = db.query_enhanced(request.form)
        return json2html.convert(json = res)


@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'GET':
        return render_template('base.html') #TODO Change to html file with update form
    else:
        #TODO Validate form @ validate.py
        res = db.update_record(request.form)
        return json2html.convert(json = res)


@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('base.html')  #TODO Change to html file with create form
    else:
        #TODO Validate form @ validate.py
        res = db.create_record(request.form)
        return json2html.convert(json = res)


@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'GET':
        return render_template('base.html') #TODO Change to html file with delete form
    else:
        #TODO Validate form @ validate.py
        res = db.delete_record(request.form)
        return json2html.convert(json = res)