# base class for implementing parser

from bs4 import BeautifulSoup
from requests import get
from abc import ABC


class BaseScraper(ABC):
    def __init__(self, url: str):
        super().__init__()

        response = get(url)
        # TODO: CLEAN ALL `\n` from text
        self.soup = BeautifulSoup(response.text)

    # NOTE: there should be base scrapers for lists, and a tags to be reused in specific implementations
