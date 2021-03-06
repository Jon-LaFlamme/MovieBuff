import pymysql
from flaskr import sqls as sqls


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


    def query_omnibus(self, field_args: dict):
        '''Idea: take in a single dictionary of query & filter params,
           & perform the correct sql query
        '''
        if not self.driver:
            self.connect()

        return dict
        
