#tt0012532
from pymongo import MongoClient
from pprint import pprint

URI = "mongodb+srv://FlaskApp:Moviebuff@cluster0.w16mq.mongodb.net/test"

client = MongoClient(URI)

#db = client.moviebuff.title
#collection = db.title

# Sample TitleID
# {"Imdb_Title_id": "tt0012532"}
#tt0012532
src = client.moviebuff.streaming
title = client.moviebuff.title
dst = client.moviebuff.sample

# res = title.aggregate([
#     {
#         '$match': {
#             'Imdb_Title_id': 'tt0012532'
#         }
#     }, {
#         '$lookup': {
#             'from': 'streaming', 
#             'localField': 'Imdb_Title_id', 
#             'foreignField': 'Imdb_Title_id', 
#             'as': 'streaming'
#         }
#     }, {
#         '$unwind': {
#             'path': '$streaming'
#         }
#     },
        # {"$out": "sample"}
# ])

res = dst.update_one({},{ "$set": { "streaming": {"$query": "$streaming.Streaming"} } })
#res = dst.find_one({})



pprint(res)
