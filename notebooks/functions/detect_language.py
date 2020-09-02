import numpy as np
from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException


def detect_language(text):
    """Detects language of a text, moving onto next text if an error is thrown

    :param text: A string to detect the language of
    :return: A list returning the language detected and confidence score associated to it

    """

    try:
        return detect_langs(text)
    except LangDetectException:
        return np.NaN
