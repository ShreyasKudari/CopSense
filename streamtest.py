import helpers
from twitterapi import PoliceStream
from twitterapi import AzureSentiments
from Coordinates import locations

policedata = PoliceStream()

helpers.stream_update(policedata)