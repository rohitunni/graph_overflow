import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.decomposition import NMF, PCA, TruncatedSVD
from code_tokenizer import code_tokenizer
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
import gensim


class Featurizer(object):
    ''' Takes the cleaned and split data from the preprocessing and feeds it
    into gensim's LDA model to create a feature matrix
    '''

    def __init__(self, n_features = 100, start_column = 7, size = 30000):
        self.s = start_column
        self.n_features = n_features
        self.size = size
        self.nmf_ncode = None
        self.nmf_code = None
        self.topics = []
        self.dict_nc = None
        self.dict_c = None
        self.corp_nc = None
        self.corp_c = None
        self.lda_nc = None
        self.lda_c = None

    def make_lda(self, doc_list, is_code = False):
        en_stop = get_stop_words('en')

        tokenizer = RegexpTokenizer(r'\w+')

         # Create p_stemmer of class PorterStemmer
        p_stemmer = PorterStemmer()
        # create sample documents

        # list for tokenized documents in loop
        texts = []
        # loop through document list
        for i, doc in enumerate(doc_list):
            # clean and tokenize document string
            raw = doc.lower()
            if is_code:
                tokens = code_tokenizer(raw)
            else:
                tokens = tokenizer.tokenize(raw)
            # remove stop words from tokens
            stopped_tokens = [i for i in tokens if not i in en_stop]
            # stem tokens
            stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
            # add tokens to list
            texts.append(stemmed_tokens)
            if i % 100000 == 0:
                print(i)

        print("Finished tokenizing and stemming \n")

        # turn our tokenized documents into a id <-> term dictionary
        dictionary = corpora.Dictionary(texts)
        # convert tokenized documents into a document-term matrix
        corpus = [dictionary.doc2bow(text) for text in texts]

        print("Made corpus\n")

        # generate LDA model in chunks
        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        lda = models.ldamulticore.LdaMulticore(corpus[:self.size], num_topics=50, id2word = dictionary, passes=2)

        print("First {}\n".format(self.size))

        for chunk in chunker(corpus[self.size:], self.size):
            lda.update(chunk)
            print("Next {}\n".format(self.size))

        print("Done!")

        return dictionary, corpus, lda




    def make_feature_matrix(self, X, is_code = False):
        if is_code:
            tfidf = TfidfVectorizer(tokenizer = code_tokenizer, stop_words = 'english',
                                    sublinear_tf=True, use_idf=True)
        else:
            tfidf = TfidfVectorizer(stop_words = 'english', sublinear_tf=True,
                                    use_idf=True)


        full_matrix = tfidf.fit_transform(X)

        features = tfidf.get_feature_names()

        print("Made tfidf")

        svd = TruncatedSVD(n_components = self.n_features)



        reduced_matrix = svd.fit_transform(full_matrix.toarray())

        print ("Finished SVD")

        num_words = 20
        top_words = []
        for topic in svd.components_:
            top_words.append([features[i] for i in topic.argsort()[:-num_words - 1:-1]])

        self.topics.append(top_words)

        return reduced_matrix


    def fit_transform(self, X):

        non_code_texts = np.concatenate((X[:,self.s], X[:, self.s+2]), axis = 0)
        code_texts = np.concatenate((X[:,self.s+1], X[:,self.s+3]), axis = 0)

        non_code_matrix = self.make_feature_matrix(non_code_texts, is_code = False)

        code_matrix = self.make_feature_matrix(code_texts, is_code = True)

        rejoined_ncode = np.split(non_code_matrix, 2, axis = 0)

        rejoined_code = np.split(code_matrix, 2, axis = 0)

        full_matrix = np.concatenate([rejoined_ncode[0].reshape(-1,1),
                                      rejoined_code[0].reshape(-1,1),
                                      rejoined_ncode[1].reshape(-1,1),
                                      rejoined_code[1]].reshape(-1,1), axis = 1)

        return full_matrix

    def fit_lda(self, X):

        # The columns come in as question non_code, question code, answer non_code, answer code
        # First the non_code and code columns are appended together
        non_code_texts = np.concatenate((X[:,self.s], X[:, self.s+2]), axis = 0)
        code_texts = np.concatenate((X[:,self.s+1], X[:,self.s+3]), axis = 0)

        # Then are fed into the LDA model

        self.dict_nc, self.corp_nc, self.lda_nc = self.make_lda(non_code_texts, is_code = False)

        self.dict_c, self.corp_c, self.lda_c = self.make_lda(code_texts, is_code = True)
