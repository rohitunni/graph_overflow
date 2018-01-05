from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


class Preprocessor(object):

    def __init__(self):
        pass

    def parse_tags(tag_string):
        '''
        Parses the tags from the raw text in the dataset

        Input: single string of tags matching pattern "<tag>"

        Output: set of strings of the tags inside the <>
        '''
        tag_list = re.findall('<[-\w\.]*>', tag_string)
        tag_list = [tag[1:-1] for tag in tag_list]

        return set(tag)

    def parse_code_blocks(raw_text):
        '''
        Takes raw HTML text and splits into two strings of all words contained
        inside code blocks and all words outside of code blocks

        Input: Raw HTML string
        Output: Non-code string, Code string
        '''

        soup = BeautifulSoup(raw_text)
        b = soup.body
        code_blocks = b.find_all('code')

        code_tags = [tag.extract() for tag in code_blocks]
        code_strings = [tag.text for tag in code_tags]
        code = ''
        for string in code_strings:
            code += string
            code += ' '

        no_code = b.text
        no_code = re.sub('\n', '', no_code)


        return no_code, code
