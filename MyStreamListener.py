import tweepy
import json
import time

#override tweepy.StreamListener to add logic to on_status


class MyStreamListener(tweepy.StreamListener):
    totalCnt = 1
    buhari_cnt = 1
    atiku_cnt = 1
    durotoye_cnt = 1
    duke_cnt = 1

    buhari_list_of_text = []
    atiku_list_of_text = []
    durotoye_list_of_text = []
    duke_list_of_text = []

    def on_status(self, status):
        candidates = {}
        document = {}
        if self.totalCnt % 50 == 0:
            time.sleep(60*5)

        if ('Buhari' or 'PMB' or 'APC') in str(status.text):
            texts = {'id': self.buhari_cnt}
            self.buhari_cnt += 1
            texts['language'] = 'en'
            texts['text'] = status.text
            self.buhari_list_of_text.append(texts)

        if ('Atiku' or 'PDP') in str(status.text):
            texts = {'id': self.atiku_cnt}
            self.atiku_cnt += 1
            texts['language'] = 'en'
            texts['text'] = status.text
            self.atiku_list_of_text.append(texts)

        if ('Durotoye' or 'Fela Durotoye' or 'ANN') in str(status.text):
            texts = {'id': self.durotoye_cnt}
            self.durotoye_cnt += 1
            texts['language'] = 'en'
            texts['text'] = status.text
            self.durotoye_list_of_text.append(texts)

        if ('Donald Duke' or 'SDP') in str(status.text):
            texts = {'id': self.duke_cnt}
            self.duke_cnt += 1
            texts['language'] = 'en'
            texts['text'] = status.text
            self.duke_list_of_text.append(texts)
        self.totalCnt += 1
        print(status.text)