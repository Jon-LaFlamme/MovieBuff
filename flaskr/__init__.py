import os

from flask import Flask, request, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flaskr import dbAPI

#Initialize the Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'data.db'
db = SQLAlchemy()

#User class provides access to all SQLAlchemy functions and classes
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    pw_hash = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.username

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