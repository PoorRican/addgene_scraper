import unittest
from helpers import build_url
from scrapers.sequence import SequenceScraper
from scrapers.sequence import SequenceType
from typing import ClassVar, List
from bs4 import Tag

EXAMPLES = (
    '/128041/sequences/',
    '/45789/sequences/'
)

SEQUENCE_AVAILABILITIES = (
    [SequenceType.ADDGENE_FULL],
    [SequenceType.DEPOSITOR_FULL, SequenceType.ADDGENE_PARTIAL]
)


class SequenceScraperTests(unittest.TestCase):
    scrapers: ClassVar[List[SequenceScraper]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.scrapers = [SequenceScraper(i) for i in EXAMPLES]

    def test_default_url(self):
        for link, scraper in zip(EXAMPLES, self.scrapers):
            self.assertEqual(scraper.url, build_url(link))

    def test_has_snapgene(self):
        scraper = self.scrapers[0]
        self.assertTrue(scraper.has_snapgene)  # add assertion here

    def test_has_genbank(self):
        scraper = self.scrapers[0]
        self.assertTrue(scraper.has_genbank)  # add assertion here

    def test_get_file_list(self):
        scraper = self.scrapers[0]
        self.assertTrue(type(scraper._get_file_list()), Tag)  # add assertion here

    def test_is_sequence_page(self):
        scraper = self.scrapers[0]
        self.assertTrue(scraper._is_sequence_page())  # add assertion here

    def test_available_sequences(self):
        for scraper, expected in zip(self.scrapers, SEQUENCE_AVAILABILITIES):
            self.assertEqual(scraper.available_sequences(), expected)

    def test_get_snapgene(self):
        scraper = self.scrapers[0]
        with open('files/addgene-plasmid-128041-sequence-254994.dna', 'rb') as f:
            self.assertEqual(f.read(), scraper.get_snapgene())

    def test_snapgene_link(self):
        scraper = self.scrapers[0]
        # this url seems like it will expire
        url = ('https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/254994/508acc8c-7d0f-4ca5-9f19'
               '-6f41a8e215a1/addgene-plasmid-128041-sequence-254994.dna')
        self.assertEqual(url, scraper._snapgene_link())

    def test_genbank_link(self):
        scraper = self.scrapers[0]
        # this url seems like it will expire
        url = ("https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/254994/508acc8c-7d0f-4ca5-9f19"
               "-6f41a8e215a1/addgene-plasmid-128041-sequence-254994.gbk")
        self.assertEqual(url, scraper._genbank_link())

    def test_get_genbank(self):
        scraper = self.scrapers[0]
        with open('files/addgene-plasmid-128041-sequence-254994.gbk', 'rb') as f:
            self.assertEqual(f.read(), scraper.get_genbank())


if __name__ == '__main__':
    unittest.main()
