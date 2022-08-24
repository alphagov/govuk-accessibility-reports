import pytest


@pytest.fixture
def good_html():
    html = f"""
<html>
<head>
    <title>Good HTML</title>
</head>
<body>
    <h1>Heading 1</h1>
    <h2>heading 2</h2>
</body>
</html>
"""

    return html

@pytest.fixture
def wrong_start():
    html = f"""
<html>
<head>
    <title>Wrong Start</title>
</head>
<body>
<h2>Bad heading 2</h2>
</body>
</html>
"""

    return html

@pytest.fixture
def good_alt_tags():
    html = f"""
<html>
<head>
    <title>Good Alt Tags</title>
</head>
<body>
<img src="myimage.png" alt="Exterior view of Ministry of Silly Walks" />
</body>
</html>
"""

    return html

@pytest.fixture
def missing_alt_tags():
    html = f"""
<html>
<head>
    <title>Missing Alt Tags</title>
</head>
<body>
<img src="myimage.png" />
</body>
</html>
"""

    return html

@pytest.fixture
def empty_alt_tags():
    html = f"""
<html>
<head>
    <title>Empty Alt Tags</title>
</head>
<body>
<img src="myimage.png" alt=""/>
</body>
</html>
"""

    return html

@pytest.fixture
def double_quote_alt_tags():
    html = f"""
<html>
<head>
    <title>Double Quote Alt Tags</title>
</head>
<body>
<img src="myimage.png" alt="&quot;&quot;"/>
</body>
</html>
"""

    return html

@pytest.fixture
def filename_alt_tags():
    html = f"""
<html>
<head>
    <title>Filename Alt Tags</title>
</head>
<body>
<img src="myimage.png" alt="myimage.png"/>
</body>
</html>
"""

    return html
