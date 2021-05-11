from pymongo import MongoClient
from pprint import pprint

""" Mongo_templates: Query templates for various filtering and ordering operations"""
"""
SAMPLE_FORM = {'yearStart': '1900',
 'yearEnd': '2021',
  'languages': [['English'], ['Spanish'], ['German'], ['Italian'], ['French'], ['Russian'], ['Danish'], ['Swedish'], ['Japanese'], ['Hindi'], ['Mandarin'], ['Arabic'], ['Korean'], ['Hebrew'], ['Cantonese'], ['Portugese'], ['Latin'], ['Ukrainian'], ['Other']],
   'imdbStart': '0',
    'imdbEnd': '10',
     'sorting': 'avg_vote',
   'genres': [['Action'], ['Adventure'], ['Animation'], ['Biography'], ['Comedy'], ['Crime'], ['Drama'], ['Fantasy'], ['History'], ['Horror'], ['Musical'], ['Mystery'], ['Romance'], ['Sci-Fi'], ['Thriller'], ['War'], ['Western']]}




def clean_filters(form: dict) -> dict:
    '''Process filter fields'''
    if form['languages']:
        form['languages'] = [item for sublist in form['languages'] for item in sublist] #flatten list
    if form['genres']:
        form['genres'] = [item for sublist in form['genres'] for item in sublist] #flatten list
    if form['streaming']:
        form['streaming'] = [item for sublist in form['languages'] for item in sublist] #flatten list

    if len(form['languages']) == 19 or len(form['languages']) == 0:
        form.pop('languages')
    if not form["streaming"]:
        form.pop('streaming')
    if len(form['genres']) == 17 or len(form['genres']) == 0:
        form.pop('genres')
    if form['yearStart']=='1900' and form['yearEnd']=='2021':
        form.pop('yearStart')
        form.pop('yearEnd')
    if (form['imdbStart']=='0' and form['imdbEnd']=='10'):
        form.pop('imdbStart')
        form.pop('imdbEnd')

    return form


def filter_query(form: dict) -> dict:
  
    form = clean_filters(form)
    query = {}

    filters = ["language", "genre"] #, "streaming"]
    for f in filters:
        if f in form:
            q = lang_genre_stream(form)
            query.update(q)
            break
  
    if "yearStart" in form:
        q = year_range(form)
        query.update(q)
    
    if "imdbStart" in form:
        q = rating_range(form)
        query.update(q)

    ob = order_by(form)
    return {"$query": query, ob}


def order_by(form: dict) -> dict:
    query = {}
    ordering = form['sorting']
    if ordering == "rating":
        q = {"$orderby": { "avg_vote" : -1 }}
        query.update(q)
    elif ordering == "title":
        q = {"$orderby": { "title" : 1 }}
        query.update(q)
    else:   
        q = {"$orderby": { "year" : -1 }}
        query.update(q)
    return query


def lang_genre_stream(form: dict) -> dict:
    query = {}
    if "language" in form:
        languages = form["language"]
        q = { "language": { "$in": languages}}
        query.update(q)
    if "genre" in form:
        genres = form["language"]
        q = { "language": { "$in": genres }}
        query.update(q)
    #if "streaming" in form:
    #    services = form["streaming"]
    #    q = { "streaming": { "$in": services }}
    #    query.update(q)
    return query


def year_range(form: dict) -> dict:
    start = form['yearStart']
    end = form['yearEnd']
    return { "year" : { "$gte" :  start, "$lte" : end}}


def rating_range(form: dict) -> dict:
    start = form['imdbStart']
    end = form['imdbEnd']
    return { "avg_vote" : { "$gte" :  start, "$lte" : end}}

"""



URI = "mongodb+srv://FlaskApp:Moviebuff@cluster0.w16mq.mongodb.net/test"

client = MongoClient(URI)
#db = client.moviebuff.title
#collection = db.title

#collection = client.moviebuff.title

#print(collection.find_one({"title": "Miss Jerry"}))
#print(collection.find_one({'imdb_title_id': 'tt0000009'}))
# res = []
# for doc in collection.find({ "$query": {}, "$orderby": { "avg_vote" : -1 }}).limit(10):
#    res.append(doc)

# for doc in res:
#     pprint(doc)
#     print('\n')

# def filter_query(self, form: dict) -> cursor:
#     """Home Page Big Filter Query:
#             Returns cursor obj that requires iteration to unpack.
#             Suggest iterate into list for pagination of results"""
#     if not self.client:
#         self.connect()
#     query = filter_query(form)
#     return self.db.find(query).limit(25)


#READ_PATH = "/Users/jon/Desktop/titles.txt"
#WRITE_PATH = "/Users/jon/Desktop/titles1.txt"

# with open(WRITE_PATH, "w") as f:
#     res = collection.find({}, {"Imdb_Title_id":1, "_id":0})
#     for id in res:
#         f.write(id["Imdb_Title_id"] + "\n")

# distinct = set()
# with open(READ_PATH, "r") as f:
#     for line in f.readlines():
#         distinct.add(line)

# with open(WRITE_PATH, "w") as f:
#     for item in distinct:
#         f.write(item + "\n")

sample = client.moviebuff.sample
sample.aggregate([
    {
        '$lookup': {
            'from': 'streaming', 
            'localField': 'Imdb_Title_id', 
            'foreignField': 'Imdb_Title_id', 
            'as': 'streaming'
        }
    }, {
        '$unwind': {
            'path': '$streaming'
        }
    }, {
        '$set': {
            'streaming': '$streaming.Streaming'
        }
    }, {
        '$out': 'title'
    }
], maxTimeMS=999999999)