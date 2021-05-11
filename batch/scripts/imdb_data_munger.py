import pandas as pd

#TODO Notes to Sriram
    #1) Port numeric types to numeric from string
    #2) Names Collection Update with more complete IMDB set

#TODO   JOIN IMDB title basics table with streamingtable
TITLE = "/Users/jon/Desktop/titlebasics.tsv"
STREAM = "/Users/jon/Desktop/stream.csv"

title = pd.read_csv(TITLE, sep="\t", low_memory=False)
stream = pd.read_csv(STREAM, sep=',', engine='python')
title.drop(labels =  ["titleType","originalTitle","isAdult", "endYear", "runtimeMinutes", "genres"], axis=1, inplace=True)
stream.drop(labels = ["ID", "Genres", "Country", "Language", "Runtime", "IMDb", "Age", "Type", "Directors","Unnamed: 0", "Rotten Tomatoes"], axis=1, inplace=True)
title.rename(columns={"primaryTitle": "title", "startYear": "year", "tconst": "Imdb_Title_id"}, inplace=True)
stream.rename(columns={"Title": "title", "Year": "year"}, inplace=True)

stream = stream.astype({"title": "string", 'year': 'string', "Netflix": "boolean", "Hulu": "boolean","Prime Video": "boolean","Disney+": "boolean",}, errors="ignore")
title = title.astype( {"title": "string", "Imdb_Title_id": "string", "year": "string"} ,errors="ignore")


# print(title.dtypes)
# print(stream.dtypes)

# print(title.info())
# print(stream.info())

joined = pd.merge(
    title,
    stream,
    how="inner",
    on=['title',"year"],
    sort=False,
    validate= "many_to_one"  
)

# print(joined.info())
# print(joined.head())

JOINED = "/Users/jon/Desktop/joined.csv"

joined.to_csv(path_or_buf=JOINED, index=False)
