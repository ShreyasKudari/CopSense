from twitterapi import PoliceStream
from twitterapi import AzureSentiments
# pprint is used to format the JSON response
from pprint import pprint

policedata = PoliceStream()
tweets = policedata.getPoliceTweets()
# for tweet in tweets:
    # print(tweet.created_at, tweet.place.name if tweet.place else "Undefined place", tweet.text)
parselist = [tweet.text for tweet in tweets]
azureSent = AzureSentiments()
azureSent.createDocument(parselist)
#Printing out the Json format
pprint(azureSent.getSentiments())