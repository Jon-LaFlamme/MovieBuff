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

    def query_by_id(self, title: str) -> dict:
        """Simple title Fetch by IMDB"""
        if not self.client:
            self.connect()
        return self.db.find_one({'Imdb_Title_id': title})

    def query_person_titles(self, name: str): #-> cursor object
        """Fetches Titles a person was in"""
        if not self.client:
            self.connect()
        query = templates.query_titles_by_person(name)
        return self.db.find(query).limit(30)

    def query_by_person(self, name: str) -> dict:
        """Returns roles and titles for cast/crew member"""
        if not self.client:
            self.connect()
        return self.client.moviebuff.castcrew.find_one({'Name': name})

    def filter_query(self, form: dict): #-> cursor object
        """Home Page multiple filter and order query"""
        if not self.client:
            self.connect()
        query = templates.filter_query(form)
        print("This is the full filter query: ", query)
        return self.db.find(query).limit(25)

    def query_by_title_name(self, title: str): # -> cursor object:
        """Simple title Fetch by title_name"""
        if not self.client:
            self.connect()
        return self.db.find({'title': title}).limit(15)

    def full_text_search_name(self, term: str):
        """For autocomplete functionality.. fuzzy search on Name"""
        if not self.client:
            self.connect()
        query = templates.full_text_search_name(term)
        return self.client.moviebuff.castcrew.aggregate(query)

    def full_text_search_title(self, term: str):
        """For autocomplete functionality.. fuzzy search on Title"""
        if not self.client:
            self.connect()
        query = templates.full_text_search_title(term)
        return self.client.moviebuff.engtitles.aggregate(query)

    def full_text_search_description(self, term: str):
        """For autocomplete functionality.. fuzzy search on Description"""
        if not self.client:
            self.connect()
        query = templates.full_text_search_description(term)
        return self.client.moviebuff.engdescriptions.aggregate(query)

    def full_text_search_all(self, term: str):
        """For autocomplete functionality.. fuzzy search on All=[name,title,description]"""
        if not self.client:
            self.connect()
        query = templates.full_text_search_all(term)
        return self.client.moviebuff.castcrew.aggregate(query)
    
 
