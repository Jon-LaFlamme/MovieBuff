import pandas as pd

STREAM = "/Users/jon/Desktop/CS411 Project Data/Title-Stream-Union/joined.csv"

stream = pd.read_csv(STREAM, low_memory=False)
copy = stream
stream = stream.astype( {"Netflix": "string", "Hulu": "string", "Prime Video": "string", "Disney+": "string"}, errors="ignore")
stream["Netflix"] = stream["Netflix"].apply((lambda x: "Netflix" if x=="True" else ""))
stream["Hulu"] = stream["Hulu"].apply((lambda x: "Hulu" if x=="True" else ""))
stream["Prime Video"] = stream["Prime Video"].apply((lambda x: "Prime" if x=="True" else ""))
stream["Disney+"] = stream["Disney+"].apply((lambda x: "Disney+" if x=="True" else ""))
stream["Streaming"] = stream[["Netflix", "Hulu", "Prime Video", "Disney+"]].values.tolist()
stream.drop(labels =  ["Netflix","Hulu","Prime Video", "Disney+", "year", "title"], axis=1, inplace=True)

def clean_list(x):
    res = []
    for i in x:
        if i:
            res.append(i)
    res = str(res)
    res =  res.replace("[", "").replace("]", "").replace('\'', "")
    return res

stream["Streaming"] = stream["Streaming"].apply(clean_list)     
stream = stream.astype( {"Streaming": "string"}, errors="ignore")      

STREAM = "/Users/jon/Desktop/CS411 Project Data/Title-Stream-Union/tidystream.csv"


stream.to_csv(path_or_buf=STREAM, index=False)