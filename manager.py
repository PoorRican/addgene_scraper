from db import DbFileFetcher
from scrapers.plasmid import PlasmidScraper
from random import normalvariate
from os import mkdir, chdir, listdir
from typing import Union
from time import sleep
import re


# TODO: update function
class DbManager:
    path = "addgene_dump"
    # list of already downloaded plasmids
    local: list
    db: dict
    current: Union[None | str]

    def __init__(self):
        super().__init__()
        try:
            mkdir(self.path)
            print(f"Created directory '{self.path}'")
        except FileExistsError:
            print(f"Directory '{self.path}' exists")
            pass
        chdir(self.path)

        self.local = self._get_local()

    def load_db(self):
        fetcher = DbFileFetcher()
        self.db = fetcher.load()

    @staticmethod
    def _get_local() -> list:
        """ get the list already loaded plasmid id's.

        This is used to keep track of what plasmids have already been downloaded.

        Returns
        =======
        [int]
        list of already downloaded plasmid id's
        """
        local = []
        pattern = re.compile(r"plasmid_(\d.*)\.json")
        for fn in listdir('.'):
            matched = pattern.match(fn)
            if matched:
                local.append(matched.groups()[0])
        return local

    def _check_remaining(self) -> list:
        local = self._get_local()
        total = [i for i in self.db]
        return list(filter(lambda x: x['id'] not in local, total))

    def begin_dumping(self):
        print("Beginning to dump plasmid data...\n")
        print(f"...there are {len(self.db)} records...")
        remaining = self._check_remaining()
        print(f"...but we only have {len(remaining)} records left!")

        for i in remaining:
            endpoint = i['link']
            plasmid_id = i['id']
            if endpoint == '':
                endpoint = f'/vector-database/{plasmid_id}'

            wait = self._generate_wait()
            print(f"Waiting {wait} seconds before fetching {plasmid_id}")
            sleep(wait)
            print(f"Fetching {plasmid_id}")

            scraper = PlasmidScraper(endpoint)
            scraper.scrape()
            scraper.save(f"plasmid_{plasmid_id}.json")

    @staticmethod
    def _generate_wait() -> float:
        """ Generate a random time around 5 seconds to avoid any blanket protections """
        return normalvariate(5)


# get entire db as json
if __name__ == "__main__":
    client = DbManager()
    client.load_db()
    client.begin_dumping()
