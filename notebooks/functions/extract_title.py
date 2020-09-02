import ast


def extract_title(text):
    """Extracts all the attachment titles from GOV.UK pages

    :param html: String of the HTML code for the GOV.UK page being passed in
    :return: list of all the attachment titles that were extracted from GOV.UK page

    """
    text = ast.literal_eval(text)
    text = text.get('attachments')

    titles = list(map(lambda x: x['title'], text))

    return titles
