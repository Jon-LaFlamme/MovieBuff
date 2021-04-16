from pymongo import MongoClient
from flaskr import sqls as sqls
from flaskr import mongo_templates as templates



class MongoDB():
    def __init__(self):
        self.app = None
        self.client = None
        self.db = None
   
    def init_app(self, app):
        self.app = app
        if not self.client:
            self.connect()

    def connect(self):
        URI = "mongodb+srv://FlaskApp:Moviebuff@cluster0.w16mq.mongodb.net/test"
        self.client = MongoClient(URI)
        self.db = self.client.moviebuff.title

    def close_connection(self):
        self.client.close()
        self.client = None

    def query_by_id(self, s: str) -> dict:
        """Simple title Fetch by IMDB"""
        if not self.client:
            self.connect()
        return self.db.find_one({'imdb_title_id': s})

    def filter_query(self, form: dict): #-> cursor object
        """Home Page Big Filter Query:
                Returns cursor obj that requires iteration to unpack.
                Suggest iterate into list for pagination of results"""
        if not self.client:
            self.connect()
        query = templates.filter_query(form)
        print("this is the full query")
        print(query)
        return self.db.find(query).limit(25)


#sample sql for reference:
#select imdb_title_id, title, year, genre, language, avg_vote, Netflix, Hulu, Prime, Disney 
# from imdblist, streaming where imdblist.title = streaming.STitle and year >= %s 
# and year <= %s and avg_vote >= %s and avg_vote <= %s and (Netflix = 1) order by avg_vote desc

