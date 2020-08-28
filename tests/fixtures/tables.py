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
                <td>VENGEANCE</td>
                <td>Gotham</td>
            </tr>
            <tr>
                <th>First son</th>
                <td>Robin</td>
                <td>Partner</td>
                <td>Bludhaven</td>
            </tr>
            <tr>
                <th>Replacement</th>
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
            <td>Superman</td>
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
        <tr>
            <th>Name</td>
            <th>Role</td>
        </tr>
        <tr>
            <th>Superman</td>
            <td>Himbo</td>
        </tr>
        <tr>
          <td>Flash</td>
          <td>Speedster</td>
        </tr>
    </table>
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
