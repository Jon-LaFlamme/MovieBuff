#https://polyglot.readthedocs.io/en/latest/Detection.html



#TODO For Titles Field: Run Polglot Detector over data and return only English.
#TODO Trim records down to "Title" & "Imdb_id"
#TODO Upload as new collection to MongoDB
#TODO Try again to index on Title Field

from pymongo import MongoClient
from polyglot.text import Text, Word
import pandas as pd
import json
from pprint import pprint


# URI = "mongodb+srv://FlaskApp:Moviebuff@cluster0.w16mq.mongodb.net/test"
# client = MongoClient(URI)
# title = client.moviebuff.title

# WRITE_PATH = "/Users/jon/Desktop/titlessubset.csv"

# with open(WRITE_PATH, "w") as f:
#     f.write("Imdb_Title_id, title\n")
#     res = title.find({}, {"Imdb_Title_id":1, "title":1, "_id":0})
#     for r in res:
#         f.write(r["Imdb_Title_id"] + "," + r["title"] + "\n")

TITLES = "/Users/jon/Desktop/CS411ProjectData/titlessubset.csv"

data = pd.read_csv(TITLES)

print(data.head())

#print(data.head())
#pprint(data[0])