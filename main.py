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

        for i in self._plasmid_ids():
            wait = self._generate_wait()
            print(f"Waiting {wait} seconds before fetching {i}")
            sleep(wait)
            print(f"Fetching {i}")
            scraper = PlasmidScraper(i)
            scraper.scrape()
            scraper.save(f"plasmid_{i}.json")

    @staticmethod
    def generate_wait() -> float:
        """ Generate a random time around 5 seconds to avoid any blanket protections """
        return normalvariate(5)

    def _plasmid_ids(self):
        """ Generator for iterating through a list of plasmid ids """
        pattern = re.compile(r"/(\d*)/")
        for i in self.db:
            link = i['link']
            matched = pattern.search(link)
            if matched:
                yield matched.groups()[0]


# get entire db as json
if __name__ == "__main__":
    client = DumpClient()
    client.begin_dumping()
