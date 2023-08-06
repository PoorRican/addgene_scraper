import unittest
from requests import get

from helpers import build_url

# TODO: "Tag/Fusion Protein" does not parse correctly
EXPECTED = {
    '128041': {
        'Vector backbone': {'value': 'pBABE puro', 'href': '/vector-database/query/?q_vdb=pBABE%20puro'},
        'Vector type': {'value': 'Mammalian Expression, Retroviral', 'href': None},
        '/ Fusion Protein': {'value': [], 'href': None},
        'Bacterial Resistance(s)': {'value': 'Ampicillin, 100 μg/mL', 'href': None},
        'Growth Temperature': {'value': '37°C', 'href': None},
        'Growth Strain(s)': {'value': 'NEB Stable', 'href': None},
        'Copy number': {'value': 'High Copy', 'href': None},
        'Gene/Insert name': {'value': 'None', 'href': None},
        'Tag/ Fusion Protein': {'value': [], 'href': None},
        'Purpose': {'value': '(Empty Backbone)Retroviral vector with N terminal EGFP', 'href': None},
        'Depositing Lab': {'value': 'Oskar Laur', 'href': '/browse/pi/4513/'},
        'Publication': {'value': 'Emory Custom Cloning Core Plasmids - Oskar Laur (unpublished)',
                        'href': '/browse/article/28203582/'},
        'Sequence Information': {'value': [{'value': 'Sequences (1)', 'href': '/128041/sequences/'}]}
     }
}


class PlasmidPageTests(unittest.TestCase):
    def test_parse_page(self):
        for key, expected in EXPECTED:
            response = get(build_url(key))
            parsed = get_plasmid(response)
            self.assertEqual(expected, parsed)  # add assertion here


if __name__ == '__main__':
    unittest.main()
