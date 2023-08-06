# Functor that parses a plasmid pageb
from scrapers.scraper import BaseScraper
from helpers import build_url, get_inner_string


class PlasmidScraper(BaseScraper):
    def __init__(self, plasmid_id: str):
        url = build_url(plasmid_id)
        super().__init__(url)

    def _scrape_desc(self) -> {}:
        return {}

    def _scrape_details(self) -> {}:
        # get detail section
        raw = self.soup.find(attrs={'id': 'detail-sections'})
        details = {}

        # avoid getting pricing data
        ignore = ["ordering"]

        sections = raw.find_all_next('section')
        for section in sections:
            title = section.find(attrs={'class': 'title'})
            if title is None or title.text.strip().lower() in ignore:
                continue
            else:           # extract detail fields
                fields = {}
                for field_element in section.find_all(attrs={'class': 'field'}):
                    key = field_element.find(attrs={'class': 'field-label'}).text
                    value = get_inner_string(field_element)

                    # try extracting an array
                    if value is None:
                        element = field_element.find(attrs={'class': "addgene-document-list"})
                        if element:
                            value = [i.text for i in element.children]

                    # attempt to grab the href
                    a = field_element.find('a')
                    if a:
                        href = a.attrs['href'].strip()
                    else:
                        href = None

                    fields[key] = {'value': value, 'href': href}
                details.update(fields)

        return details

    def scrape(self) -> {}:
        plasmid = dict()
        plasmid.update(self._scrape_details())
        plasmid.update(self._scrape_desc())
        return plasmid
