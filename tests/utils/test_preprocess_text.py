from src.helpers.preprocess_text import extract_text_from_html


def test_extract_text_from_html(html_text):
    strong_text = [extract_text_from_html(text=txt, name='strong') for txt in html_text['raw']]
    assert strong_text == html_text['strong']
