import unittest
from helpers import build_url
from scrapers.sequence import SequenceScraper

EXAMPLES = (
    '/128041/sequences/#addgene-full',
)


class SequenceScraperTests(unittest.TestCase):
    def test_default_url(self):
        for endpoint in EXAMPLES:
            scraper = SequenceScraper(endpoint)
            self.assertEqual(scraper.url, build_url(endpoint))

    def test_has_snapgene(self):
        endpoint = EXAMPLES[0]
        scraper = SequenceScraper(endpoint)
        self.assertTrue(scraper.has_snapgene)  # add assertion here

    def test_has_genbank(self):
        endpoint = EXAMPLES[0]
        scraper = SequenceScraper(endpoint)
        self.assertTrue(scraper.has_genbank)  # add assertion here

    def test_is_sequence_page(self):
        endpoint = EXAMPLES[0]
        scraper = SequenceScraper(endpoint)
        self.assertTrue(scraper._is_sequence_page())  # add assertion here

    def test_get_snapgene(self):
        endpoint = EXAMPLES[0]
        scraper = SequenceScraper(endpoint)
        with open('files/128041.snap') as f:
            self.assertEqual(f.read(), scraper.get_snapgene())

    def test_get_genbank(self):
        endpoint = EXAMPLES[0]
        scraper = SequenceScraper(endpoint)
        with open('files/128041.gbk') as f:
            self.assertEqual(f.read(), scraper.get_genbank())


if __name__ == '__main__':
    unittest.main()
