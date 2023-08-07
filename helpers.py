from bs4 import Tag, NavigableString
from urllib.parse import urljoin


def build_url(endpoint: str) -> str:
    base = "https://www.addgene.org"
    return urljoin(base, endpoint)


# NOTE: these are helper functions to scrape primitive data

# TODO: add test for primitive data
def get_inner_string(tag: Tag) -> str:
    """ Get text enclosed by a tag, ignoring any other contained text.
    """
    for s in tag.children:
        if type(s) == NavigableString:
            return str(s).strip()

