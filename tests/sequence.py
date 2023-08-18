import unittest
from helpers import build_url
from scrapers.sequence import SequenceScraper, FileType
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
FULL_SNAPGENE_LINKS = (
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
    }
)

PARTIAL_SNAPGENE_LINKS = (
    {},
    {
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

FULL_GENBANK_LINKS = (
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
    }
)

PARTIAL_GENBANK_LINKS = (
    {},
    {
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

    def test_best_sequence(self):
        for scraper, expected in zip(self.scrapers, FULL_GENBANK_LINKS):
            self.assertEqual([i for i in expected.values()][0][0], scraper.best_sequence(FileType.GENBANK))
        for scraper, expected in zip(self.scrapers, FULL_SNAPGENE_LINKS):
            self.assertEqual([i for i in expected.values()][0][0], scraper.best_sequence(FileType.SNAPGENE))

    def test_has_full_sequence(self):
        for scraper in self.scrapers:
            self.assertTrue(scraper._has_full_sequence())

    def test_full_links(self):
        # test genbank
        for scraper, expected in zip(self.scrapers, FULL_GENBANK_LINKS):
            self.assertEqual(scraper._full_links(FileType.GENBANK), expected)

        # test snapgene
        for scraper, expected in zip(self.scrapers, FULL_SNAPGENE_LINKS):
            self.assertEqual(scraper._full_links(FileType.SNAPGENE), expected)

    def test_is_sequence_page(self):
        scraper = self.scrapers[0]
        self.assertTrue(scraper._is_sequence_page())  # add assertion here

    def test_available_sequences(self):
        for scraper, expected in zip(self.scrapers, SEQUENCE_AVAILABILITIES):
            self.assertEqual(scraper.available_sequences(), expected)


if __name__ == '__main__':
    unittest.main()
