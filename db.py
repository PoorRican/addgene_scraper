import datetime
from datetime import datetime
from datetime import timedelta as td
from helpers import build_url
import json
from os import listdir
import re
from selenium import webdriver
from selenium.webdriver.safari.options import Options
from typing import Union


class DbFileFetcher:
    """ Dump entire vector database.

    The entire AddGene database is loaded in the browser when rendering any page.
    The database is stored in the DOM as `window.results.data`.

    This class uses a webdriver from Selenium to fetch the loaded data. This process is manual and slow.
    Therefore, functions will be provided that determine if this database is stale, and a locally, cached version will
    be loaded when a copy of the AddGene db is needed.
    """
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

    def save(self, path: str):
        """ Save current loaded data as JSON """
        if self.data is None:
            raise ValueError("Self data is None")
        else:
            fn = f"{path}/addgene_db_{datetime.now()}.json"
            with open(fn, 'w') as f:
                json.dump(self.data, f)

    def load(self):
        """ Loads database file.

        Database is loaded using `DbFileFetcher().scrape()` if a recent cached version database is unavailable.
        """
        # get fn for latest local db
        latest = self._get_local_db()
        if latest is False or self._is_stale(latest[0]):
            print("Downloading current database")
            self.scrape()
            self.save('.')
            print("... database saved to disk.")
            return self.data
        else:
            with open(str(latest[1]), "r") as f:
                return json.load(f)

    @staticmethod
    def _get_local_db() -> Union[False, tuple[datetime, str]]:
        pattern = re.compile(r"addgene_db_(.*)\.json")
        cached = []
        for fn in listdir('.'):
            matched = pattern.match(fn)
            if matched:
                cached.append(matched.group())

        if len(cached) == 0:
            return False
        else:
            latest_date = datetime.fromtimestamp(0)
            fn = None
            for i in cached:
                frag = pattern.match(i)
                date = datetime.fromisoformat(frag.groups()[0])
                if date > latest_date:
                    latest_date = date
                    fn = i
            return latest_date, fn

    @staticmethod
    def _is_stale(latest: datetime):
        return (latest - datetime.now()) > td(days=7)
