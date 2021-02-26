'''
__init__.py runs the flask app
Execution is asynchronous
Functions handle REST requests
Decorators for each Function define the url endpoint and the accepted REST methods 
'''

import os
from flask import Flask, request, redirect, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flaskr.models import db, TitleBasics
from flaskr.queries import title_name, title_id

#Initialize the Flask app and database
app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'data.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()


#Example CREATE record
'''
title = TitleBasics(titleID='ttexample000', titleType='Documentary',\
                        primaryTitle='Free Solo', originalTitle='Free Solo',\
                        isAdult=False, startYear=2018, endYear=2018,\
                        runtimeMinutes=100, genres=['Adventure','Documentary'])
db.session.add(title)
db.session.commit()
'''

#TODO sample home page placeholder
@app.route('/')
def home():
    return render_template('base.html')

#TODO Method performs basic query retrieval
@app.route('/form-1', methods=['GET','POST'])
def form_1():
    if request.method == 'GET':
        return render_template('form-1.html')
    else:
        return render_template('results.html')


#TODO Method processes query
#Do we want to pass an argument so all queries are processed/returned to the same page?
@app.route('/results', methods=['POST']) 
def results():
    if request.method == 'POST':
        query_string = request.form['primaryTitle']
        return title_name(query_string)
        #TODO(edit resutls to make the results more readable)
    else:
        return 'nothing'