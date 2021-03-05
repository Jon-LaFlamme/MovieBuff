'''
queries.py provides an API for performing SQL queries
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskr.models import TitleBasics


def title_name_query(s: str):
    return f'title: {title}, released: {year}, runtime: {runtime}, genres: {genres}'


def title_id(s: str):
    #TODO Complete function
    records = None
    if records:
        return records
    else:
        return 'No record(s) found by that ID'