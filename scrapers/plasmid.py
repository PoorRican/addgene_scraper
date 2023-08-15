# Functor that parses a plasmid page
import re

from scrapers.scraper import BaseScraper
from helpers import build_url, get_inner_string
from bs4 import Tag
import json


class PlasmidScraper(BaseScraper):
    data: dict

    def __init__(self, plasmid_id: str):
        url = build_url(plasmid_id)
        super().__init__(url)

    def _scrape_desc(self) -> {}:
        fields = {}

        raw = self.soup.find(attrs={'id': 'plasmid-description-list'})
        for field in raw.find_all('div', attrs={'class': 'field'}):
            label = field.find(attrs={'class': 'field-label'}).text

            _content = field.find(attrs={'class': 'field-content'})

            # try extracting an array
            if _content is None:
                element = field.find('ul')
                if element:
                    values = []
                    for i in element.children:
                        href = i.find('a').attrs['href']
                        values.append({'value': i.text, 'href': href})
                    fields[label] = {'value': values}

            else:
                # try extracting a link
                a = _content.find('a')
                if a:
                    value = a.text
                    href = str(a['href'])
                else:
                    value = _content.text
                    href = None
                fields[label] = {'value': value, 'href': href}
        return fields

    def _scrape_details(self) -> {}:
        # get detail section
        raw = self.soup.find(attrs={'id': 'detail-sections'})
        if raw is None:
            print(self.soup.text)
            raise ValueError(f'URL ({self.url}) did not resolve to plasmid')
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
        if self._is_available():
            plasmid.update(self._scrape_details())
            plasmid.update(self._scrape_desc())
        else:
            plasmid = self._extract_limited()
        self.data = plasmid
        return plasmid

    def save(self, path: str):
        with open(path, 'w') as f:
            json.dump(self.data, f)

    def _is_available(self) -> bool:
        """ Check if current plasmid is available from AddGene.

        Example: /vector-database/1403

        If plasmid is not available from AddGene, there is only a limited amount of data to be extracted.

        Returns
        =======
        false page states that plasmid is not available on AddGene,
        otherwise, `true`
        """
        try:
            main = self.soup.find(attrs={'id': 'main-content'})
            danger = main.find(attrs={'class': 'alert-danger'})
            # this alert-danger element should say that vector is not available on addgene
            assert 'NOT available' in danger.text
            return False
        except (AttributeError, AssertionError):
            return True

    def _extract_limited(self) -> {}:
        """ Extract data from a plasmid id that is not available from addgene.

        This is called when `_is_available()` is `False`
        """
        data = {}
        main = self.soup.find(attrs={'id': 'main-content'})

        # get name
        _name = main.find('h2').text
        _pattern = re.compile('Plasmid: (.*)')
        data['Plasmid'] = _pattern.match(_name).groups()[0]

        table = main.find('table')
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            label = cells[0].text[:-1]      # truncate last character
            value = cells[1]

            # if value is Tag, then extract link
            a = value.find('a')
            if a:
                value = {'href': a.attrs['href'], 'label': a.text}
            else:
                value = value.text

            data[label] = value

        return data
