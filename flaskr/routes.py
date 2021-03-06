from flask import Flask, request, redirect, render_template, g, url_for
import wtforms_jsonschema2
from json2html import *
from flaskr.forms import Title
from flaskr.db import MoviebuffDB
from flaskr import app

db = MoviebuffDB()


@app.route('/')
def home():
    return render_template('base.html')


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
                          template="form-template")
