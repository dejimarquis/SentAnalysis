import tweepy
import datetime
import time
import requests
import MyStreamListener
from datetime import datetime, timedelta


class SentAnalysis:

    request_limit = 20
    api = ""
    data = []
    program_end_time = datetime.now() + timedelta(days=1)
    headers = {"Ocp-Apim-Subscription-Key": "5abfc68054d94cf59d03d3194e231577"}
    sentiment_api_url = "https://westus2.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"

    twitter_keys = {
        'consumer_key': "2ZDxwFRNlqbiBIdOtFu5Ilfql",
        'consumer_secret': "kVruU1qKLAeRKuj49vOg5vFZKPOkYFP8WGQGtvedQFSyViK3pl",
        'access_token_key': "389622860-wozPQKO4aEwetq1VaQnD06hx7kudH8mbPzKItsfT",
        'access_token_secret': "bcTmQY6r2ap4iCWZkR4XmBnrObE6AG6mrXKz6627P8vzf"
    }

    def __init__(self, request_limit=20):
        self.request_limit = request_limit
        self.set_up_creds()

    def set_up_creds(self):
        auth = tweepy.OAuthHandler(self.twitter_keys['consumer_key'], self.twitter_keys['consumer_secret'])
        auth.set_access_token(self.twitter_keys['access_token_key'], self.twitter_keys['access_token_secret'])
        self.api = tweepy.API(auth)

    def livestream_of_tweets(self):
        myStreamListener = MyStreamListener.MyStreamListener()
        myStream = tweepy.Stream(auth=self.api.auth, listener=myStreamListener)
        myStream.filter(track=['Buhari', 'PMB', 'APC', 'Atiku', 'PDP', 'Durotoye', 'Fela Durotoye', 'ANN', 'Donald Duke', 'SDP'],
                        languages=['en'])


    def send_data_to_powerbi_api(self):

            self.livestream_of_tweets()
        # while datetime.now() < self.program_end_time:
        #     time.sleep(60*60*5)
        #     # get sentAnalysis data
        #     documents = self.mine_user_tweets()
        #     response = requests.post(self.sentiment_api_url, headers=self.headers, json=documents)
        #     sentiments = response.json()
        #     print(sentiments)






if __name__ == '__main__':
    mine = SentAnalysis()
    print(mine.send_data_to_powerbi_api())