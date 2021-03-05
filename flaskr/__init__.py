'''
__init__.py runs the flask app
Execution is asynchronous
Functions handle REST requests
Decorators for each Function define the url endpoint and the accepted REST methods 
#pymysql docs: https://pymysql.readthedocs.io/en/latest/user/examples.html
'''

import os
from flask import Flask, request, redirect, render_template, g
from flaskext.mysql import MySQL
from flaskr.models import db, TitleBasics
from flaskr.queries import title_name, title_id
from flaskr.forms import Title, TitleYear
from json2html import *



#Initialize the Flask app and database
app = Flask(__name__)

connection = pymysql.connect(user='moviebuff@moviebuff',\
                            password='CS411ssjb',\
                            host='moviebuff.mysql.database.azure.com',\
                            database='moviebuff',\
                            charset='utf8mb4',\
                            autocommit=True,\
                            cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/search', methods=['GET','POST'])
def search():
    form = Title()
    if form.validate_on_submit():
        return redirect(url_for("results"))
    return render_template("basic-title-search.jinja2", form=form,\
                          template="form-template")


@app.route('/results', methods=['POST']) 
def results():
    if request.method == 'POST':
        title = form.title
        sql = title_name(title)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
            return json2html.convert(json = res)
    else:
        return redirect(url_for("home"))