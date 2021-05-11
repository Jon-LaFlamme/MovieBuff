from pymongo import MongoClient
from pprint import pprint
import pandas as pd

URI = "mongodb+srv://FlaskApp:Moviebuff@cluster0.w16mq.mongodb.net/test"
client = MongoClient(URI)
#db = client.moviebuff.title
#collection = db.title
collection = client.moviebuff.title


#READ_PATH = "/Users/jon/Desktop/titles.txt"
#WRITE_PATH = "/Users/jon/Desktop/moviebufflists.txt"

""" Completed pull from MongoDB """
# with open(WRITE_PATH, "w") as f:
#     f.write("Imdb_Title_id;language;genre;Streaming\n")
#     res = collection.find({}, {"Imdb_Title_id":1, "_id":0, "language":1, "genre":1, "Streaming":1})
#     for _id in res:
#         #pprint(_id)
#         f.write(_id["Imdb_Title_id"]\
#              + ";" + _id["language"]\
#              + ";" + _id["genre"]\
#              + ";" + _id["Streaming"]\
#              + "\n")

# nestedlanglist = [['English'], ['Spanish'], ['German'], ['Italian'], ['French'], ['Russian'], ['Danish'], ['Swedish'], ['Japanese'], ['Hindi'], ['Mandarin'], ['Arabic'], ['Korean'], ['Hebrew'], ['Cantonese'], ['Portugese'], ['Latin'], ['Ukrainian'], ['Other']]
# nestedgenrelist =  [['Action'], ['Adventure'], ['Animation'], ['Biography'], ['Comedy'], ['Crime'], ['Drama'], ['Fantasy'], ['History'], ['Horror'], ['Musical'], ['Mystery'], ['Romance'], ['Sci-Fi'], ['Thriller'], ['War'], ['Western']]
# nestedstreamlist = [['Netflix'], ['Prime'], ['Hulu'], ['Disney']]  #Note: be sure to plug into api correctly

# flatlang = sorted([item for sublist in nestedlanglist for item in sublist])
# flatgenre = sorted([item for sublist in nestedgenrelist for item in sublist])
# flatstream = sorted([item for sublist in nestedstreamlist for item in sublist])

# LANGS = {}
# GENRES = {}
# STREAMS = {}

# for i, lang in enumerate(flatlang):
#     value = int(bin(1<<i),2)
#     LANGS.update({lang: value})
# for i, genre in enumerate(flatgenre):
#     value = int(bin(1<<i),2)
#     GENRES.update({genre: value})
# for i, serv in enumerate(flatstream):
#     value = int(bin(1<<i),2)
#     STREAMS.update({serv: value})

# print(LANGS)
# print(GENRES)
# print(STREAMS)

# READ_PATH = "/Users/jon/Desktop/moviebufflists.txt"
# titles = pd.read_csv(READ_PATH, sep=";", low_memory=False)

# titles = pd.concat(
#     [
#         titles,
#         pd.DataFrame(
#             index = titles.index, 
#             columns=['bin_language', 'bin_genre', 'bin_stream']
#         )
#     ], axis=1
# )
# #titles = titles.astype( {"birthYear": "string", "deathYear": "string", "category": "string", "Name": "string"}, errors="ignore")

# print(titles.head())
# print("\n")

# def bin_mapper_lang(x):
#     if isinstance(x, str):
#         x = x.split(",")
#     else:
#         x = ["Other"]
#     x = [elem.strip() for elem in x]
#     ct = 0
#     for elem in x:
#         if elem in LANGS:
#             ct = ct | LANGS[elem]        
#     return ct

# def bin_mapper_gen(x):
#     if isinstance(x, str):
#         x = x.split(",")
#     else:
#         x = ["Other"]
#     x = [elem.strip() for elem in x]
#     ct = 0
#     for elem in x:
#         if elem in GENRES:
#             ct = ct | GENRES[elem]         
#     return ct

# def bin_mapper_stream(x):
#     if isinstance(x, str):
#         x = x.split(",")
#     else:
#         x = []
#     x = [elem.strip() for elem in x]
#     ct = 0
#     for elem in x:
#         if elem in STREAMS:
#             ct = ct | STREAMS[elem]          
#     return ct

# titles['bin_language'] = titles['language'].apply(bin_mapper_lang)
# titles['bin_genre'] = titles['genre'].apply(bin_mapper_gen)
# titles['bin_stream'] = titles['Streaming'].apply(bin_mapper_stream)

# print(titles.head())
# print("\n")

# titles.drop(labels =["Streaming", "genre", "language"], axis=1, inplace=True)

# print(titles.head())

# WRITE_PATH = "/Users/jon/Desktop/binmap.txt"
# titles.to_csv(path_or_buf=WRITE_PATH, index=False)

""" FAIL: have to reupload a doc with all filters """
# WRITE_PATH = "/Users/jon/Desktop/extrafilters.txt"

# with open(WRITE_PATH, "w") as f:
#     f.write("Imdb_Title_id;year;avg_vote;title\n")
#     res = collection.find({}, {"Imdb_Title_id":1, "_id":0, "year":1, "avg_vote":1, "title":1})
#     for _id in res:
#         #pprint(_id)
#         f.write(_id["Imdb_Title_id"]\
#              + ";" + _id["year"]\
#              + ";" + _id["avg_vote"]\
#              + ";" + _id["title"]\
#              + "\n")


READ_PATH = "/Users/jon/Desktop/extrafilters.txt"
titles = pd.read_csv(READ_PATH, sep=";", low_memory=False, error_bad_lines = False)

READ_PATH = "/Users/jon/Desktop/binmap.txt"
binmap = pd.read_csv(READ_PATH, sep=",", low_memory=False, error_bad_lines = False)

joined = pd.merge(
    titles,
    binmap,
    how="inner",
    on= "Imdb_Title_id",
    sort=False,
    validate= "one_to_one"  
)

print(titles.head())
print(binmap.head())
print(joined.head())

WRITE_PATH = "/Users/jon/Desktop/bitmapsplus.txt"
joined.to_csv(path_or_buf=WRITE_PATH, index=False)