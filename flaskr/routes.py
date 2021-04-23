from flask import Flask, request, redirect, render_template, g, url_for, session, jsonify
import wtforms_jsonschema2
from json2html import *
from flaskr.forms import Title
from flaskr.db import MoviebuffDB
from flaskr.cosmos import MoviebuffCosmos
from flaskr.mongo import MongoDB
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from flaskr import app
import json
from flaskr import sqls as sqls

db = MoviebuffDB()
cosmos_db = MoviebuffCosmos()
mongo_db = MongoDB()

convoList = []
ServicesList = ['Netflix', 'Prime', 'Hulu', 'Disney']
earliestYear = 1900
lowestRating = 0
languageList = ['English','Spanish','German','Italian','French','Russian','Danish','Swedish','Japanese','Hindi','Mandarin','Arabic','Korean','Portugese']
genreList = ['Action','Adventure','Animation','Biography','Comedy','Crime',
             'Drama','Fantasy','History','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']

FAILURE = [{'imdb_title_id':"",
        'title':"Sorry, No Titles Found",
        'year':"N/A",
        'genre':"N/A",
        'language':"N/A",
        'avg_vote':'N/A',
        'Netflix':"N/A",
        'Hulu':"N/A",
        'Prime':"N/A",
        'Disney':"N/A"}]


bot = ChatBot("Candice")

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

# Train based on english greetings corpus
trainer.train("chatterbot.corpus.english.greetings")

# Train based on the english conversations corpus
trainer.train("chatterbot.corpus.english.conversations")

listTrainer = ListTrainer(bot)


for i in ServicesList:
    listTrainer.train([
        i,
        "Ok, we'll search for movies on the " + i + " streaming service. Please enter one of the following languages to search for : " + ' '.join(languageList)
    ])

for i in languageList:
    listTrainer.train([
        i,
        "Ok, we'll search for movies in the " + i + " language. Please enter one of the following genres to search for : " + ' '.join(genreList)
    ])

for i in genreList:
    listTrainer.train([
        i,
        "Ok, we'll search for movies in the " + i + " genre. Searching..."
    ])

@app.route('/', methods=['GET','POST'])  #Basic Title Search/Home Page
def home():
    if request.method == 'GET':
        return render_template('base.html')
    else:
        query = request.form.get('Title')
        res = db.query_basic(query)
        return json2html.convert(json=res)

@app.route('/__Candice', methods=['GET','POST'])  #Basic Title Search/Home Page
def Candice():
    global convoList
    convoList = []
    if request.method == 'GET':
        return render_template('candice.html')

@app.route('/getChat')
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot.get_response(userText))
    global convoList

    if (userText in genreList or userText in languageList or userText in ServicesList):
        convoList.append(userText)

    returnVal = str(bot.get_response(userText))
    if returnVal.find("Searching...") == -1:
        return returnVal
    else:
        finalString = ''
        res = db.filter_chatbot(convoList[0])
        res = filterLanguage([convoList[1]], res)
        res = filterGenre([convoList[2]], res)
        for i in res[:-1]:
            finalString += i['title'] + ", "
        finalString += res[-1]['title']
        finalString += ". To begin again, re-enter the streaming service you would like to search, Netflix, Hulu, Prime, or Disney"
        convoList = []
        return finalString

@app.route('/Login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', failedLogin = False)
    if request.method == 'POST':
        if db.login([request.form.get('User'),request.form.get('Password')]):
            session['login'] = True
            session['userID'] = int(db.getUserID(request.form.get('User')))
            return render_template('base.html')
        else:
            return render_template('login.html', failedLogin = True)

@app.route('/SignUp', methods=['GET','POST'])
def newUser():
    if request.method == 'POST':
        if db.addUser([request.form.get('User'), request.form.get('Email'), request.form.get('Password')]):
            return render_template('signup.html', success=0)
        else:
            return render_template('signup.html', success=-1)
    else:
        return render_template('signup.html', success=1)

@app.route('/Logout')
def logout():
    session['login'] = False
    session['userID'] = 0
    return render_template('base.html')

def filterGenre(Genres, res):
    delList = []
    for i in res:
        add = True
        for j in Genres:
            if j in i['genre']:
                add = False
                break
        if (add):
            delList.append(i['imdb_title_id'])
    res[:] = [d for d in res if d['imdb_title_id'] not in delList]
    return res

def filterLanguage(Languages, res):
    delList = []
    for i in res:
        add = True
        for j in Languages:
            if j in i['language']:
                add = False
                break
        if (add):
            delList.append(i['imdb_title_id'])
    res[:] = [d for d in res if d['imdb_title_id'] not in delList]
    return res

@app.route('/process', methods=['GET','POST'])
def process():
    query = []
    res = ""
    query.append(int(request.json['yearStart']))
    query.append(int(request.json['yearEnd']))
    query.append(int(request.json['imdbStart']))
    query.append(int(request.json['imdbEnd']))

    Languages = []
    Genres = []
    Services = []
    if('languages' in request.json):
        Languages = [item for sublist in request.json['languages'] for item in sublist]
    if('genres' in request.json):
        Genres = [item for sublist in request.json['genres'] for item in sublist]
    if('streaming' in request.json):
        Services = [item for sublist in request.json['streaming'] for item in sublist]

    addLanguages = False
    addGenres = False
    addServices = False

    if(len(Languages) > 0 and len(Languages) < 19):
        addLanguages = True
    if(len(Genres) > 0 and len(Genres) < 17):
        addGenres = True
    if(len(Services)):
        addServices = True

    if(request.json['sorting'] == 'avg_vote'):
        if(addServices):
            res = db.filter_streaming(query, Services)
        else:
            res = db.filter_query(query)
        if(addGenres):
            res = filterGenre(Genres, res)
        if(addLanguages):
            res = filterLanguage(Languages, res)
        return render_template('results.html', results = res)
    elif(request.json['sorting'] == 'year'):
        if(addServices):
            res = db.filter_streaming_date(query, Services)
        else:
            res = db.filter_query_date(query)
        if(addGenres):
            res = filterGenre(Genres, res)
        if(addLanguages):
            res = filterLanguage(Languages, res)
        return render_template('results.html', results = res)
    else:
        if(addServices):
            res = db.filter_streaming_title(query, Services)
        else:
            res = db.filter_query_title(query)
        if(addGenres):
            res = filterGenre(Genres, res)
        if(addLanguages):
            res = filterLanguage(Languages, res)
        return render_template('results.html', results = res)


@app.route('/search', methods=['GET','POST'])   #MongoDB
def search():
    if request.method == 'GET':      
        if 'q' in request.args:
            term = request.args.get('q')
            category = request.args.get('c')
            res = ["No Matches Found"]
            print([term,category], file=sys.stderr)
            if category == "Cast/Crew Name":
                cursor = mongo_db.full_text_search_name(term)
                unique_res = set()
                for x in cursor:
                    unique_res.add(x['Name']) 
                res = list(unique_res)
            elif category == "Description":
                cursor = mongo_db.full_text_search_description(term)
                raw_res = []
                res = []
                if cursor:
                    for x in cursor:
                        raw_res.append((x["Imdb_Title_id"], x['title']))
                    for key, desc in raw_res:
                        t = mongo_db.query_by_id(key)
                        if t:
                            entry = t['title'] + ' : ' + desc + "\n"
                            res.append(entry)
            elif category == "Movie Title":
                cursor = mongo_db.full_text_search_title(term)
                unique_res = set()
                for x in cursor:
                    unique_res.add(x['title'])
                res = list(unique_res)
            else:   #category=="Search All"
                #TODO Create FTS for multi-index search
                pass
            #print(res, file=sys.stderr)
            return jsonify(matching_results=res)
        else:
            return render_template('base-test-nosql.html')
    else:
        print(request.json, file=sys.stderr)
        res = []
        if "searchTerm" in request.json:
            term = request.json['searchTerm']
            category = request.json['searchCategory']
            cursor = None
            if category == "Cast/Crew Name":
                cursor = mongo_db.query_person_titles(term)
            elif category == "Description":
                title = term.split(':')[0].strip()
                cursor = mongo_db.query_by_title_name(title)
            elif category == "Movie Title":
                cursor = mongo_db.query_by_title_name(term)
            else:   #category=="Search All"
                pass #TODO Setup multi-index text search       
            if cursor:
                res = [mov for mov in cursor]
            else:
                res = FAILURE
        else:
            cursor = mongo_db.filter_query(request.json)
            res = [mov for mov in cursor]
        if not res:
            res = FAILURE   
        return render_template('results-mongo.html', results = res)  


@app.route('/search/<moviename>')   #MongoDB
def search_title(moviename):
    imgurl = "https://moviebuffposters.blob.core.windows.net/images/" + moviename + ".jpg" 
    title = mongo_db.query_by_id(moviename)    
    title.pop("Imdb_Title_id")
    title.pop("_id")
    principals = title.pop("Principals")   
    cast_crew = []
    for role in principals:
        job = role["category"]
        names = role['name']
        for person in names:
            cast_crew.append((person["name"], job))
    return render_template('movie-nosql.html', res = json2html.convert(json=title), cast_crew = cast_crew, 
                        imgurl = imgurl, title = title['title'], titleId = moviename)

@app.route('/search/cast-crew/<name>')   #MongoDB
def search_person(name):
    person_details = mongo_db.query_by_person(name)
    print(person_details, file=sys.stderr)
    titles = mongo_db.query_person_titles(name)     #titles -> cursor object iterable
    person_all_roles = []
    person_title_role = {}
    for t in titles:       
        person_title_role = {"Imdb_Title_id": t["Imdb_Title_id"],
                            "title": t['title'],
                             "year": t['year']}
        principals = t["Principals"]
        for role in principals:
            names = role['name']
            print(names, file=sys.stderr)    
            for n in names:
                if n['name'] == name:
                    person_title_role.update({"category": role['category']})
                    print(person_title_role, file=sys.stderr)
                    person_all_roles.append(person_title_role)

    print(person_all_roles, file=sys.stderr)

    return render_template('person-mongo.html', title_details = person_all_roles, person = person_details)



@app.route('/<moviename>')
def movie(moviename):
    titleId = str(moviename)
    imgurl = "https://moviebuffposters.blob.core.windows.net/images/" + titleId + ".jpg"

    dbRes = db.query_id(titleId)  
    if(dbRes):
        remove = []
        for i in dbRes.keys():
            if dbRes[i] == '':
                remove.append(i)
        for i in remove:
            del dbRes[i]
        nmRes = db.query_nm(str(moviename))
        names = dict()
        for i in nmRes:
            names[i['imdb_title_id']] = db.query_rName(str(i['imdb_title_id']))[0]['name']
        return render_template('movie.html', res = json2html.convert(json=dbRes), nmRes = nmRes, names = names, 
                        imgurl = imgurl, title = dbRes['title'], titleId = titleId)
    else:
        if res:
            #Testing: This title image verified in Datastore: try Intolerance (tt00006864)
            dbRes = res
            remove_fields = ["_id", "reviews_from_critics", "reviews_from_users",
                             "original_title", "date_published"]
            swaps = ["writer", "director", "actors"]
            cast_crew = {}

            for field in remove_fields:
                if field in dbRes:
                    dbRes.pop(field)
            for field in swaps:
                cast_crew[field] = dbRes.pop(field)
            for k,v in dbRes.items():
                if not v:
                    dbRes[k] = "N/A"
            
            nmRes = db.query_nm(str(moviename))
            names = dict()
            for i in nmRes:
                names[i['imdb_title_id']] = db.query_rName(str(i['imdb_title_id']))[0]['name']

        else:
            dbRes = FAILURE
            dbRes['imdb_title_id'] = moviename
        return render_template('movie.html', res = json2html.convert(json=dbRes), nmRes = nmRes, names = names, 
                        imgurl = imgurl, title = dbRes['title'], titleId = titleId)


@app.route('/<moviename>/reviews')
def reviews(moviename):
    titleId = str(moviename)
    imgurl = "https://moviebuffposters.blob.core.windows.net/images/" + titleId + ".jpg"
    dbRes = db.query_id_reviews(titleId)
    reviewed = False
    avgScore = []
    for i in dbRes:
        if i['CreatedByUserID'] == session['userID']:
            reviewed = True
        avgScore.append(i['reviewscore'])
    avgScoreFinal = 0
    if(len(avgScore)):
        avgScoreFinal = round(sum(avgScore) / len(avgScore), 1)
    return render_template('reviews.html', imgurl = imgurl, title = db.query_movieName(titleId)['title'], titleId = titleId, dbRes = dbRes, reviewed = reviewed, avgScore = avgScoreFinal)


@app.route('/<moviename>/reviews/create', methods=['GET','POST'])
def reviews_create(moviename):
    titleId = str(moviename)
    if request.method == 'GET':
        return render_template('reviews_create.html', title = db.query_movieName(titleId)['title'], titleId = titleId)

    elif request.method == 'POST':
        UserID = session['userID']
        Score = request.form.get("Score")
        Review = request.form.get("Review")
        db.create_review(UserID, Score, titleId, Review)
        return redirect(url_for('reviews', moviename=titleId))

@app.route('/<moviename>/reviews/<reviewId>/update', methods=['GET','POST'])
def reviews_update(moviename, reviewId):
    titleId = str(moviename)
    if request.method == 'GET':
        return render_template('reviews_update.html', title = db.query_movieName(titleId)['title'], titleId = titleId, reviewId = reviewId)
    elif request.method == 'POST':
        UserID = session['userID']
        Score = request.form.get("Score")
        Review = request.form.get("Review")
        db.update_review(Score, UserID, reviewId, Review)
        return redirect(url_for('reviews', moviename=titleId))
    

@app.route('/<moviename>/reviews/<reviewId>/delete', methods=['GET','POST'])
def reviews_delete(moviename, reviewId):
    titleId = str(moviename)
    
    if request.method == 'GET':
        dbRes = db.query_review_by_reviewid(reviewId)
        
        return render_template('reviews_delete.html', title = db.query_movieName(titleId)['title'], titleId = titleId, dbRes = dbRes)
    elif request.method == 'POST':
        db.remove_reviewtext_by_reviewid(reviewId)
        db.remove_review_by_reviewid(reviewId)
    
    return redirect(url_for('reviews', moviename=titleId))


@app.route('/_<personname>')
def person(personname):
    dbRes = db.query_nmData(str(personname))
    titleRes = dict()
    for i in dbRes:
        titleRes[i['imdb_name']] = db.query_movieName(i['imdb_name'])
    # print(dbRes, file=sys.stderr)
    # print(titleRes, file=sys.stderr)
    return render_template('person.html', dbRes = dbRes, titleRes = titleRes)



@app.route('/title-fetch/<title_id>', methods=['GET','POST'])
def cosmos_lookup():
    if request.method == 'GET':
        res = cosmos_db.query_enhanced(title_id)
        return render_template('basic-title-search.html')
    else:
        res = cosmos_db.query_enhanced(request.form['_id'])[0]
        return render_template('results.html', results = [res])


