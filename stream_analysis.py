from twitterapi import PoliceStream
from twitterapi import AzureSentiments
from Coordinates import locations
# pprint is used to format the JSON response
from pprint import pprint
import json
from numpy.random import randint
from pymongo import MongoClient
import helpers
import main

client = MongoClient('mongodb+srv://shreyas:copsense101@cluster0.2etod.mongodb.net/admin?retryWrites=true&w=majority')
dbnames = client.list_database_names()

policedata = PoliceStream()
azureSent = AzureSentiments() 

db = client.codechella
data = db.data

helpers.stream_update(policedata,azureSent,data,searchtime=1)

