from featurizer import Featurizer
import pandas as pd
import numpy as np

df = pd.read_csv('stack_data_cleaned.csv', na_filter=False)

f = Featurizer(n_features = 100)

matrix_data = f.fit_transform(df.values)

np.savetxt('first_nmf_20.csv', matrix_data, delimiter=',')
