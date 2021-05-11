import pandas as pd
import pprint
import json

STREAM = "/Users/jon/Desktop/CS411 Project Data/movies_metadata.csv"


summary = pd.read_csv(STREAM, low_memory=False)

#print(summary.info())


print(summary['overview'][0])



