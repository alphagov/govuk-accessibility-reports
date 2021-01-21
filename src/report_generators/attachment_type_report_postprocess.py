from src.helpers.postprocess import get_attachment_counts_or_percents

import pandas as pd
import swifter  # noqa: F401
from ast import literal_eval

df_all = pd.read_csv(filepath_or_buffer='data/attachment_type_report.csv')

id_columns = list(df_all.columns)

# Reshape ---
# filter for whitehall and specialist publisher-only
df = df_all[df_all["publishing_app"].isin(["whitehall", "specialist"])].copy()

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

    # get attachment + '_only' entries
    new_col_name = attach + '_only'
    df_attachments[new_col_name] = df_attachments.loc[:, col_names].isnull().all(axis=1) & \
                                   df_attachments.loc[:, attach].notnull()  # noqa: E127

# concat horizontally these two dfs together
df = pd.concat(objs=[df.reset_index(), df_attachments], axis=1)
df = df.drop(columns="index")
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
df["primary_publishing_organisation"] = df["primary_publishing_organisation"].str.replace(pat=r'[\[\]]', repl='')
# rename column to make it clearer this column is for QA purposes
df = df.rename(columns={"attachment_and_count": "qa_attachment_count"})


# Report: Organisation and Document Type ---
# get reports along the following cuts:
#   i. Publishing organisation attachments for counts for all time
#   ii. Publishing organisation attachments for counts for restricted dates
#   iii. Publishing organisation attachments for percents for all time
#   iv. Publishing organisation attachments for percents for restricted dates
#   v. Document type attachments for counts for all time
#   vi. Document type attachments for counts for restricted dates
#   vii. Document type attachments for percents for all time
#   viii. Document type attachments for percents for restricted dates
filters = {"primary_publishing_organisation": ["counts", "percents"],
           "document_type": ["counts", "percents"]}
restrict_dates = ['2019-09-23', '2020-12-07']

df_list = list()
df_names_list = ['attachment_type_org_counts',
                 'attachment_type_org_restrict_dates_counts',
                 'attachment_type_org_percents',
                 'attachment_type_org_restrict_dates_percents',
                 'attachment_type_doc_counts',
                 'attachment_type_doc_restrict_dates_counts',
                 'attachment_type_doc_percents',
                 'attachment_type_doc_restrict_dates_percents']
for key, value in filters.items():
    for v in value:
        df_temp_all = get_attachment_counts_or_percents(df=df, index=key, values=v)
        df_temp_all["date_coverage"] = "all"
        df_temp_restrict = get_attachment_counts_or_percents(df=df, index=key, values=v, date=restrict_dates)
        df_temp_restrict["date_coverage"] = ' to '.join(restrict_dates)
        df_list.append(df_temp_all)
        df_list.append(df_temp_restrict)

del df_temp_all, df_temp_restrict, id_columns, key, value, filters, restrict_dates, attach, new_col_name

# export to csv
files_save = dict(zip(df_names_list, df_list))
[v.to_csv(path_or_buf='data/' + k + '.csv', index=False) for k, v in files_save.items()]
