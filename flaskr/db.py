import pymysql
from flaskr import sqls as sqls
import hashlib, uuid
import sys

class MoviebuffDB():
    def __init__(self):
        self.app = None
        self.driver = None
    
    def init_app(self, app):
        self.app = app
        self.connect()

    def connect(self):
        self.driver = pymysql.connect(user='moviebuff@moviebuff',\
                                password='CS411ssjb',\
                                host='moviebuff.mysql.database.azure.com',\
                                ssl_disabled=True,\
                                database='moviebuff',\
                                charset='utf8mb4',\
                                autocommit=True,\
                                cursorclass=pymysql.cursors.DictCursor)
        #return self.driver


    def get_db(self):
        if not self.driver:
            return self.connect()
        return self.driver()

    def query_basic(self, query: str):
        '''Quick Search: Target for Demo on Mar 14'''
        if not self.driver:
            self.connect()
        sql = sqls.title_name
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchone()           
        return res

    def query_id(self, query: str):
        '''Quick Search: Target for Demo on Mar 14'''
        if not self.driver:
            self.connect()
        sql = sqls.imdb_id
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchone()
        return res

    def filter_query(self, query: str):
        if not self.driver:
            self.connect()
        sql = sqls.filter_search_rating
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        return res

    def filter_query_date(self, query: str):
        if not self.driver:
            self.connect()
        sql = sqls.filter_search_date
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        return res

    def filter_query_title(self, query: str):
        if not self.driver:
            self.connect()
        sql = sqls.filter_search_title
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        return res

    def filter_query_language(self, query: str, language):
        if not self.driver:
            self.connect()
        if(len(language) == 1):
            language.append("asdfasdf")
        sql = sqls.filter_search_rating_language.format(tuple(language))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        return res

    def filter_query_date_language(self, query: str, language):
        if not self.driver:
            self.connect()
        if(len(language) == 1):
            language.append("asdfasdf")
        sql = sqls.filter_search_date_language.format(tuple(language))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        return res

    def filter_query_title_language(self, query: str, language):
        if not self.driver:
            self.connect()
        if(len(language) == 1):
            language.append("asdfasdf")
        sql = sqls.filter_search_title_language.format(tuple(language))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        return res

    def filter_query_genre(self, query: str, genres):
        if not self.driver:
            self.connect()
        if(len(genres) == 1):
            genres.append("asdfasdf")
        sql = sqls.filter_search_rating_genre.format(tuple(genres))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        return res

    def filter_query_date_genre(self, query: str, genres):
        if not self.driver:
            self.connect()
        if(len(genres) == 1):
            genres.append("asdfasdf")
        sql = sqls.filter_search_date_genre.format(tuple(genres))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        return res

    def filter_query_title_genre(self, query: str, genres):
        if not self.driver:
            self.connect()
        if(len(genres) == 1):
            genres.append("asdfasdf")
        sql = sqls.filter_search_title_genre.format(tuple(genres))
        res = {"Query result": 0}
        with self.driver.cursor() as c:
            c.execute(sql, query)
            res = c.fetchall()
        return res

    def filter_query_language_genre(self, query: str, languages, genres):
        if not self.driver:
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
        return res

    def filter_query_date_language_genre(self, query: str, languages, genres):
        if not self.driver:
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
        return res

    def filter_query_title_language_genre(self, query: str, languages, genres):
        if not self.driver:
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
        return res

    def login(self, userInfo):
        if not self.driver:
            self.connect()
        sql = sqls.login
        with self.driver.cursor() as c:
            c.execute(sql, (userInfo[0], hashlib.md5(userInfo[1].encode()).hexdigest()))
            res = c.fetchone()
            if(res['COUNT(*)'] >= 1):
                return True
            else:
                return False

    def addUser(self, userInfo):
        if not self.driver:
            self.connect()
        sql = sqls.add_user
        with self.driver.cursor() as c:
            try:
                c.execute(sql, (userInfo[0], userInfo[1], hashlib.md5(userInfo[2].encode()).hexdigest()))
                self.driver.commit()
            except:
                return False
        return True

    def query_omnibus(self, field_args: dict):
        '''Idea: take in a single dictionary of query & filter params,
           & perform the correct sql query
        '''
        if not self.driver:
            self.connect()
        return dict
        
