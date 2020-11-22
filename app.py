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


@app.route('/v', methods=['GET'])
def findAll():
    query = SampleTable.find({})  # gets all the data as a cursor
    queried = {
        "key1": [['State', 'Sentiment']],#, 'Sentiment Data']],
        "key2": [],
        "key3": [],
        "key4": []
    }
    for item in query:
        positives = round(sum(item['Positives'])/len(item['Positives'])
                          if len(item['Positives']) != 0 else 0, 2)
        negatives = round(sum(item['Negatives'])/len(item['Negatives'])
                          if len(item['Negatives']) != 0 else 0, 2)
        neutrals = round(sum(item['Neutrals'])/len(item['Neutrals'])
                         if len(item['Neutrals']) != 0 else 0, 2)
        score = round(0.5, 2)
        if positives > 0.5:
            score = positives
        elif negatives > 0.5:
            score = 1-negatives
        x = 'Positive: ' + str(positives) + ' Negatives: ' + str(negatives) + ' Neutrals: ' + str(neutrals) 
        queried['key1'].append(
            [item['State'], score])#, x])
        queried['key2'].append(item['PosTweet'])
        queried['key3'].append(item['NegTweet'])
        queried['key4'].append(item['NeuTweet'])
        print(type(item['PosTweet']))
    return queried


if __name__ == '__main__':
	app.run(debug=True)
