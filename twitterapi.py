import tweepy
import creds
import os
import requests


class PoliceStream:
    def __init__(self):
        #auth for twitter api
        auth = tweepy.OAuthHandler(creds.consumer_key, creds.consumer_secret)
        auth.set_access_token(creds.access_token, creds.access_token_secret)
        self.api = tweepy.API(auth)
        
    def getPoliceTweets(self, hashtag="police OR cops OR #Police OR #police OR co OR police brutality", count=1,coordinates="33.99381794192959,-118.09065927851562,50mi"):
        return tweepy.Cursor(self.api.search,q=hashtag,count=count,lang="en",geocode = coordinates).items(count)



#auth for azure text-analytics
class AzureSentiments:
    def __init__(self):
        self.subscription_key = creds.subscription_key
        endpoint = creds.endpoint
        # self.sentiment_url = endpoint + "/text/analytics/v3.1-preview.2/sentiment?opinionMining=True"
        self.keyword_url = endpoint + "/text/analytics/v3.1-preview.2/keyPhrases"
        self.id = 1
    def createDocument(self, parselist, lang="en"):
        self.documents = {"documents":[]}
        for tweet in parselist:
            self.documents['documents'].append({"id": self.id, "language": lang,
                    "text": tweet})
            self.id+=1                
    # def getSentiments(self):
    #     headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
    #     response = requests.post(self.sentiment_url, headers=headers, json=self.documents)
    #     return response.json()
    def getKeyword(self):
        headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
        key_response = requests.post(self.keyword_url, headers=headers, json=self.documents)
        return key_response.json()


