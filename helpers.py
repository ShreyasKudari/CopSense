from twitterapi import PoliceStream
from twitterapi import AzureSentiments
from twitterapi import StreamListener
from Coordinates import locations
import tweepy
import numpy as np
def search_update(policedata, azureSent, state_info, count = 1):
    geodata = state_info['Longitude']+','+state_info['Latitude']+','+'1000mi'
    tweets = policedata.getPoliceTweets(count = count,coordinates=geodata)
    ##Possible call to preprocess tweets
    parselist = [tweet.text for tweet in tweets]
    pos = [0,0,0,0,0]
    neg = [0,0,0,0,0]
    neut = [0,0,0,0,0]
    if len(parselist)==0:
        return pos,neg,neut,[],[],[]
    azureSent.createDocument(parselist)
    sentiments = azureSent.getSentiments()
   
    print(sentiments)
    i = 0
    for sentiment in sentiments['documents']:
        pos[i]=(sentiment['confidenceScores']['positive'])
        neg[i]=(sentiment['confidenceScores']['negative'])
        neut[i]=(sentiment['confidenceScores']['neutral'])
        i+=1
    postweets = [parselist[np.argmax(pos)]]
    negtweets = [parselist[np.argmax(neg)]]
    neutweets = [parselist[np.argmax(neut)]]
    return pos,neg,neut,postweets,negtweets,neutweets


def stream_update(policedata):
    listener = StreamListener()
    stream = tweepy.Stream(auth = policedata.api.auth, listener = listener)
    stream.filter(track=['police','cops','cop','#Police','#PoliceBrutality','#Cops'])

   