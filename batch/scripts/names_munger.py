import pandas as pd


NAMES = "/Users/jon/Desktop/names.tsv"
TRIMMED1 = "/Users/jon/Desktop/trimmed1.csv"
TRIMMED2 = "/Users/jon/Desktop/trimmed2.csv"
UNIQUE_NAMES = "/Users/jon/Desktop/uniquenameid.txt"

names = pd.read_csv(NAMES, sep="\t", low_memory=False)
names.drop(labels =  ["knownForTitles"], axis=1, inplace=True)
# trimmed1 = pd.read_csv(TRIMMED1, low_memory=False)
# trimmed2 = pd.read_csv(TRIMMED2, low_memory=False)
# nconst = pd.concat([trimmed1, trimmed2], axis=0)
# print(nconst.info())
# unique_name_ids = pd.unique(nconst['nconst'])
# print('unique names: ', len(unique_name_ids))
# with open(UNIQUE_NAMES, 'w') as f:
#     for _id in unique_name_ids:
#         f.write(str(_id) + '\n')
ids = pd.read_csv(UNIQUE_NAMES, names=['nconst'], sep="\n", low_memory=False)

# print(ids.info())
# print(ids.head())
# print(names.info())
# print(names.head())

joined = pd.merge(
    ids,
    names,
    how="inner",
    on= "nconst",
    sort=False,
    validate= "one_to_one"  
)

joined.drop(labels = "nconst", axis=1, inplace=True)
joined.rename(columns={"primaryProfession": "category", "primaryName": "Name"}, inplace=True)
joined = joined.astype( {"birthYear": "string", "deathYear": "string", "category": "string", "Name": "string"}, errors="ignore")

# print(nconst.info())
# print(nconst.head())
# print(names.info())
# print(names.head())

print(joined.info())
print(joined.head())

TRIMMEDNAMES = "/Users/jon/Desktop/trimmednames.csv"
joined.to_csv(path_or_buf=TRIMMEDNAMES, index=False)