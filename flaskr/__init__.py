import os

from flask import Flask, request, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flaskr import dbAPI

#Initialize the Flask app and database
app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'data.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


#Example CREATE record
title = dbAPI.TitleBasics(titleID='ttexample000', titleType='Documentary',\
                        primaryTitle='Free Solo', originalTitle='Free Solo',\
                        isAdult=False, startYear=2018, endYear=2018,\
                        runtimeMinutes=100, genres=['Adventure','Documentary'])
db.session.add(title)
db.session.commit



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
        data = request.form
        return render_template('results.html')


#TODO Method processes query
@app.route('/process', methods=['POST']) 
def process():
    if request.method == 'POST':
        query_string = request.form['primaryTitle']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM TitleBasics(primaryTitle) Values (%)", query_string)
        #TODO find correct query and method for storing returned records
        mysql.connection.commit()
        cur.close()

        #TODO(perform query on TITLE_BASICS and return information)


        ''' TODO(edit resutls.html file to accept the following fields)
        return render_template('results.html', 
                                title_name=title_name, 
                                title_type=title_type,
                                title_start=title_start,
                                title_end=title_end,
                                title_runtime=title_runtime,
                                is_displayed=False,
                                title_genre=title_genre,
                                title_id=title_id)
        '''