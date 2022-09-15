# Helps extract HTML/Govspeak from the mismash string content item details
# that is being passed to the report generators
#
# To use, first get the content details, then you can pass that to one
# of the xxx_from_content_details methods:
#
# from src.utils.content_item_details import content_details, html_from_content_details
# cd = content_item_details(content_item)
# html = html_from_content_details(cd)
#
# (html is just the html of the content item, can be parsed with BeautifulSoup)
#

def content_item_details(content_item):
    return eval(content_item['details'])

def format_from_content_details_body(body, content_type) -> str:
    if type(body) == str:
        return body
    content = [f['content'] for f in body if f['content_type'] == content_type]
    if len(content) == 0:
        return None
    else:
        return content[0]

def html_from_content_details(details) -> str:
    body = format_from_content_details_body(details['body'], 'text/html')
    if 'documents' in details and len(details['documents']) > 0:
        body += details['documents'][0]
    return body

def govspeak_from_content_details(details) -> str:
    return format_from_content_details_body(details['body'], 'text/govspeak')
