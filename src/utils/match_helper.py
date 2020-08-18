from bs4 import BeautifulSoup
import re
import regex
from src.helpers.preprocess_text import extract_text
from collections import Counter


def unique_matches(matches):
    return list(set(matches))


def matcher(text, wording_regex):
    return [match[0] for match in regex.findall(wording_regex, text, re.IGNORECASE)]


def count_matches(matches):
    return Counter(matches)


def strip_calls(callout_pattern, text_clean):
    return re.sub(callout_pattern, "", text_clean)


def remove_bracketing(text):
    return re.sub(" +", " ", re.sub(r"\(|\)|\[|\]", r"", text.strip()).replace("\n", " "))


def preprocess_text(text):
    return remove_bracketing(extract_text(text))


def preprocess_regex(text):
    for c in r"\&+-=!":
        text = text.replace(c, f"{c}")
    return remove_bracketing(extract_text(text))


def compute_regex(text):
    soup = BeautifulSoup(text, "html.parser")
    items = list(soup.find_all("div", {'class': ['call-to-action']}))
    return "|".join([preprocess_regex(str(i)) for i in items])


def aggregate_callouts(text):
    soup = BeautifulSoup(text, "html.parser")
    items = list(soup.find_all("div", {'class': ['call-to-action']}))
    return [(" ".join(i.attrs['class']), preprocess_text(str(i))) for i in items]


def regex_match_callouts(callout_list, wording_regex):
    results = []
    for key, value in callout_list:
        if bool(regex.search(wording_regex, value, re.IGNORECASE)):
            results.extend(matcher(value, wording_regex))
    return results
