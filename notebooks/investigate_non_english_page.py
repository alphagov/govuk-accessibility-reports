import pandas as pd
from notebooks.functions.non_english import extract_publishing_organisation

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

df_lang_detect = df[['base_path', 'publishing_app', 'document_type', 'organisations']].merge(right=df_lang_detect,
                                                                                             on='base_path',
                                                                                             how='right')
# remove unnecessary rows of:
# - those that are detected to have English
# - those that have NaN in the `text` column
df_lang_detect = df_lang_detect.query('detected_as_english == "False"')
df_lang_detect = df_lang_detect.dropna(subset=['text'], axis='index')

# extract `primary_organisation_name`
df_lang_detect['primary_publishing_organisation'] = df_lang_detect['organisations'].apply(lambda x: extract_publishing_organisation(content_item=x,
                                                                                                                                    key='primary_publishing_organisation',
                                                                                                                                    index=1))

# select only relevant columns
df_lang_detect = df_lang_detect[['base_path',
                                 'primary_publishing_organisation',
                                 'publishing_app',
                                 'document_type',
                                 'text',
                                 'text_languages']]

# export
df_lang_detect.to_csv('data/non_english_page_report.csv')
