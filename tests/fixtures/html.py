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
