import unittest
from helpers import build_url
from scrapers.sequence import SequenceScraper
from bs4 import Tag

EXAMPLES = (
    '/128041/sequences/#addgene-full',
)


class SequenceScraperTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.scrapers = [(i, SequenceScraper(i)) for i in EXAMPLES]

    def test_default_url(self):
        for link, scraper in self.scrapers:
            self.assertEqual(scraper.url, build_url(link))

    def test_has_snapgene(self):
        _, scraper = self.scrapers[0]
        self.assertTrue(scraper.has_snapgene)  # add assertion here

    def test_has_genbank(self):
        _, scraper = self.scrapers[0]
        self.assertTrue(scraper.has_genbank)  # add assertion here

    def test_get_file_list(self):
        _, scraper = self.scrapers[0]
        self.assertTrue(type(scraper._get_file_list()), Tag)  # add assertion here

    def test_is_sequence_page(self):
        _, scraper = self.scrapers[0]
        self.assertTrue(scraper._is_sequence_page())  # add assertion here

    def test_get_snapgene(self):
        _, scraper = self.scrapers[0]
        with open('files/128041.snap') as f:
            self.assertEqual(f.read(), scraper.get_snapgene())

    def test_get_genbank(self):
        _, scraper = self.scrapers[0]
        with open('files/128041.gbk') as f:
            self.assertEqual(f.read(), scraper.get_genbank())


if __name__ == '__main__':
    unittest.main()
