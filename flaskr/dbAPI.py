from flask import Flask
from flaskr import __init__ as app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Declaring a model. https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#models
class TitleBasics(db.Model):
    titleID = db.Column(db.String(80), primary_key=True, unique=True)
    titleType = db.Column(db.String(80))
    primaryTitle = db.Column(db.String(80))
    originalTitle = db.Column(db.String(80))
    isAdult = db.Column(db.Boolean)
    startYear = db.Column(db.Integer)
    endYear = db.Column(db.Integer)
    runtimeMinutes = db.Column(db.Integer)
    genres = db.Column(db.PickleType)

class Plots(db.Model):
    titleID = db.Column(db.String(80), primary_key=True, unique=True)
    plotSummary = db.Column(db.Text)
    duration = db.Column(db.String(80))
    genre = db.Column(db.String(80))
    rating = db.Column(db.Float)
    releaseDate = db.Column(db.String(80))
    plotSynopsis = db.Column(db.Text)

#TODO Declare the remaining tables in our schema




