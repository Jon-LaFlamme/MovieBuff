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