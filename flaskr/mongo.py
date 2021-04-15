from pymongo import MongoClient


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
        """TODO: Simple ID Fetch """
        if not self.client:
            self.connect()
        return self.db.find_one({'imdb_title_id': s})

        
        
   