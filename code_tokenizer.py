import re

def code_tokenizer(input_string):
    # regex to extract object methods in python without including the object
    # name, except for common prefixes like np. and pd.
    methods_re = '(?<!\w)[npd]{2}\.[\w_]+(?=[\(\[])|\.[\w|_]*(?=[\(|\[])'
    tokens = re.findall(methods_re, input_string)
    new_str = re.sub(methods_re, '', input_string)
    # extracts any other functions not picked up by first regex
    other_funcs_re = '[\w_]+(?=[\(\[])'
    tokens.extend(re.findall(other_funcs_re, new_str))
    new_str = re.sub(other_funcs_re, '', new_str)
    # for any code not picked up as a function or method, splits in the standard
    # way just on non alphanumeric characters
    tokens.extend(re.split('\W+', new_str))
    # makes all tokens lowercase
    tokens = [token.lower() for token in tokens if len(token) > 0]

    return tokens
