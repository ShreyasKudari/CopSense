from twitterapi import PoliceStream
from twitterapi import AzureSentiments
from twitterapi import StreamListener
from Coordinates import locations
import tweepy
import numpy as np
import main
from refinetweets import refineTweets
from boundingbox import boxes
import time

def search_update(policedata, azureSent, state_info, count = 1):
    geodata = state_info['Longitude']+','+state_info['Latitude']+','+'600mi'
    tweets = policedata.getPoliceTweets(count = count,coordinates=geodata)
    
    parselist = [tweet.text for tweet in tweets]
    analyzeList = []
    for tweet in parselist:
        tweet_data, word_dep = refineTweets(tweet)
        azureSent.createDocument([tweet])
        keywords = azureSent.getKeyword()
        if main.has_intersection(tweet_data, word_dep, keywords) and main.remove_reports(tweet_data):
            analyzeList.append(tweet)
    parselist = analyzeList
    pos = []
    neg = []
    neut = []
   
    if len(parselist)==0:
        return pos,neg,neut,[],[],[]
    
    azureSent.createDocument(parselist)
    sentiments = azureSent.getSentiments()
   
    print(sentiments)
    i = 0
    pos = []
    neg = []
    neut = []
    for sentiment in sentiments['documents']:
        pos.append(sentiment['confidenceScores']['positive'])
        neg.append(sentiment['confidenceScores']['negative'])
        neut.append(sentiment['confidenceScores']['neutral'])
        i+=1
    postweets = [parselist[np.argmax(pos)]]
    negtweets = [parselist[np.argmax(neg)]]
    neutweets = [parselist[np.argmax(neut)]]
    return pos,neg,neut,postweets,negtweets,neutweets

def azurelist(parselist, azureSent):
    analyzeList = []
    for tweet in parselist:
        tweet_data, word_dep = refineTweets(tweet)
        azureSent.createDocument([tweet])
        keywords = azureSent.getKeyword()
        if main.has_intersection(tweet_data, word_dep, keywords) and main.remove_reports(tweet_data):
            analyzeList.append(tweet)
    pos = []
    neg = []
    neut = []
    parselist = analyzeList
    if len(parselist)==0:
        return pos,neg,neut,[],[],[]

    azureSent.createDocument(parselist)
    sentiments = azureSent.getSentiments()

    print(sentiments)

    pos = []
    neg = []
    neut = []
    for sentiment in sentiments['documents']:
        pos.append(sentiment['confidenceScores']['positive'])
        neg.append(sentiment['confidenceScores']['negative'])
        neut.append(sentiment['confidenceScores']['neutral'])

    postweets = [parselist[np.argmax(pos)]]
    negtweets = [parselist[np.argmax(neg)]]
    neutweets = [parselist[np.argmax(neut)]]
    return pos,neg,neut,postweets,negtweets,neutweets

def stream_update(policedata, azureSent,  data, searchtime = 1):
    runtime = 60 #timeout for 60 seconds

    for iteration in range(searchtime):
        statenumber = 0
        for geobox in boxes:
            listener = StreamListener()
            stream = tweepy.Stream(auth = policedata.api.auth, listener = listener)
            stream.filter(locations = geobox)
            stream.disconnect()
            parselist = listener.parselist
            print(parselist)
            pos, neg, neut, postweet, negtweet, neutweet = azurelist(parselist,azureSent)
            if len(pos)==0: continue
            state_info = locations['cords'][statenumber]
            
            data.update_one({'State':state_info['State']},{"$push":{"Positives":pos,"Negatives":neg,"Neutrals":neut,
                                                            "PosTweet":postweet,"NegTweet":negtweet,"NeuTweet":neutweet
                                                            }},upsert=False)
            data.update_one({'State':state_info['State']},{"$set":{"PosTweet":postweet,"NegTweet":negtweet,"NeuTweet":neutweet
                                                            }},upsert=False)
            statenumber+=1