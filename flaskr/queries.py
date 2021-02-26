'''
queries.py provides an API for performing SQL queries
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskr.models import TitleBasics


def title_name(s: str):
    #TODO Error handling
    records = TitleBasics.query.filter_by(primaryTitle=s)
    id_ = records.titleID
    title = records.primaryTitle
    year = records.startYear
    runtime = records.runtimeMinutes
    genres = records.genres
    if records:
        return f'title: {title}, released: {year}, runtime: {runtime}, genres: {genres}'
    else:
        return 'No record(s) found by that title'

def title_id(s: str):
    #TODO Complete function
    records = None
    if records:
        return records
    else:
        return 'No record(s) found by that ID'