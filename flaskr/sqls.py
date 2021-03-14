title_name = "SELECT * FROM imdblist WHERE title = %s"

title_year_name = 'SELECT imdb_title_id, year, genre from imdblist WHERE Title=%s AND year IN (%s..%s)'

delete_by_id = 'DELETE FROM imbdblist WHERE id=%s'


def insert_record(form: dict) -> tuple:

    sqls = 'INSERT INTO imdblist ('
    attributes = []
    values = []
    ref_tag = []

    for k,v in form.items():
        if v:
            attributes.append(k)
            values.append(v)
            ref_tag.append('%s')

    sqls += ','.join(attributes) + ') VALUES ('
    sqls += ','.join(ref_tag) + ')'

    return (sqls,tuple(values))


def update_record(form: dict) -> tuple:

    sqls = 'UPDATE imdblist SET'
    title_id = form.pop('title_id')
    values = []
    for k,v in form.items():
        if v:
            sqls += ' %s = %s'
            values.append(k)
            values.append(v)

    sqls += ' WHERE title_id = %s'
    values.append(title_id)

    return (sqls,tuple(values))


def purge_redundant_filters(form: dict) -> dict:
    '''Optimizes query performance by removing filters that select all'''
    if(len(form['languages']) == 19):
        form['languages'] = None
    else:
        form['languages'] = [item for sublist in form['languages'] for item in sublist] #flatten list
    if(len(form['genres']) == 17):
        form['genres'] = None
    else:
        form['genres'] = [item for sublist in form['genres'] for item in sublist] #flatten list
    #if(len(form['streaming_services']) == 4):
        # form['streaming_services'] = None
    if(form['yearStart']=='1900' and form['yearEnd']=='2021'):
        form['yearStart'] = None
        form['yearEnd'] = None
    if (form['imdbStart']=='0' and form['imdbEnd']=='10'):
        form['imdbStart'] = None
        form['imdbEnd'] = None
    #if(form['rottenStart']==0 and form['rottenEnd']==10):
    #    form['rottenStart'] = None
    #    form['rottenEnd'] = None   

    return form


def query_enhanced(form: dict) -> tuple:

    form = purge_redundant_filters(form)
    languages = form['languages']
    #services = form['streaming_services']
    genres = form['genres']
    year_start = form['yearStart']
    year_end = form['yearEnd']
    imdb_start = form['imdbStart']
    imdb_end = form['imdbEnd']
    #rotten_start = form['rottenStart']
    #rotten_end = form['rottenEnd']
    sort_by = form['sorting']

    #sqls = 'SELECT imdblist, <stream_service_table> WHERE '
    sqls = 'SELECT title, year, genre, language, avg_vote FROM imdblist WHERE'
    add_and = False
    values = []

    if languages:
        escapes = ','.join(['%s' for x in languages])
        sqls += ' language IN (' + escapes + ')'      
        values.extend(list(languages))
        add_and = True

    #if services:
    #    if add_and:
    #        sqls += ' AND'
    #    escapes = ','.join(['%s' for x in services])
    #    sqls += ' services IN (' + escapes + ')'      
    #    values.extend(services)
    #    add_and = True

    if genres:
        if add_and:
            sqls += ' AND'
        escapes = ','.join(['%s' for x in genres])
        sqls += ' genre IN (' + escapes + ')'   
        values.extend(list(genres))
        add_and = True

    if year_start and year_end:
        if add_and:
            sqls += ' AND'
        sqls += ' year BETWEEN %s AND %s'
        values.extend([year_start, year_end])
        add_and = True

    if imdb_start and imdb_end:
        if add_and:
            sqls += ' AND'
        sqls += ' avg_vote BETWEEN %s AND %s'
        values.extend([imdb_start, imdb_end])
        add_and = True

    #if rt_start and rt_end:
        #if add_and:
         #   sqls += ' AND'
      #  sqls += ' rt_rating BETWEEN %d AND %d'
       # values.extend([rt_start, rt_end])
       #add_and = True
    
    if add_and == False:
        sqls = 'SELECT title, year, genre, language, avg_vote FROM imdblist'

    if sort_by:
        if sort_by == 'title':
            sqls += ' ORDER BY %s'
        else:
            sqls += ' ORDER BY %s DESC'
        values.append(sort_by)

    return (sqls, tuple(values))


filter_search_rating = "select imdb_title_id, title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s order by avg_vote desc"

filter_search_date = "select imdb_title_id, title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s order by year desc"

filter_search_title = "select imdb_title_id,title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s order by title"

filter_search_rating_language = "select imdb_title_id,title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} order by avg_vote desc"

filter_search_date_language = "select imdb_title_id,title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} order by year desc"

filter_search_title_language = "select imdb_title_id,title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} order by title"

filter_search_rating_genre = "select imdb_title_id,title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and genre in {} order by avg_vote desc"

filter_search_date_genre = "select imdb_title_id,title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and genre in {} order by year desc"

filter_search_title_genre = "select imdb_title_id,title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and genre in {} order by title"

filter_search_rating_language_genre = "select imdb_title_id,title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} and genre in {} order by avg_vote desc"

filter_search_date_language_genre = "select imdb_title_id,title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} and genre in {} order by year desc"

filter_search_title_language_genre = "select imdb_title_id,title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} and genre in {} order by title"

imdb_id = "SELECT * FROM imdblist WHERE imdb_title_id = %s"

add_user = "INSERT INTO user (UserName, EmailAddress, Password) values (%s, %s, %s)"

login = "SELECT COUNT(*) FROM user WHERE UserName = %s AND Password = %s"

name = "SELECT imdb_title_id, category FROM imdbprincipals WHERE imdb_name = %s"

realName = "SELECT name FROM imdbnames WHERE imdb_name = %s"

nameData = "SELECT imdb_name, category FROM imdbprincipals WHERE imdb_title_id = %s order by category"

movieById = "SELECT title, year from imdblist where imdb_title_id = %s"




