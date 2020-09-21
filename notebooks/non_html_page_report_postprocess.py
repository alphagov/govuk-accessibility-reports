from src.helpers.preprocess_text import extract_from_path

import pandas as pd
import numpy as np
import ast

# import data
df = pd.read_csv(filepath_or_buffer='data/non_html_page_report.csv')

# explode so we have one attachment for each row
df['attachment_path'] = df['attachment_path'].apply(ast.literal_eval)
df_long = df.explode(column='attachment_path').copy()

# extract links
df_long['attachment_ext'] = df_long['attachment_path'].apply(lambda x: extract_from_path(data=x,
                                                                                         part='ext'))
# un-nest so can easily replace blanks
df_long['attachment_ext'] = df_long['attachment_ext'].apply(lambda x: ''.join(x))
df_long['attachment_ext'] = df_long['attachment_ext'].replace(to_replace='',
                                                              value=np.NaN)

# remove non-attachment and empty rows
df_long = df_long.dropna(subset=['attachment_path', 'attachment_ext'], how='any', axis=0)

# filter for after Sep 2018 for Specialist and Travel Advice publishers
df_long['first_published_at'] = df_long['first_published_at'].astype('datetime64[ns]')
cond_one = (df_long['publishing_app'] == 'specialist-publisher') & (df_long['first_published_at'] > '2018-09-30')
cond_two = (df_long['publishing_app'] == 'travel-advice-publisher') & (df_long['first_published_at'] > '2018-09-30')
cond_three = df_long['publishing_app'].isin(['publisher', 'service-manual-publisher'])
df_long = df_long[cond_one | cond_two | cond_three].copy()

# export three sets of files
#   i. all data in one file
#   ii. sample data in one file (for viewing purposes)
#   iii. all data but split by primary publishing organisation (for viewing purposes)

# i.
df_long.to_csv(path_or_buf='data/inaccessible_nonhtml_reports/full.csv', index=False)

# ii.
df_long.sample(n=10000, random_state=42).to_csv(path_or_buf='data/inaccessible_nonhtml_reports/sample.csv',
                                                index=False)

# iii.
df_long = df_long.set_index('publishing_app')
for key in df_long.index.unique():
    df_long.loc[key].to_csv('data/inaccessible_nonhtml_reports/{}.csv'.format(key),
                            index=False,
                            header=True)
