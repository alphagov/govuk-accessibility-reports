import pytest
import pandas as pd
import numpy as np


@pytest.fixture()
def df_attachments_long():
    return pd.DataFrame(data={'base_path': ['a', 'a', 'b', 'c'],
                              'organisation': ['Foo', 'Foo', 'Bar', 'Foo'],
                              'attachment_type': ['.html', '.pdf', '.csv', '.xml'],
                              'attachment_count': [2, 3, 1, 1]})


@pytest.fixture()
def df_attachments_wide():
    return pd.DataFrame(data={'organisation': ['Bar', 'Foo'],
                              '.csv': [1, np.NaN],
                              '.html': [np.NaN, 1/3],
                              '.pdf': [np.NaN, 1/3],
                              '.xml': [np.NaN, 1/3]})
