from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re


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

    pass
