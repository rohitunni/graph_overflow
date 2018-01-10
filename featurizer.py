from preprocessing import Preprocessor
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.decomposition import NMF


class Featurizer(object):

    def __init__(self, n_features = 10):
        self.n_features = n_features


    def fit_transform(self, X):
        
        non_code_texts = np.concatenate((X[:,3], X[:, 5]), axis = 0)
        code_texts = np.concatenate((X[:,4], X[:,6]))

        tfidf_ncode = TfidfVectorizer()
        non_code_matrix = tfidf_ncode.fit_transform(non_code_texts)

        tfidf_code = TfidfVectorizer(tokenizer=code_tokenizer)
        code_matrix = tfidf_code.fit_transform(code_texts)
