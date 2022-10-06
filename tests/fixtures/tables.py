import pytest

good_table_string = f"""
    <p>Good table</p>
    <table>
        <thead>
            <tr>
                <th></th>
                <th>Name</th>
                <th>Role</th>
                <th>Base</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <th scope="row">Founder</th>
                <td>Batman</td>
                <td>VENG<br />EANCE</td>
                <td>Gotham</td>
            </tr>
            <tr>
                <th scope="row">First son</th>
                <td>Robin</td>
                <td>Partner</td>
                <td>Bludhaven</td>
            </tr>
            <tr>
                <th scope="row">Replacement</th>
                <td>Robin 2</td>
                <td>Dead one</td>
                <td>Pit</td>
            </tr>
        </tbody>
    </table>
"""

bad_table_string = f"""
    <p>Bad table</p>
    <table>
        <tr>
            <td>Name</td>
            <td>Role</td>
        </tr>
        <tr>
            <th scope="row">Superman</td>
            <td>Himbo</td>
        </tr>
        <tr>
          <td>Flash</td>
          <td>Speedster</td>
        </tr>
    </table>
"""

bad_table_missing_row_scope_string = f"""
    <p>Bad table missing row scope</p>
    <table>
        <tbody>
        <tr>
            <th scope="row">Name</td>
            <th>Role</td>
        </tr>
        <tr>
            <th scope="row">Superman</td>
            <td>Himbo</td>
        </tr>
        <tr>
            <th>Flash</td>
            <td>Speedster</td>
        </tr>
        </tbody>
    </table>
"""

bad_table_missing_row_th_string = f"""
    <p>Bad table missing row th</p>
    <table>
        <tbody>
        <tr>
            <th scope="row">Name</td>
            <th>Role</td>
        </tr>
        <tr>
            <th scope="row">Superman</td>
            <td>Himbo</td>
        </tr>
        <tr>
            <td>Flash</td>
            <td>Speedster</td>
        </tr>
        </tbody>
    </table>
"""

two_tables_string ="""
    <table><tr><td>1</td></tr></table>
    <table><tr><td>2</td></tr></table>
"""

good_table_mention_string="""
    <table><thead><tr><th>Expected</th></tr></thead><tbody><tr><td>1</td></tr></tbody></table>
    <p>The table shows the data expected</p>
"""

bad_table_mention_string="""
    <p>The table shows the data expected</p>
    <a href="whatever">Hello</a>
"""

missing_table_mention_string="""
    <p>by putting food on your table!</p>
"""


@pytest.fixture
def good_table():
    return good_table_string

@pytest.fixture
def bad_table():

    return bad_table_string

@pytest.fixture
def bad_table_missing_row_scope():
    return bad_table_missing_row_scope_string

@pytest.fixture
def bad_table_missing_row_th():
    return bad_table_missing_row_th_string

@pytest.fixture
def two_tables():
    return two_tables_string

@pytest.fixture
def good_table_mention():
    return good_table_mention_string

@pytest.fixture
def bad_table_mention():
    return bad_table_mention_string

@pytest.fixture
def missing_table_mention():
    return missing_table_mention_string

@pytest.fixture
def html():
    html = f"""
<html>
<head>
    <title>Tables</title>
</head>
<body>
{good_table_string}
{bad_table_string}
</body>
</html>
"""

    return html
