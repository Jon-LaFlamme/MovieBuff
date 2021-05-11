import pandas as pd



TITLEID = "/Users/jon/Desktop/titles1.txt"
PRINCIPALS = "/Users/jon/Desktop/principals.tsv"



principals = pd.read_csv(PRINCIPALS, sep="\t", low_memory=False)
titles = pd.read_csv(TITLEID, sep="\n", names=['Imdb_Title_id'], low_memory=False)
principals.rename(columns={"tconst": "Imdb_Title_id"}, inplace=True)
principals.drop(labels =  ["ordering","category","job", "characters"], axis=1, inplace=True)
principals = principals.astype( {"Imdb_Title_id": "string", "nconst": "string"}, errors="ignore")
titles = titles.astype( {"Imdb_Title_id": "string"}, errors="ignore")

print(principals.head())
print(principals.info())
print(titles.head())
print(titles.info())

joined = pd.merge(
    principals,
    titles,
    how="inner",
    on= "Imdb_Title_id",
    sort=False,
    validate= "many_to_one"  
)

print(joined.head())
print(joined.info())

JOINED1 = "/Users/jon/Desktop/trimmed1.csv"
JOINED2 = "/Users/jon/Desktop/trimmed2.csv"
#JOINED3 = "/Users/jon/Desktop/trimmed3.csv"

joined1 = joined.loc[:16811,:]
joined2 = joined.loc[16812:,:]

#BAD INDEX = 16811

#joined3 = joined.loc[20000:,:]
joined1.to_csv(path_or_buf=JOINED1, index=False)
joined2.to_csv(path_or_buf=JOINED2, index=False)
#joined3.to_csv(path_or_buf=JOINED3, index=False)

