

title_name = "SELECT * FROM imdblist WHERE title = %s"

title_year_name = 'SELECT imdb_title_id, year, genre from imdblist WHERE Title=%s AND year IN (%s..%s)'



def query_enhanced(form: object) -> tuple:
    languages = form.get('languages')
    services = form.get('services')
    genres = form.get('genres')
    year = form.get('year')
    imdb_rating = form.get('imdb_rating')
    rt_rating = form.get('rt_rating')
    sort_by = form.get('sort_by')

    #sqls = 'SELECT imdblist, <stream_serve_table> WHERE '
    sqls = 'SELECT imdblist WHERE'
    values = []

    if languages:
        sqls += ' language = %s' + 'OR %s'.join(languages)
        values.extend(languages)

    #if services:
    #    sqls += ' AND <service_name> = %s' 'OR %s'.join(services)
    #    values.extend(services)

    if genres:
        sqls += ' genre = %s' + 'OR %s'.join(genres)
        values.extend(genres)

    if year:
        sqls += ' year BETWEEN %d AND %d'
        values.extend(year)

    if imdb_rating:
        sqls += ' rating BETWEEN %d AND %d'
        values.extend(imdb_rating)

    #if rt_rating:
      #  sqls += ' rt_rating BETWEEN %d AND %d'
       # values.extend(rt_rating)

    if sort_by:
        sqls += ' ORDER BY %s'
        values.extend(sort_by)

    return (sqls, tuple(values))
