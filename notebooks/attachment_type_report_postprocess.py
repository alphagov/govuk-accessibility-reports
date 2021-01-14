import pandas as pd
import numpy as np
import swifter  # noqa: F401
from ast import literal_eval

df = pd.read_csv(filepath_or_buffer='data/attachment_type_report.csv')

n_govuk_pages = df.shape[0]
id_columns = list(df.columns)

# convert each element to dictionary
df["attachment_and_count"] = df["attachment_and_count"].swifter.apply(literal_eval)
# turn each key into column
df_attachments = pd.json_normalize(data=df["attachment_and_count"])
# identify pdf only attachments
col_names = list(df_attachments.columns)
col_names.remove(".pdf")
conditions = [df_attachments.loc[:, col_names].isnull().all(axis=1),
              df_attachments.loc[:, col_names].notnull().any(axis=1)]
choices = [True, False]
df_attachments["pdf_only"] = np.select(condlist=conditions,
                                       choicelist=choices,
                                       default=np.NaN)
df_attachments["pdf_only"] = df_attachments["pdf_only"].astype(bool)

# concat these two dfs together
df = pd.concat(objs=[df, df_attachments], axis=1)
del df_attachments, choices, col_names, conditions


# melt these attachment columns
id_columns.append("pdf_only")
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

# export to csv
df.to_csv(path_or_buf='data/attachment_type_report_process.csv',
          index=False)
