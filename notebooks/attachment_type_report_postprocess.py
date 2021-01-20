from src.helpers.postprocess import get_attachment_percents

import pandas as pd
import swifter  # noqa: F401
from ast import literal_eval

df = pd.read_csv(filepath_or_buffer='data/attachment_type_report.csv')

id_columns = list(df.columns)

# convert each element to dictionary
df["attachment_and_count"] = df["attachment_and_count"].swifter.apply(literal_eval)
# turn each key into column
df_attachments = pd.json_normalize(data=df["attachment_and_count"])

# identify pdf-only and html-only attachments
# to see if reduction in pdf-only leads to rise in html-only
col_names = list(df_attachments.columns)

for attach in (".pdf", ".html"):
    # identify pdf-only attachments - fragile since relies on ".pdf" being first in tuple above
    if attach == ".pdf":
        col_names.remove(".pdf")
    # identify html-only attachments - fragile since relies on ".pdf" being first in tuple above
    elif attach == ".html":
        col_names.append(".pdf")
        col_names.remove(".html")

    # get
    new_col_name = attach + '_only'
    df_attachments[new_col_name] = df_attachments.loc[:, col_names].isnull().all(axis=1) & \
                                   df_attachments.loc[:, attach].notnull()  # noqa: E127

# concat these two dfs together
df = pd.concat(objs=[df, df_attachments], axis=1)
del df_attachments, col_names


# melt these attachment columns
id_columns = id_columns + [".pdf_only", ".html_only"]
df = pd.melt(frame=df,
             id_vars=id_columns,
             var_name='attachment_type',
             value_name='attachment_count')
# remove nas
df = df.dropna(subset=["attachment_count"])

# remove brackets in primary_publishing_organisation
df["primary_publishing_organisation"] = df["primary_publishing_organisation"].str.replace(pat=r'[\[\]]',
                                                                                          repl='')
# rename column to make it clearer this column is for QA purposes
df = df.rename(columns={"attachment_and_count": "qa_attachment_count"})

restrict_dates = ['2019-09-23', '2020-12-07']
# Report: Organisation ---
df_org = get_attachment_percents(df=df,
                                 index="primary_publishing_organisation")
df_org["date_coverage"] = "all"
df_org_restrict_dates = get_attachment_percents(df=df,
                                                index="primary_publishing_organisation",
                                                date=restrict_dates)
df_org_restrict_dates["date_coverage"] = ' to '.join(restrict_dates)
# Report: Document Types ---
df_doc = get_attachment_percents(df=df,
                                 index="document_type")
df_doc["date_coverage"] = "all"
df_doc_restrict_dates = get_attachment_percents(df=df,
                                                index="document_type",
                                                date=restrict_dates)
df_doc_restrict_dates["date_coverage"] = ' to '.join(restrict_dates)

# export to csv
files_save = {'attachment_type_org': df_org,
              'attachment_type_org_restrict_dates': df_org_restrict_dates,
              'attachment_type_doc': df_doc,
              'attachment_type_doc_restrict_dates': df_doc_restrict_dates}
[v.to_csv(path_or_buf='data/' + k + '.csv', index=False) for k, v in files_save.items()]
