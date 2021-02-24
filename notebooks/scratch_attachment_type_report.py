# script lays foundation code for `src/report_generators/attachment_type_report_generator.py`

from src.utils.constants import CONTENT_STORE_HEADER, CONTENT_STORE_DATE, ATTACHMENTS
from src.helpers.preprocess_text import extract_links_from_html, extract_from_path

import os
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter

DATA_DIR = os.getenv('DATA_DIR')
FILE_NAME = 'preprocessed_content_store_111120.csv.gz'

df = pd.read_csv(filepath_or_buffer=DATA_DIR + '/' + FILE_NAME,
                 compression='gzip',
                 encoding='utf-8',
                 sep='\t',
                 header=0,
                 names=list(CONTENT_STORE_HEADER.keys()),
                 dtype=CONTENT_STORE_HEADER,
                 parse_dates=CONTENT_STORE_DATE)

# drop empty rows
df_process = df.dropna(subset=['details'])

# take one page
test = df[df["base_path"] == "/government/publications/success-profiles"]
test = df[df["base_path"] == "/government/publications/screening-tests-for-you-and-your-baby"]
test = test['details'].iloc[0]
test = BeautifulSoup(test, features='lxml')
# get page links
page_links = [link.get('href') for link in test.find_all('a', href=True)]
page_attachments = extract_from_path(data=page_links, part='ext')
page_html = [html for html in page_links if html.startswith('/')]
# get valid attachments only
page_attachments = [x for x in page_attachments if x in ATTACHMENTS]
# get unique elements
page_html = list(set(page_html))
# add html links
page_attachments.extend(page_html)
# count repeated attachment elements in list
attachment_counts = dict(Counter(page_attachments))
# add html counts
attachment_counts.update({'html': len(page_html)})

# try using existing function
test = df[df["base_path"] == "/government/publications/success-profiles"]
test = test['details'].iloc[0]
extract_links_from_html(text=test)
test = BeautifulSoup(test, 'html5lib')
[link.get('href') for link in test.findAll(name='a', href=True)]

# smart answers
test = df[df["base_path"] == "/student-finance-forms"]
test = df[df["base_path"] == "/government/publications/measles-mumps-and-rubella-lab-confirmed-cases-in-england-2019"]
test = test['details'].iloc[0]
test = BeautifulSoup(test, features='lxml')
# get page links
page_links = [link.get('href') for link in test.find_all(name='a', href=True)]
page_attachments = extract_from_path(data=page_links, part='ext')
# remove empty elements
page_attachments = list(filter(None, page_attachments))
# take valid attachments
page_attachments = [x for x in page_attachments if x in ATTACHMENTS]
# count repeated attachment elements in list
attachment_counts = dict(Counter(page_attachments))
