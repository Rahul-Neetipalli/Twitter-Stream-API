from django.db import models
import json
from tweepy.streaming import StreamListener




class listener(StreamListener):

    def on_data(self, data):
        datajson = json.loads(data) #understand this
        created_at = datajson['created_at']
        print("Tweet collected at " + created_at)
        #print("id = " + str(datajson['id_str']) )
        return True

    def on_error(self, status):
        print (status)
