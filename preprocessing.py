from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


class Preprocessor(object):

    def __init__(self):
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
        print X.shape

        for row in X:
            row[6] = self.parse_tags(row[6])
            row[7] = self.parse_code_blocks(row[2])['no code']
            row[8] = self.parse_code_blocks(row[2])['code']
            row[9] = self.parse_code_blocks(row[4])['no code']
            row[10] = self.parse_code_blocks(row[4])['code']




        #X[:,6] = self.parse_tags(X[:,6])


        return X
