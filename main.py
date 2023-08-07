from scrapers.plasmid import PlasmidScraper
from db import DbDump
from random import normalvariate
from os import mkdir, chdir, listdir
from typing import Union
from time import sleep
import json
import re
from datetime import datetime
from datetime import timedelta as td


# TODO: update function
# TODO: check currently installed. Report remaining, continue dumping.
class DumpClient:
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
        # TODO: see if there are any downloaded objects to enable updating

    def load_db(self):
        """ Loads database file.

        Database is loaded using `DbDump().scrape()` if a recent cached version database is unavailable.
        """
        # get fn for latest local db
        latest = self._get_local_db()
        if latest is False or self._is_stale(latest[0]):
            print("Downloading current database")
            obj = DbDump()
            self.db = obj.scrape()
            obj.save('.')
            print("... database saved to disk.")
        else:
            with open(str(latest[1]), "r") as f:
                self.db = json.load(f)

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
        total = [i for i in self._plasmid_ids()]
        return list(filter(lambda x: x not in local, total))

    def begin_dumping(self):
        print("Beginning to dump plasmid data...\n")
        print(f"...there are {len(self.db)} records...")
        remaining = self._check_remaining()
        print(f"...but we only have {len(remaining)} records left!")

        for i in remaining:
            wait = self._generate_wait()
            print(f"Waiting {wait} seconds before fetching {i}")
            sleep(wait)
            print(f"Fetching {i}")
            scraper = PlasmidScraper(i)
            scraper.scrape()
            scraper.save(f"plasmid_{i}.json")

    @staticmethod
    def _generate_wait() -> float:
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

    @staticmethod
    def _is_stale(latest: datetime):
        return (latest - datetime.now()) > td(days=7)


# get entire db as json
if __name__ == "__main__":
    client = DumpClient()
    client.load_db()
    client.begin_dumping()
