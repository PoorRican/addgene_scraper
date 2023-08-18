from bs4 import Tag
from enum import Enum
from helpers import build_url
from scrapers.scraper import BaseScraper
from typing import List, Iterator, Tuple


class SequenceType(Enum):
    ADDGENE_FULL = 'addgene_full'
    ADDGENE_PARTIAL = 'addgene_partial'
    DEPOSITOR_FULL = 'depositor_full'
    DEPOSITOR_PARTIAL = 'depositor_partial'


class SequenceScraper(BaseScraper):
    """ Download associated GenBank / SnapGene file from sequences page on plasmid page """

    def __init__(self, endpoint: str):
        """ Create scraper class from sequence URL """
        super().__init__(build_url(endpoint))

    def _is_sequence_page(self) -> bool:
        """ Helper function to detect if page is for vector sequence data

        Returns
        `True` if page contains correct links
        `False` if page is incorrect
        """
        if self._get_file_list() is not None:
            return True
        return False

    def _get_file_list(self) -> Tag:
        """ Get file list element.

        Returns
        `Tag` with file list element if page has sequence data

        Raises
        `ValueError` when downloaded page does not contain 'download-files-list' element
        """
        for div in self.soup.find_all('div'):
            if 'id' in div.attrs.keys():
                if 'download-files-list' in div.attrs['id']:
                    return div
        raise ValueError('HTML does not contain \'download-files-list\' element')

    def _sequence_sections(self) -> Iterator[Tuple[SequenceType, Tag]]:
        terms = [
            ('depositor-full', SequenceType.DEPOSITOR_FULL),
            ('addgene-full', SequenceType.ADDGENE_FULL),
            ('depositor-partial', SequenceType.DEPOSITOR_PARTIAL),
            ('addgene-partial', SequenceType.ADDGENE_PARTIAL),
        ]
        for _id, _type in terms:
            yield _type, self.soup.find('section', attrs={'id': _id})

    def available_sequences(self) -> List[SequenceType]:
        """ Show available sequence types for given plasmid

        Although some plasmids may have more than one partial sequence, only one `SequenceType` is returned
        regardless of the amount of sequences. For example [this plasmid](https://www.addgene.org/45789/sequences/)
        has one full sequence from depositor and 5 partial sequences by AddGene. However, only `[ADDGENE_PARTIAL,
        DEPOSITOR_FULL]` is returned.
        """
        available = []
        for _type, element in self._sequence_sections():
            if element is not None:
                available.append(_type)
        return available


def _get_link_from_text(tag: Tag, text: str) -> str:
    """ Get the link for an anchor element that contains the given text """
    for a in tag.find_all('a'):
        if text in a.text.lower():
            if 'href' in a.attrs.keys():
                return a.attrs['href']
            else:
                raise ValueError('\'a\' element has no href')
    raise ValueError(f'No element with \'{text}\' found')

