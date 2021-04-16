""" Mongo_templates: Query templates for various filtering and ordering operations"""


def clean_filters(form: dict) -> dict:
    '''Process filter fields'''
    if form['languages']:
        form['languages'] = [item for sublist in form['languages'] for item in sublist] #flatten list
    if form['genres']:
        form['genres'] = [item for sublist in form['genres'] for item in sublist] #flatten list
    # if form['streaming']:
    #     form['streaming'] = [item for sublist in form['languages'] for item in sublist] #flatten list

    if len(form['languages']) == 19 or len(form['languages']) == 0:
        form.pop('languages')
    # if not form["streaming"]:
    #     form.pop('streaming')
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
    """Clean filters and select correct query string"""
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
    order = order_by(form)["$orderby"]
    print("this is output for order")
    print(order)
    print("this is the filter query")
    print(query)

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


