import json
import os
from types import SimpleNamespace

path = './output/'

outfile = open("output.txt","w+")

for filename in os.listdir(path):
    with open(path+filename, "r") as read_file:
        data = json.load(read_file, object_hook=lambda d: SimpleNamespace(**d))

    for document in data.hits:
        outfile.write(str(int(filename[0])+1) + ' Q0 ' + (vars(document.doc)['docno'])[0] + ' ' + str(data.hits.index(document)) + ' ' + str(document.score) + ' natasha_guilherme' + '\n')

outfile.close()