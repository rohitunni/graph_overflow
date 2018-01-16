import re


def code_tokenizer(input_string):
    methods_re = '(?<!\w)[npd]{2}\.[\w_]+(?=[\(\[])|\.[\w|_]*(?=[\(|\[])'
    tokens = re.findall(methods_re, input_string)
    new_str = re.sub(methods_re, '', input_string)
    other_funcs_re = '[\w_]+(?=[\(\[])'
    tokens.extend(re.findall(other_funcs_re, new_str))
    new_str = re.sub(other_funcs_re, '', new_str)
    tokens.extend(re.split('\W+', new_str))
    tokens = [token.lower() for token in tokens if len(token) > 0]

    return tokens


if __name__ == '__main__':
    t_str = 'index[5] rand_object.execute_it(select * from people) mean(function) \
            for row something.iloc[5] hello \n np.delete(something, something) and \
            pd.DataFrame(something else)'

    #print code_tokenizer(t_str)
