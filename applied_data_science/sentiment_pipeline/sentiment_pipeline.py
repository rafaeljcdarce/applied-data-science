import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import multiprocessing as mp
import tqdm

class SentimentPipeline():

    def __init__(self, workers=10, chunksize=100000, make_lower=False, remove_url=True, remove_user=True, remove_hash=False, threshold=0.05, pos_label=1, neu_label=0, neg_label=-1):
        self.workers = workers
        self.analyser = SentimentIntensityAnalyzer()
        self.chunksize = chunksize
        self.threshold = threshold
        self.pos = pos_label
        self.neu = neu_label
        self.neg = neg_label
        self.lower = make_lower
        self.url = remove_url
        self.user = remove_user
        self.hash = remove_hash

    def __call__(self,  df):

        print("\nCLEANING")
        clean_texts = self._clean_parallel(df['text'])
        
        print("\nANALYSING")
        sent_scores = self._analyse_parallel(clean_texts)
        
        print("\nCLASSIFYING")
        sents = self._classify_parallel(sent_scores)

        print("\nDONE")
        output = pd.DataFrame({"date": df['date'].tolist(), "text":clean_texts, "sentiment_score":sent_scores, "sentiment":sents})
        output = output.set_index('date')
        return output

    def _clean_parallel(self, texts):
        with mp.Pool(self.workers) as pool:
            return [i for i in pool.map(self._clean, tqdm.tqdm(texts), chunksize = self.chunksize)]

    def _analyse_parallel(self, texts):
        analyser = SentimentIntensityAnalyzer()
        with mp.Pool(self.workers) as pool:
            return [i['compound'] for i in pool.map(analyser.polarity_scores, tqdm.tqdm(texts), chunksize = self.chunksize)]
    
    def _classify_parallel(self, sents):
        with mp.Pool(self.workers) as pool:
            return [i for i in pool.map(self._classify, tqdm.tqdm(sents), chunksize = self.chunksize)]

    def _classify(self, sent):
        if sent >= self.threshold:
            return self.pos
        elif sent <= -self.threshold:
            return self.neg
        else:
            return self.neu
    
   
    def _clean(self, text):
        # https://gist.github.com/ravikiranj/2639031
        
        #Convert to lower case
        if self.lower:
            text = text.lower()

        #remove www.* or https?://* e.g. URLs
        if self.url:
            text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))',' ',text)

        #Remove @username
        if self.user:
            text = re.sub('@[^\s]+',' ',text)

        #Replace #word with word
        if self.hash:
            text = re.sub(r'#([^\s]+)', r'\1', text)

        #trim
        text = text.strip('\'"')

        return text


