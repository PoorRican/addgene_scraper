import unittest

from scrapers.plasmid import PlasmidScraper

# TODO: "Tag/Fusion Protein" does not parse correctly
EXPECTED = {
    '128041': {
        'Vector backbone': {'value': 'pBABE puro', 'href': '/vector-database/query/?q_vdb=pBABE%20puro'},
        'Vector type': {'value': 'Mammalian Expression, Retroviral', 'href': None},
        'Bacterial Resistance(s)': {'value': 'Ampicillin, 100 μg/mL', 'href': None},
        'Growth Temperature': {'value': '37°C', 'href': None},
        'Growth Strain(s)': {'value': 'NEB Stable', 'href': None},
        'Copy number': {'value': 'High Copy', 'href': None},
        'Gene/Insert name': {'value': 'None', 'href': None},
        'Tag/ Fusion Protein': {'value': ['EGFP (N terminal on backbone)'], 'href': None},
        'Purpose': {'value': '(Empty Backbone)Retroviral vector with N terminal EGFP', 'href': None},
        'Depositing Lab': {'value': 'Oskar Laur', 'href': '/browse/pi/4513/'},
        'Publication': {'value': 'Emory Custom Cloning Core Plasmids - Oskar Laur (unpublished)',
                        'href': '/browse/article/28203582/'},
        'Sequence Information': {'value': [{'value': 'Sequences (1)', 'href': '/128041/sequences/'}]},
        'Article Citing this Plasmid': {'value': ['1 Reference'], 'href': '/128041/citations/'},
        'Academic/Nonprofit Terms': {'value': ['UBMTA', 'Ancillary Agreement for Plasmids Containing FP Materials'],
                                     'href': '/agreement/1/'},
        'Industry Terms': {'value': ['Not Available to Industry'], 'href': None},
     }
}


class PlasmidPageTests(unittest.TestCase):
    def test_parse_page(self):
        # TODO: the tests for checking keys (both ways), and checking values should be split into multiple tests.
        #  However, GET requests should be executed on the class level ONCE and not per test.
        for plasmid_id, expected in EXPECTED.items():
            scraper = PlasmidScraper(plasmid_id)
            parsed = scraper.scrape()
            for key, value in expected.items():
                self.assertTrue(parsed[key], f"Scraped values did not contain {key}")
                self.assertEqual(parsed[key], expected[key], f"Values don't match for {key}")  # add assertion here
            # also fail if key is not expected (meaning incomplete implementation)
            for key in parsed.keys():
                self.assertTrue(key in expected.keys(), f"Expected value does not contain {key}: {parsed[key]}")


if __name__ == '__main__':
    unittest.main()
