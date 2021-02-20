from elasticsearch import Elasticsearch
import os
import glob
import pandas as pd
import codecs

def extractFiles(files):
    this_loc=1
    df = pd.DataFrame(columns = ("name","content"))
    for file in files:
        transcript = codecs.open(file, "r", "utf-8")
        df.loc[this_loc]= file,transcript.read()
        this_loc += 1
    return df

os.chdir("D:/path/to/your/directory/x")
files = glob.glob("*.*")

df=extractFiles(files)
print(df.head())

es = Elasticsearch()
col_names=df.columns

for row in range(df.shape[0]):
    body = dict([(name,str(df.iloc[row][name])) for name in col_names])
    es.index(index = "tbmmrecords", body =body)
    
