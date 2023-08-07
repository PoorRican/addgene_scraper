from scrapers.query import QueryScraper
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        scraper = QueryScraper()
        data = scraper.scrape()
        self.assertGreaterEqual(len(data), 10572)


if __name__ == '__main__':
    unittest.main()
