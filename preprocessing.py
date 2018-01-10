from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from code_tokenizer import code_tokenizer
from sklearn.decomposition import NMF

class Preprocessor(object):

    def __init__(self, del_scores = False):
        self.del_scores = del_scores
        pass

    def parse_tags(self, tag_string):
        '''
        Parses the tags from the raw text in the dataset

        Input: single string of tags matching pattern "<tag>"

        Output: set of strings of the tags inside the <>
        '''
        tag_list = re.findall('<[-\w\.]*>', str(tag_string))
        tag_list = [tag[1:-1] for tag in tag_list]

        return set(tag_list)

    def parse_code_blocks(self, raw_string):
        '''
        Takes raw HTML text and splits into two strings of all words contained
        inside code blocks and all words outside of code blocks

        Input: Raw HTML string
        Output: Non-code string, Code string
        '''
        soup = BeautifulSoup(str(raw_string), 'lxml')
        b = soup.body
        code_blocks = b.find_all('code')

        code_tags = [tag.extract() for tag in code_blocks]
        code_strings = [tag.text for tag in code_tags]
        code = ''
        for string in code_strings:
            code += string
            code += ' '

        no_code = b.text
        no_code = re.sub('\n|\r', '', no_code)

        return {'no code': no_code, 'code': code}

    def test_function(self, num):
        return num * 0

    def transform(self, data):
        #id, title, body, q_score, answer, a_score, tags
        X = np.copy(data)
        num_rows = len(X)
        # first separate the two text bodies into code and non code texts
        #X[:,2] = self.parse_code_blocks(X[:,2])
        #X[:,4] = self.parse_code_blocks(X[:,4])
        #break the raw tag strings into sets of tags
        empty_cols = np.zeros((num_rows, 4))
        X = np.concatenate((X, empty_cols), axis = 1)

        for row in X:
            row[6] = self.parse_tags(row[6])
            row[7] = self.parse_code_blocks(row[2])['no code']
            row[8] = self.parse_code_blocks(row[2])['code']
            row[9] = self.parse_code_blocks(row[4])['no code']
            row[10] = self.parse_code_blocks(row[4])['code']
        X = np.delete(X, 4, 1)
        X = np.delete(X, 2, 1)
        if self.del_scores:
            X = np.delete(X, 3, 1)
            X = np.delete(X, 2, 1)

        non_code_texts = np.concatenate((X[:,3], X[:, 5]), axis = 0)
        code_texts = np.concatenate((X[:,4], X[:,6]))

        tfidf_ncode = TfidfVectorizer()
        non_code_matrix = tfidf_ncode.fit_transform(non_code_texts)



        print non_code_matrix.shape




        #X[:,6] = self.parse_tags(X[:,6])


        return X
