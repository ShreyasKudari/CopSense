from twitterapi import PoliceStream
from twitterapi import AzureSentiments
from Coordinates import locations
# pprint is used to format the JSON response
from pprint import pprint
import json
from numpy.random import randint
from pymongo import MongoClient
import helpers

client = MongoClient('mongodb+srv://shreyas:copsense101@cluster0.2etod.mongodb.net/admin?retryWrites=true&w=majority')
dbnames = client.list_database_names()

#database name is codechella
#collection name is data
# if 'codechella' not in dbnames:
#     db = client['codechella']
#     data.insert_many(locations["cords"])

db = client.codechella
data = db.data
# data.delete_many({})
# data.update_many({},{"$unset":{"Neurtrals": ""}})
policedata = PoliceStream()
azureSent = AzureSentiments() 
for state_info in locations['cords']:
    #geodata = state_info['latitude']+','+state_info['longitude']+','+'600mi'
    pos, neg, neut, postweet, negtweet, neutweet = helpers.search_update(policedata,azureSent,state_info,count=5)
    data.update_one({'State':state_info['State']},{"$set":{"Positives":pos,"Negatives":neg,"Neutrals":neut,
                                                            "PosTweet":postweet,"NegTweet":negtweet,"NeuTweet":neutweet
                                                            }},upsert=False)
# cap = 5
# data.insert_many(locations["cords"])
# data.update_many({},
#             { "$set": {"PosTweet":["sample positive tweet"],"NegTweet":["sample negative tweet"],"NeuTweet":["sample neutral tweet"]}}
#                 ,upsert = False)


# tweets = policedata.getPoliceTweets()
# for tweet in tweets:
#     # print(tweet.created_at, tweet.place.name if tweet.place else "Undefined place", tweet.text)
#parselist = [tweet.text for tweet in tweets]
# # print(parselist)

# azureSent.createDocument(parselist)
# # #Printing out the Json format
# sentiments = azureSent.getSentiments()
# # with open('data.txt', 'w') as outfile:
# #     json.dump(sentiments, outfile)
# pprint(sentiments)