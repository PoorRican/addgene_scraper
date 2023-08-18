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

# these urls seem like they will eventually become invalid
SNAPGENE_SEQUENCE_LINKS = (
    {
        SequenceType.ADDGENE_FULL: [
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/254994/508acc8c-7d0f-4ca5-9f19'
            '-6f41a8e215a1/addgene-plasmid-128041-sequence-254994.dna'
        ]
    },
    {
        SequenceType.DEPOSITOR_FULL: [
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/108431/2caf23fb-5f75-4a9a-9650'
            '-495f56119387/addgene-plasmid-45789-sequence-108431.dna',
        ],
        SequenceType.ADDGENE_PARTIAL: [
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/67198/6d25587f-25a6-4830-a6c5'
            '-ae2865247e8a/addgene-plasmid-45789-sequence-67198.dna',
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/67201/54e728d4-3350-4d8c-b397'
            '-cbd11f92e8b7/addgene-plasmid-45789-sequence-67201.dna',
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/67202/24edfa33-5b44-4688-ba36'
            '-c68a0b71aec1/addgene-plasmid-45789-sequence-67202.dna',
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/67203/cab7b1b0-d3d8-4a03-a940'
            '-de8eab5011ef/addgene-plasmid-45789-sequence-67203.dna',
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/67643/6cc29437-4840-4379-9db5'
            '-23cd1556fa85/addgene-plasmid-45789-sequence-67643.dna',
        ]
    }
)
GENBANK_SEQUENCE_LINKS = (
    {
        SequenceType.ADDGENE_FULL: [
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/254994/508acc8c-7d0f-4ca5-9f19'
            '-6f41a8e215a1/addgene-plasmid-128041-sequence-254994.gbk'
        ]
    },
    {
        SequenceType.DEPOSITOR_FULL: [
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/108431/2caf23fb-5f75-4a9a-9650'
            '-495f56119387/addgene-plasmid-45789-sequence-108431.gbk',
        ],
        SequenceType.ADDGENE_PARTIAL: [
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/67198/6d25587f-25a6-4830-a6c5'
            '-ae2865247e8a/addgene-plasmid-45789-sequence-67198.gbk',
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/67201/54e728d4-3350-4d8c-b397'
            '-cbd11f92e8b7/addgene-plasmid-45789-sequence-67201.gbk',
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/67202/24edfa33-5b44-4688-ba36'
            '-c68a0b71aec1/addgene-plasmid-45789-sequence-67202.gbk',
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/67203/cab7b1b0-d3d8-4a03-a940'
            '-de8eab5011ef/addgene-plasmid-45789-sequence-67203.gbk',
            'https://media.addgene.org/snapgene-media/v1.7.9-0-g88a3305/sequences/67643/6cc29437-4840-4379-9db5'
            '-23cd1556fa85/addgene-plasmid-45789-sequence-67643.gbk',
        ]
    }
)


class SequenceScraperTests(unittest.TestCase):
    scrapers: ClassVar[List[SequenceScraper]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.scrapers = [SequenceScraper(i) for i in EXAMPLES]

    def test_default_url(self):
        for link, scraper in zip(EXAMPLES, self.scrapers):
            self.assertEqual(scraper.url, build_url(link))

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
        for scraper, expected in zip(self.scrapers, SNAPGENE_SEQUENCE_LINKS):
            self.assertEqual(expected, scraper._snapgene_link())

    def test_genbank_link(self):
        for scraper, expected in zip(self.scrapers, GENBANK_SEQUENCE_LINKS):
            self.assertEqual(expected, scraper._genbank_link())

    def test_get_genbank(self):
        scraper = self.scrapers[0]
        with open('files/addgene-plasmid-128041-sequence-254994.gbk', 'rb') as f:
            self.assertEqual(f.read(), scraper.get_genbank())


if __name__ == '__main__':
    unittest.main()
