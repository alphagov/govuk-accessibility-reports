import time

import pandas as pd
import numpy as np

from pandarallel import pandarallel
import multiprocessing

from notebooks.functions import extract_publishing_organisation
from notebooks.functions import extract_title
from notebooks.functions import detect_language

# create dictionaries and headers to specify dtype and date columns
dict_header = {'base_path': object,
               'content_id': object,
               'title': object,
               'description': object,
               'publishing_app': object,
               'document_type': object,
               'details': object,
               'text': object,
               'organisations': object,
               'taxons': object,
               'step_by_steps': object,
               'details_parts': object,
               'first_published_at': object,
               'public_updated_at': object,
               'updated_at': object,
               'finder': object,
               'facet_values': object,
               'facet_groups': object,
               'has_brexit_no_deal_notice': bool,
               'withdrawn': bool,
               'withdrawn_at': object,
               'withdrawn_explanation': object}
list_header_date = ['first_published_at',
                    'public_updated_at',
                    'updated_at',
                    'withdrawn_at']

# load data
df = pd.read_csv(filepath_or_buffer='data/preprocessed_content_store_200820.csv.gz',
                 compression='gzip',
                 encoding='utf-8',
                 sep='\t',
                 header=0,
                 names=list(dict_header.keys()),
                 dtype=dict_header,
                 parse_dates=list_header_date)

dict_header = {'base_path': object,
               'text': object,
               'text_languages': object,
               'detected_as_english': object}

df_lang_detect = pd.read_csv(filepath_or_buffer='data/non_english_docs_report.csv',
                             header=0,
                             names=list(dict_header.keys()),
                             dtype=dict_header)

df = df[['base_path', 'publishing_app', 'document_type', 'details', 'organisations']].merge(right=df_lang_detect,
                                                                                            on='base_path',
                                                                                            how='left')

del dict_header, list_header_date, df_lang_detect

# preprocessing
df['organisation_name'] = df['organisations'].apply(lambda x: extract_publishing_organisation(content_item=x,
                                                                                              key='primary_publishing_organisation',
                                                                                              index=1))
# filter for pages with 'attachments'
df['details_attachment_exists'] = df['details'].str.contains('\'attachments\'\: \[', na = False)
df_attachment = df.query('details_attachment_exists == True').copy()

# extracting title links
df_attachment['attachment_title_dict'] = df_attachment['details'].apply(extract_title)

# keep only pages with actual attachments on
df_attachment = df_attachment[df_attachment['attachment_title_dict'].map(lambda d: len(d) > 0)]


# language detection
n_cores = multiprocessing.cpu_count() - 1
pandarallel.initialize(nb_workers=n_cores, progress_bar=True, use_memory_fs=False)

df_extract = df_attachment[['base_path',
                            'publishing_app',
                            'organisation_name',
                            'document_type',
                            'text',
                            'text_languages',
                            'attachment_title_dict']].copy()
# make every list item a row entry
df_extract = df_extract.explode('attachment_title_dict')

# detect attachment title language
start = time.time()
df_extract['attachment_title_lang'] = df_extract['attachment_title_dict'].parallel_apply(detect_language)
print(time.time() - start)

df_extract = df_extract.rename(columns={'text_languages': 'text_lang',
                                        'attachment_title_dict': 'attachment_title'})

# save intermediary result so don't have to run func_detectlangs again
df_extract.to_pickle('../data/df_attachment.pkl')


# formatting

# extract language, by taking first list item
# note: `text_lang` is string whereas `attachment_title_lang` is list
df_extract['text_lang_main'] = df_extract['text_lang'].str[1:3]
df_extract['attachment_title_lang_main'] = df_extract['attachment_title_lang'].str[0]
df_extract[['attachment_title_lang_main', 'attachment_title_lang_main_score']] = df_extract['attachment_title_lang_main'].astype(str).str.split('\:', expand=True)


# see if text language is same as attachment title language
df_extract['check'] = np.where((df_extract['text_lang_main'] == df_extract['attachment_title_lang_main']), True, False)

# prepare data output to save as .csv
df_output = df_extract.query('check == False').copy()
df_output = df_output[['base_path', 'organisation_name', 'publishing_app', 'document_type', 'text', 'text_lang_main', 'attachment_title', 'attachment_title_lang_main']]

# save as separate csvs by organisation
df_output['organisation_name'] = df_output['organisation_name'].apply(lambda x: ', '.join([str(i) for i in x]))
df_output = df_output.set_index('organisation_name')
df_output.to_csv('../data/non_english_attachment_report.csv')
for key in df_output.index.unique():
    df_output.loc[key].to_csv('data/attachment/{}_attachment_report.csv'.format(key), index=False, header=True)
