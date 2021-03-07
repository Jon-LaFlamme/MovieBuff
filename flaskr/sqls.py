

title_name = "SELECT * FROM imdblist WHERE title = %s"

title_year_name = 'SELECT imdb_title_id, year, genre from imdblist WHERE Title=%s AND year IN (%s..%s)'

<<<<<<< HEAD


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
=======
filter_search_rating = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s order by avg_vote desc"

filter_search_date = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s order by year desc"

filter_search_title = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s order by title"

filter_search_rating_language = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} order by avg_vote desc"

filter_search_date_language = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} order by year desc"

filter_search_title_language = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} order by title"

filter_search_rating_genre = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and genre in {} order by avg_vote desc"

filter_search_date_genre = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and genre in {} order by year desc"

filter_search_title_genre = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and genre in {} order by title"

filter_search_rating_language_genre = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} and genre in {} order by avg_vote desc"

filter_search_date_language_genre = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} and genre in {} order by year desc"

filter_search_title_language_genre = "select title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s and language in {} and genre in {} order by title"
>>>>>>> 204482bd31707a79b964abb1c37e79fe7d30fef5
