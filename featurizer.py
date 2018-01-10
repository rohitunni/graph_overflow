from preprocessing import Preprocessor
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.decomposition import NMF
from code_tokenizer import code_tokenizer


class Featurizer(object):

    def __init__(self, n_features = 10, start_column = 5):
        self.s = start_column
        self.n_features = n_features
        self.nmf_ncode = None
        self.nmf_code = None

    def make_feature_matrix(self, X, is_code = False):
        if is_code:
            tfidf = TfidfVectorizer(tokenizer = code_tokenizer)
        else:
            tfidf = TfidfVectorizer()
        full_matrix = tfidf.fit_transform(X)

        nmf = NMF(n_components = self.n_features)

        

        reduced_matrix = nmf.fit_transform(full_matrix)

        return reduced_matrix


    def fit_transform(self, X):

        non_code_texts = np.concatenate((X[:,self.s], X[:, self.s+2]), axis = 0)
        code_texts = np.concatenate((X[:,self.s+1], X[:,self.s+3]), axis = 0)

        non_code_matrix = self.make_feature_matrix(non_code_texts, is_code = False)

        code_matrix = self.make_feature_matrix(code_texts, is_code = True)

        rejoined_ncode = np.concatenate(np.split(non_code_matrix, 2, axis = 0), axis = 1)

        rejoined_code = np.concatenate(np.split(code_matrix, 2, axis = 0), axis = 1)

        full_matrix = np.concatenate([rejoined_ncode, rejoined_code], axis = 1)

        return full_matrix
