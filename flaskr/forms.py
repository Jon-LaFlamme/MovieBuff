"""Form object declaration."""
#Adapted from https://hackersandslackers.com/flask-wtforms-forms/
#Docs: https://wtforms.readthedocs.io/en/2.3.x/

from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Optional



class Title(FlaskForm):
    """Search by Title"""
    title = StringField(
        'Title',
        [DataRequired()]
    )
    submit = SubmitField('Submit')


class TitleYear(FlaskForm):
    """Search by Title and Range of Years"""
    title = StringField(
        'Title',
        [DataRequired()]
    )
    min_year = IntegerField(
        'Release Year >=',
        [Optional()]
    )
    max_year = IntegerField(
        'Release Year <=',
        [Optional()]
    )
    submit = SubmitField('Submit')


class Omnibus(FlaskForm):
    """Search by Many Parameters"""
    #TODO
    submit = SubmitField('Submit')