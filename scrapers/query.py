import datetime

from helpers import build_url
from selenium import webdriver
from selenium.webdriver.safari.options import Options
from datetime import datetime
import json


class QueryScraper:
    """ Scrapes vector database page to fetch entire vector database """
    data: dict

    @staticmethod
    def _url() -> str:
        return build_url('vector-database/query/?q_vdb=*')

    def scrape(self) -> dict:
        options = Options()
        options.page_load_strategy = 'normal'
        with webdriver.Safari(options=options) as wd:
            wd.get(self._url())
            self.data = wd.execute_script('return window.results.data')

        return self.data

    def save(self):
        """ Save current loaded data as JSON """
        if self.data is None:
            raise ValueError("Self data is None")
        else:
            fn = f"addgene_db_{datetime.now()}.json"
            with open(fn, 'w') as f:
                json.dump(self.data, f)
