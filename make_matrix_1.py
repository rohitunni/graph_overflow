from featurizer import Featurizer
import pandas as pd
import numpy as np

df = pd.read_csv('stack_data_cleaned.csv', na_filter=False)

f = Featurizer(n_features = 100, start_column = 7)

matrix_data = f.fit_transform(df.values)

non_code_topics = f.topics[0]

code_topics = f.topics[1]

np.savetxt('svd100.csv', matrix_data)

np.savez('latent_features', non_code_topics, code_topics)
