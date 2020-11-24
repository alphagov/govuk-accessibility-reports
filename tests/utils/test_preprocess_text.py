from src.helpers.preprocess_text import extract_html_tag


def test_extract_html_tag(html_text):
    strong_text = [extract_html_tag(text=txt, name='strong') for txt in html_text['raw']]
    assert strong_text == html_text['strong']
