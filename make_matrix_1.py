from featurizer import Featurizer
import pandas as pd
import numpy as np
import pickle

df = pd.read_csv('stack_data_cleaned.csv', na_filter=False)

f = Featurizer(n_features = 100, start_column = 7)

f.fit_lda(df.values)

f.lda_c.save('lda_code')
f.lda_nc.save('lda_noncode')

ncode_corp_dict = [f.corp_nc, f.dict_nc]

code_corp_dict = [f.corp_c, f.dict_c]

with open('ncode_corp_dict.pkl', 'wb') as fnc:
    pickle.dump(ncode_corp_dict, fnc)

with open('code_corp_dict.pkl', 'wb') as fc:
    pickle.dump(code_corp_dict, fc)
