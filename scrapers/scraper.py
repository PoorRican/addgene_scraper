# base class for implementing parser

from bs4 import BeautifulSoup
from requests import get
from abc import ABC


def clean_all_newlines(raw: str) -> str:
    """ Deletes any newlines and cleans up excess whitespace """
    split = raw.splitlines(False)
    stripped = [i.strip() for i in split]
    return ''.join(stripped)


class BaseScraper(ABC):
    def __init__(self, url: str):
        super().__init__()
        self.url = url

        # TODO: constructors shouldn't call blocking function
        response = get(url)
        cleaned = clean_all_newlines(response.text)
        self.soup = BeautifulSoup(cleaned, features="html.parser")
