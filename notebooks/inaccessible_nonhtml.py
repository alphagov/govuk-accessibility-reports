import pandas as pd
import numpy as np

import os
import ast
import json
from bs4 import BeautifulSoup


# function to extract links from HTML
def get_links(text):
    list_links = []
    soup = BeautifulSoup(text, "html.parser")
    for a in soup.find_all('a', href=True):
        link = a['href']
        list_links.append(link)
    return list_links


# function to extract filename from HTML
def extract_filename(list_text):
    """Extracts the last part of a URL path string, including the file name and extension

    :param list: A list of strings to extract last part from, e.g. everything after '/'
    :return: A list of the same length as list_text, but with the last parts kept e.g. everything after '/'

    """
    file_name = [os.path.split(text)[1] for text in list_text]
    return file_name


# function to extract titles
def extract_title(text):
    """Extracts all the attachment titles from GOV.UK pages

    :param html: String of the HTML code for the GOV.UK page being passed in
    :return: list of all the attachment titles that were extracted from GOV.UK page

    """
    text = ast.literal_eval(text)
    text = text.get('attachments')

    titles = list(map(lambda x: x['title'], text))

    return titles


# function to extract from list nested in HTML
def extract_publishing_organisation(content_item, key, index=0):
    """ Extracts the value of a key within a dictionary masquerading as a string

    :param content_item: A string that's in the format of a dictionary
    :param key: The name of the key you want to extract the associated value from
    :param index: The index of specific value if you extracted more than one value from the key
    :return: the extracted value of the key
    """
    try:
        # convert object to string
        content_item = json.dumps(content_item)
        # convert string to object
        content_item = json.loads(content_item)

        # convert to dictionary
        organisations = ast.literal_eval(content_item)

        # extract value of key entered from dictionary
        organisations = list(map(lambda org: org[index], organisations.get(key, {})))

        return organisations
    except (ValueError, SyntaxError):
        return [np.NaN]


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

# report should contain following columns:
#   - base_path
#   - pubishing_app (mainstream(?), service-manual-publisher, specialist-publisher, travel-advice-publisher)
#   - organisations
#   - attachment file + extension (from details)
#   - first_published_at
#   - public_updated_at
#   - updated_at

del dict_header, list_header_date

# select only relevant columns
df_output = df[['base_path',
                'organisations',
                'publishing_app',
                'document_type',
                'first_published_at',
                'public_updated_at',
                'updated_at',
                'details']].copy()

# parameter for all GOV.UK file attachments to identify
file_attachment = (".chm|.csv|.diff|.doc|.docx|.dot|.dxf|.eps|"
                   + ".gif|.gml|.ics|.jpg|.kml|.odp|.ods|.odt|.pdf|"
                   + ".png|.ppt|.pptx|.ps|.rdf|.ris|.rtf|.sch|.txt|"
                   + ".vcf|.wsdl|.xls|.xlsm|.xlsx|.xlt|.xml|.xsd|.xslt|"
                   + ".zip")

# filter pages with attachments on them
df_output['attachment_exists'] = df_output['details'].str.contains(file_attachment, na=False)
df_output = df_output.query('attachment_exists == True')

# extract attachment - fairly slow, consider SoupStrainer and multiprocessing
df_output['hyperlinks'] = df_output['details'].apply(get_links)
df_output['attachments'] = df_output['hyperlinks'].apply(extract_filename)

# have non-attachments in output
# suggests we are not identifying attachments in line with part when we filter

# get primary_publishing_organisation
df_output['primary_publishing_organisation'] = df_output['organisations'].apply(lambda x: extract_publishing_organisation(content_item=x,
                                                                                                                          key='primary_publishing_organisation',
                                                                                                                          index=1))

# export to .csv for Accessibility team
df_filter = df_output.query('publishing_app == ["publisher", "service-manual-publisher", "specialist-publisher", "travel-advice-publisher"]')
df_filter[['base_path',
           'primary_publishing_organisation',
           'publishing_app',
           'document_type',
           'first_published_at',
           'public_updated_at',
           'updated_at',
           'attachments']].to_csv(path_or_buf='data/inaccessible_nonhtml_report.csv', index=False)
