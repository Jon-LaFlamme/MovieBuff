import pymysql
from flaskr import sqls as sqls

class MoviebuffDB():
    def __init__(self):
        self.app = None
        self.driver = None
    
    def init_app(self, app):
        self.app = app

    def close_connection(self):
        self.driver.close()
        self.driver = None

    def connect(self):
        self.driver = pymysql.connect(user='moviebuff@moviebuff',\
                                password='CS411ssjb',\
                                host='moviebuff.mysql.database.azure.com',\
                                ssl_disabled=True,\
                                database='moviebuff',\
                                charset='utf8mb4',\
                                autocommit=True,\
                                cursorclass=pymysql.cursors.DictCursor)

    def query_basic(self, query: str) -> dict:
        '''Quick Search: Target for Demo on Mar 14'''
        self.connect()
        sql = sqls.title_name
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchone()
        self.close_connection()
        return res

    def filter_query(self, query: str):
        self.connect()
        sql = sqls.filter_search_rating
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res

    def filter_query_date(self, query: str):
        self.connect()
        sql = sqls.filter_search_date
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res

    def filter_query_title(self, query: str):
        self.connect()
        sql = sqls.filter_search_title
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res

    def filter_query_language(self, query: str, language):
        self.connect()
        if(len(language) == 1):
            language.append("asdfasdf")
        sql = sqls.filter_search_rating_language.format(tuple(language))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res

    def filter_query_date_language(self, query: str, language):
        self.connect()
        if(len(language) == 1):
            language.append("asdfasdf")
        sql = sqls.filter_search_date_language.format(tuple(language))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res

    def filter_query_title_language(self, query: str, language):
        self.connect()
        if(len(language) == 1):
            language.append("asdfasdf")
        sql = sqls.filter_search_title_language.format(tuple(language))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res

    def filter_query_genre(self, query: str, genres):
        self.connect()
        if(len(genres) == 1):
            genres.append("asdfasdf")
        sql = sqls.filter_search_rating_genre.format(tuple(genres))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res

    def filter_query_date_genre(self, query: str, genres):
        self.connect()
        if(len(genres) == 1):
            genres.append("asdfasdf")
        sql = sqls.filter_search_date_genre.format(tuple(genres))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res

    def filter_query_title_genre(self, query: str, genres):
        self.connect()
        if(len(genres) == 1):
            genres.append("asdfasdf")
        sql = sqls.filter_search_title_genre.format(tuple(genres))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res

    def filter_query_language_genre(self, query: str, languages, genres):
        self.connect()
        if(len(genres) == 1):
            genres.append("asdfasdf")
        if(len(languages) == 1):
            languages.append("asdfasdf")
        sql = sqls.filter_search_rating_language_genre.format(tuple(languages), tuple(genres))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res

    def filter_query_date_language_genre(self, query: str, languages, genres):
        self.connect()
        if(len(genres) == 1):
            genres.append("asdfasdf")
        if(len(languages) == 1):
            languages.append("asdfasdf")
        sql = sqls.filter_search_date_language_genre.format(tuple(languages), tuple(genres))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res

    def filter_query_title_language_genre(self, query: str, languages, genres):
        self.connect()
        if(len(genres) == 1):
            genres.append("asdfasdf")
        if(len(languages) == 1):
            languages.append("asdfasdf")
        sql = sqls.filter_search_title_language_genre.format(tuple(languages), tuple(genres))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        self.close_connection()
        return res


    def query_enhanced(self, form: dict) -> dict:
        self.connect()
        res = {"Not yet implemented": 0}
        with self.driver.cursor() as c:
            sql,values = sqls.query_enhanced(form)
            c.execute(sql, values)
            res = c.fetchall()  
        self.close_connection()         
        return res


    def delete_record(self, s: str) -> dict:
        self.connect()
        k = -1
        with self.driver.cursor() as c:
            sql = sqls.delete_by_id(s)
            num = c.execute(sql, s) 
        self.close_connection()       
        return {"Number of records deleted from imdb": k}


    def create_record(self, s: str) -> dict:
        self.connect()
        k = -1
        with self.driver.cursor() as c:
            sql = sqls.insert_by_id(s)
            num = c.execute(sql, s) 
        self.close_connection()       
        return {"Number of records deleted from imdb": k}


    def update_record(self, s: str) -> dict:
        self.connect()
        k = -1
        with self.driver.cursor() as c:
            sql = sqls.delete_by_id(s)
            num = c.execute(sql, s) 
        self.close_connection()       
        return {"Number of records deleted from imdb": k}
