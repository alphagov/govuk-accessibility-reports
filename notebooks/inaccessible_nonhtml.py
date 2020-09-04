import pandas as pd

from notebooks.functions.main import get_links
from notebooks.functions.main import extract_filename
from notebooks.functions.main import extract_publishing_organisation


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
