

title_name = "SELECT * FROM imdblist WHERE title = %s"

title_year_name = 'SELECT imdb_title_id, year, genre from imdblist WHERE Title=%s AND year IN (%s..%s)'

filter_search_rating = "select imdb_title_id, title, year, genre, language, avg_vote from imdblist where year >= %s and year <= %s and avg_vote >= %s and avg_vote <= %s order by avg_vote desc"

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

imdb_id = "SELECT * FROM imdblist WHERE imdb_title_id = %s"

add_user = "INSERT INTO user (UserName, EmailAddress, Password) values (%s, %s, %s)"

login = "SELECT COUNT(*) FROM user WHERE UserName = %s AND Password = %s"




