from refinetweets import refineTweets
from twitterapi import PoliceStream
from twitterapi import AzureSentiments
from sentopinion import sentiment_analysis_with_opinion_mining
from client_auth import authenticate_client
from pprint import pprint

policedata = PoliceStream()
tweets = policedata.getPoliceTweets()
parselist = [tweet.text for tweet in tweets]
# parselist = ['The food and service were unacceptable, but the concierge were nice']


def has_intersection(tweet_data, word_dep, keywords):
    tokens = {}
    for w,x,y,i in tweet_data:
        tokens[i] = w

    wd = []
    for _, a, b in word_dep:
        wd.append(tokens.get(a-1, ""))
        wd.append(tokens.get(b-1, ""))

    list_of_kwords = []
    for i in keywords['documents']:
        for j in i['keyPhrases']:
            list_of_kwords += j.split()


    wd = set(wd)
    k = set(list_of_kwords)
    intersection = wd.intersection(k)
    if intersection:
        return True
    else:
        return False

def remove_reports(tweet_data):
    for data in tweet_data:
        if (data[0]=='cops' or data[0]=='cop' or data[0]=='copping') and data[1]=='VBD':
            return False
        else:
            return True

def get_location(tweet_data):
    location = []
    for data in tweet_data:
        if (data[2]=='CITY' or data[2]=='LOCATION' or data[2]=='STATE_OR_PROVINCE'):
            location.append(data[0])
    return location


client = authenticate_client()

for tweet in parselist:
    tweet_data, word_dep = refineTweets(tweet)
    azureSent = AzureSentiments()
    azureSent.createDocument([tweet])
    keywords = azureSent.getKeyword()

    if has_intersection(tweet_data, word_dep, keywords) and remove_reports(tweet_data):
        sentiment_analysis_with_opinion_mining(client, [tweet])

    tweet_loc = get_location(tweet_data)




