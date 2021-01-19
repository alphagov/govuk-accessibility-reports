import pandas as pd
import swifter  # noqa: F401
from ast import literal_eval

df = pd.read_csv(filepath_or_buffer='data/attachment_type_report.csv')

n_govuk_pages = df.shape[0]
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

# inc total govuk pages
df["total_en_labelled_govuk_pages"] = n_govuk_pages

# arrange by base_path
df = df.sort_values(by=["base_path", "first_published_at", "attachment_type", "attachment_count"])

# Report: Organisation ---
df_org = df.value_counts(subset=["primary_publishing_organisation", "attachment_type"], sort=False)
df_org = df_org.reset_index()
df_totals = df.value_counts(subset=["primary_publishing_organisation"], sort=False)
df_totals = df_totals.reset_index()
df_org = df_org.merge(right=df_totals,
                      how='left',
                      on=["primary_publishing_organisation"],
                      validate="many_to_one")
df_org = df_org.rename(columns={"0_x": "counts_attachments",
                                "0_y": "total_pages"})
df_org["percentage_attachments"] = df_org["counts_attachments"] / df_org["total_pages"]
df_org = pd.pivot_table(data=df_org,
                        index=["primary_publishing_organisation"],
                        columns="attachment_type",
                        values="percentage_attachments").reset_index()
df_org = df_org.sort_values(by="primary_publishing_organisation")

# Report: Document Types ---
df_doc = df.value_counts(subset=["document_type", "attachment_type"], sort=False).reset_index()
df_totals = df.value_counts(subset=["document_type"], sort=False).reset_index()
df_doc = df_doc.merge(right=df_totals,
                      how='left',
                      on=["document_type"],
                      validate="many_to_one")
df_doc = df_doc.rename(columns={"0_x": "counts_attachments",
                                "0_y": "total_pages"})
df_doc["percentage_attachments"] = df_doc["counts_attachments"] / df_doc["total_pages"]
df_doc = pd.pivot_table(data=df_doc,
                        index=["document_type"],
                        columns="attachment_type",
                        values="percentage_attachments").reset_index()
df_doc = df_doc.sort_values(by="document_type")

# export to csv
df.to_csv(path_or_buf='data/attachment_type_report_process.csv',
          index=False)
