import tweepy
import json
import requests


class MyStreamListener(tweepy.StreamListener):

    # get this from Azure text analytic resource
    sentiment_api_headers = {""}
    sentiment_api_url = ""

    # when you create a powerbi datastream, a post url is given. Insert that here
    powerbi_url = ""

    totalCnt = 1
    buhari_cnt = 1
    atiku_cnt = 1
    durotoye_cnt = 1
    duke_cnt = 1

    buhari_list_of_text = []
    atiku_list_of_text = []
    durotoye_list_of_text = []
    duke_list_of_text = []

    totalApprovalCnt = 0
    buhari_approval_cnt = 0
    atiku_approval_cnt = 0
    durotoye_approval_cnt = 0
    duke_approval_cnt = 0

    publish_cnt = 0
    twitter_api = ""

    def on_status(self, status):

        if self.totalCnt % 900 == 0:
            self.process_sentiment_on_list()
            self.publish_to_powerbi_and_twitter()
            self.buhari_list_of_text = []
            self.atiku_list_of_text = []
            self.durotoye_list_of_text = []
            self.duke_list_of_text = []


        if ('Buhari' or 'PMB' or 'APC') in str(status.text):
            texts = {'language': 'en'}
            texts['id'] = self.buhari_cnt
            self.buhari_cnt += 1
            texts['text'] = status.text
            self.buhari_list_of_text.append(texts)

        if ('Atiku' or 'PDP') in str(status.text):
            texts = {'language': 'en'}
            texts['id'] = self.atiku_cnt
            self.atiku_cnt += 1
            texts['text'] = status.text
            self.atiku_list_of_text.append(texts)

        if ('Durotoye' or 'Fela Durotoye' or 'ANN') in str(status.text):
            texts = {'language': 'en'}
            texts['id'] = self.durotoye_cnt
            self.durotoye_cnt += 1
            texts['text'] = status.text
            self.durotoye_list_of_text.append(texts)

        if ('Donald Duke' or 'SDP') in str(status.text):
            texts = {'language': 'en'}
            texts['id'] = self.duke_cnt
            self.duke_cnt += 1
            texts['text'] = status.text
            self.duke_list_of_text.append(texts)
        self.totalCnt += 1

    def process_sentiment_on_list(self):
        if self.buhari_list_of_text:
            document = {'documents': self.buhari_list_of_text}
            scores = self.get_scores(document)
            if scores is not None:
                for i in range(len(scores)):
                    score = scores[i]['score']
                    if score > 0.74:
                        self.buhari_approval_cnt += 1
                        self.totalApprovalCnt += 1

        if self.atiku_list_of_text:
            document = {'documents': self.atiku_list_of_text}
            scores = self.get_scores(document)
            if scores is not None:
                for i in range(len(scores)):
                    score = scores[i]['score']
                    if score > 0.74:
                        self.atiku_approval_cnt += 1
                        self.totalApprovalCnt += 1

        if self.durotoye_list_of_text:
            document = {'documents': self.durotoye_list_of_text}
            scores = self.get_scores(document)
            if scores is not None:
                for i in range(len(scores)):
                    score = scores[i]['score']
                    if score > 0.74:
                        self.durotoye_approval_cnt += 1
                        self.totalApprovalCnt += 1

        if self.duke_list_of_text:
            document = {'documents': self.duke_list_of_text}
            scores = self.get_scores(document)
            if scores is not None:
                for i in range(len(scores)):
                    score = scores[i]['score']
                    if score > 0.74:
                        self.duke_approval_cnt += 1
                        self.totalApprovalCnt += 1

    def get_scores(self, document):
        response = requests.post(self.sentiment_api_url, headers=self.sentiment_api_headers, json=document)
        result = response.json()
        scores = json.loads(json.dumps(result))
        if 'documents' in scores:
            return scores['documents']

        return None

    def publish_to_powerbi_and_twitter(self):
        atiku_approval_rating = round((self.atiku_approval_cnt/self.totalApprovalCnt) * 100, 2)
        durotoye_approval_rating = round((self.durotoye_approval_cnt/self.totalApprovalCnt) * 100, 2)
        duke_approval_rating = round((self.duke_approval_cnt/self.totalApprovalCnt) * 100, 2)
        buhari_approval_rating = round((self.buhari_approval_cnt/self.totalApprovalCnt) * 100, 2)

        # dataa = [{'approvalRating': buhari_approval_rating, 'Candidate': 'Buhari'}]
        # dataa = str(json.dumps(dataa))
        # response = requests.post(self.powerbi_url, data=dataa)
        # print(response)
        #
        # dataa = [{'approvalRating': atiku_approval_rating, 'Candidate': 'Atiku'}]
        # dataa = str(json.dumps(dataa))
        # response = requests.post(self.powerbi_url, data=dataa)
        # print(response)
        #
        # dataa = [{'approvalRating': durotoye_approval_rating, 'Candidate': 'Fela Durotoye'}]
        # dataa = str(json.dumps(dataa))
        # response = requests.post(self.powerbi_url, data=dataa)
        # print(response)
        #
        # dataa = [{'approvalRating': duke_approval_rating, 'Candidate': 'Duke'}]
        # dataa = json.dumps(dataa)
        # response = requests.post(self.powerbi_url, data=dataa)
        # print(response)

        tweet = 'id: ' + str(self.publish_cnt) + '\n' + 'Candidate: Buhari, approvalRating: ' + str(buhari_approval_rating) + \
                '% \n' + 'Candidate: Atiku, approvalRating: ' + str(atiku_approval_rating) +'% \n' + \
                'Candidate: Durotoye, approvalRating: ' + str(durotoye_approval_rating) +'% \n' + \
                'Candidate: Duke, approvalRating: ' + str(duke_approval_rating) +'% \n'
        self.twitter_api.update_status(tweet)
        self.publish_cnt += 1
        print('success!')
