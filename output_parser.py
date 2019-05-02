import json
import os
from types import SimpleNamespace

path = './json_outputs/'

queries_dic = {}
queries = open("stemmed_queries.txt", "r", encoding="mbcs")
i=1
for line in queries:
    queries_dic[line.rstrip()] = i
    i+=1

outfile = open("resultado.txt","w+")

for filename in os.listdir(path):
    with open(path+filename, "r", encoding="mbcs") as read_file:
        data = json.load(read_file, object_hook=lambda d: SimpleNamespace(**d))

    for document in data.hits:
        outfile.write(str(queries_dic[data.q]) + ' Q0 ' + (vars(document.doc)['docno'])[0] + ' ' + str(document.score) + ' natasha_guilherme' + '\n')

outfile.close()