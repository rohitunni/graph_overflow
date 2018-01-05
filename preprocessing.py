from bs4 import BeautifulSoup as bs
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
