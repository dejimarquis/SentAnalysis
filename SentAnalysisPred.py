import tweepy
import MyStreamListener

class SentAnalysis:

    request_limit = 20
    api = ""

    # insert your keys and secrets here
    twitter_keys = {
        'consumer_key': "",
        'consumer_secret': "",
        'access_token_key': "",
        'access_token_secret': ""
    }

    def __init__(self, request_limit=20):
        self.request_limit = request_limit
        self.set_up_creds()

    def set_up_creds(self):
        auth = tweepy.OAuthHandler(self.twitter_keys['consumer_key'], self.twitter_keys['consumer_secret'])
        auth.set_access_token(self.twitter_keys['access_token_key'], self.twitter_keys['access_token_secret'])
        self.api = tweepy.API(auth)

    def get_tweet_and_perform_sent_analysis(self):
        myStreamListener = MyStreamListener.MyStreamListener()
        myStreamListener.twitter_api = self.api
        myStream = tweepy.Stream(auth=self.api.auth, listener=myStreamListener)
        myStream.filter(track=['Buhari', 'PMB', 'APC', 'Atiku', 'PDP', 'Durotoye', 'Fela Durotoye', 'ANN', 'Donald Duke', 'SDP'],
                        languages=['en'])





if __name__ == '__main__':
        mine = SentAnalysis()
        mine.get_tweet_and_perform_sent_analysis()