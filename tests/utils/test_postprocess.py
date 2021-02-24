from src.helpers.postprocess import get_attachment_counts_or_percents


def test_get_attachment_percents(df_attachments_long, df_attachments_wide):
    df_wide = get_attachment_counts_or_percents(df=df_attachments_long,
                                                index='organisation',
                                                values='percents')
    df_wide = df_wide.rename_axis(None, axis=1)
    assert df_wide.equals(df_attachments_wide)
