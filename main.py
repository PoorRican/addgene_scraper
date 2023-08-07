from scrapers.plasmid import PlasmidScraper
from scrapers.query import QueryScraper
from random import normalvariate
from os import mkdir, chdir
from typing import Union
from time import sleep


# TODO: update function
# TODO: check currently installed. Report remaining, continue dumping.
class DumpClient:
    path = "addgene_dump"
    db: dict
    current: Union[None|str]

    def __init__(self):
        try:
            mkdir(self.path)
        except FileExistsError:
            pass
        chdir(self.path)
        self.db = self._get_db()
        # TODO: see if there are any downloaded objects to enable updating

    def begin_dumping(self):
        print("Beginning to dump plasmid data...\n")
        print(f"...there are {len(self.db)} records...")

        for i in self.db:
            wait = self.generate_wait()
            print(f"Waiting {wait} seconds")
            sleep(wait)
            _id = i['id']
            print(f"Fetching {_id}")
            scraper = PlasmidScraper(_id)
            scraper.scrape()
            scraper.save(f"plasmid_{_id}.json")

    @staticmethod
    def _get_db() -> dict:
        return QueryScraper().scrape()

    @staticmethod
    def generate_wait() -> float:
        """ Generate a random time around 5 seconds to avoid any blanket protections """
        return normalvariate(5)


# get entire db as json
if __name__ == "__main__":
    client = DumpClient()
    client.begin_dumping()
