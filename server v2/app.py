from flask import Flask
# from flask import jsonify
from bson.json_util import dumps, loads
import json

import pymongo


connection_url = "mongodb+srv://pranshul:iamnotsimp@cluster0.2etod.mongodb.net/<dbname>?retryWrites=true&w=majority"
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)

# Database
Database = client.get_database('codechella')
# Table
SampleTable = Database.data

#this is the method required
@app.route('/', methods=['GET'])
def findAll():
    query = SampleTable.find({}) # gets all the data as a cursor
    data_list = list(query) # converts that into a list
    x = dumps(data_list) # gets a string of the data retrieved
    f = open('a.txt', 'w')
    f.write(x)
    f = open('a.txt', 'r')


    text = f.readlines()
    stuff = ''
    for i in text:
        stuff = i
    stuff = '{ "foo" :' + stuff + '}'

    x = loads(stuff)
    for i in x['foo']:
        for j in i:
            print(j)
        # print(x)
    # y = loads(x) # converts it into a dict
    # for i in y['foo']:
    #     print(i)  # i will be a list with dicts in it
    return x
    
if __name__ == '__main__':
	app.run(debug=True)
