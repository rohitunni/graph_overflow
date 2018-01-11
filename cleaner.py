from preprocessing import Preprocessor
import pandas as pd
import numpy as np
import boto




df = pd.read_csv('stackodata.csv')

p = Preprocessor()

cleaned_data = p.transform(df.values)

df_cleaned = pd.DataFrame(cleaned_data, columns = ['id', 'title', 'qscore', 'ascore',
                                                   'tags', 'q_nocode', 'q_code',
                                                   'a_nocode', 'a_code'])

df_cleaned.to_csv('stack_data_cleaned.csv', encoding = 'utf-8')
