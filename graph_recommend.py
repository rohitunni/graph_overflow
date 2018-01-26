import snap
import gensim
from gensim import models, similarities
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
import pandas as pd

class Recommender(object):

    def __init__(self, lda, dictionary, index, graph):
        self.lda = lda
        self.dict = dictionary
        self.index = index
        self.stop_words = get_stop_words('en')
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.g = graph
        self.current_node = None

    def traverse(self):
        if self.current_node == None:
            print "Have not chosen starting node!"
        else:
            pass



    def make_bow(self, query):
        p_stemmer = PorterStemmer()

        raw = query.lower()

        tokens = self.tokenizer.tokenize(raw)

        # remove stop words and stem tokens
        stopped_tokens = [i for i in tokens if not i in self.stop_words]
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        # add tokens to document list
        bow_doc = self.dict.doc2bow(stemmed_tokens)

        return bow_doc

    def recommend(self, query):

        df = pd.read_csv('stack_data_cleaned.csv', na_filter=False)

        bow_doc = self.make_bow(query)

        vec_lda = self.lda[bow_doc]

        best_node = self.index[vec_lda][0]

        self.current_node = best_node[0]

        print df.iloc[best_node[0]]
