""" Mongo_templates: Query templates for various filtering and ordering operations"""


def clean_filters(form: dict) -> dict:
    '''Process filter fields'''
    if form['languages']:
        form['languages'] = [item for sublist in form['languages'] for item in sublist] #flatten list
    if form['genres']:
        form['genres'] = [item for sublist in form['genres'] for item in sublist] #flatten list
    if 'streaming' in form:
        form['streaming'] = [item for sublist in form['streaming'] for item in sublist] #flatten list
        if len(form["streaming"]) < 1:
            form.pop("streaming")
        else:
            if "Disney" in form["streaming"]:
                form["streaming"].append("Disney+")
    if len(form['languages']) == 19 or len(form['languages']) == 0:
        form.pop('languages')
    if len(form['genres']) == 17 or len(form['genres']) == 0:
        form.pop('genres')
    if form['yearStart']=='1900' and form['yearEnd']=='2021':
        form.pop('yearStart')
        form.pop('yearEnd')
    if 'imdbStart' in form and 'imdbEnd' in form:
        if (form['imdbStart']=='0' and form['imdbEnd']=='10'):
            form.pop('imdbStart')
            form.pop('imdbEnd')

    return form


def filter_query(form: dict) -> dict:
    """Clean filters and select correct query string"""
    form = clean_filters(form)
    query = {}
    filters = ["languages", "genres" , "streaming"]
    for f in filters:
        if f in form.keys():
            q = lang_genre_stream(form)
            query.update(q)
            break
  
    if "yearStart" in form:
        q = year_range(form)
        query.update(q)   
    if "imdbStart" in form:
        q = rating_range(form)
        query.update(q)
    order = order_by(form)["$orderby"]
    return {"$query": query, "$orderby": order}


def order_by(form: dict) -> dict:
    query = {}
    ordering = form['sorting']
    if ordering == "avg_vote":
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
    print("lang_genre_stream")
    query = {}
    if "languages" in form.keys():
        languages = form["languages"]
        q = { "language": { "$in": languages}}
        query.update(q)
    if "genres" in form.keys():
        genres = form["genres"]
        q = { "genre": { "$in": genres }}
        query.update(q)
    if "streaming" in form.keys():
       services = form["streaming"]
       q = { "Streaming": { "$in": services }}
       query.update(q)
    return query


def year_range(form: dict) -> dict:
    start = form['yearStart']
    end = form['yearEnd']
    return { "year" : { "$gte" :  start, "$lte" : end}}


def rating_range(form: dict) -> dict:
    start = form['imdbStart']
    end = form['imdbEnd']
    if end == "10":
        end = "9.99"
    return { "avg_vote" : { "$gte" :  start, "$lte" : end}}

def query_titles_by_person(name: str) -> dict:
    return {"Principals.name.name": name}

def query_titles_by_person_many(names: list) -> dict:
    return {"Principals.name.name": { "$in": names}}

def full_text_search_name(searchterm):   
    return [{"$search": {
                "index": "default", # optional, defaults to "default"
                "autocomplete": {
                    "query": searchterm,
                    "path": "Name",
                    "tokenOrder": "sequential",
                    #"fuzzy": <options>,
                    #"score": <options>
                    }
                }
            },
            {"$limit": 15 },
            {"$project": {  
                "_id": 0,
                "Name": 1,
                "category": 1
                }
            }]

def full_text_search_title(searchterm):   
    return [{"$search": {
                "index": "default", # optional, defaults to "default"
                "autocomplete": {
                    "query": searchterm,
                    "path": "title",
                    "tokenOrder": "sequential",
                    #"fuzzy": <options>,
                    #"score": <options>
                    }
                }
            },
            {"$limit": 15 },
            {"$project": {  
                "_id": 0,
                "title": 1
                }
            }]

def full_text_search_description(searchterm):   
    return [{"$search": {
                "index": "default", # optional, defaults to "default"
                "autocomplete": {
                    "query": searchterm,
                    "path": "title",
                    "tokenOrder": "sequential",
                    #"fuzzy": <options>,
                    #"score": <options>
                    }
                }
            },
            {"$limit": 15 },
            {"$project": {  
                "_id": 0,
                "title": 1,     # mislabeled, this is actually description field
                "Imdb_Title_id": 1
                }
            }]

