from bs4 import Tag
from scrapers.scraper import BaseScraper
from helpers import build_url, get_inner_string
from requests import get


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

    @property
    def has_snapgene(self) -> bool:
        try:
            self._snapgene_link()
            return True
        except ValueError:
            return False

    @property
    def has_genbank(self) -> bool:
        try:
            self._genbank_link()
            return True
        except ValueError:
            return False

    def _genbank_link(self) -> str:
        """ Return URL to download GenBank file """
        e = self._get_file_list()
        return _get_link_from_text(e, 'genbank')

    def _snapgene_link(self) -> str:
        """ Return URL to download SnapGene file """
        e = self._get_file_list()
        return _get_link_from_text(e, 'snapgene')

    def get_snapgene(self) -> bytes:
        response = get(self._snapgene_link())
        return response.content

    def get_genbank(self) -> bytes:
        response = get(self._genbank_link())
        return response.content

    def available_sequences(self) -> list:
        """ Show available sequences for given plasmid """
        return []


def _get_link_from_text(tag: Tag, text: str) -> str:
    """ Get the link for an anchor element that contains the given text """
    for a in tag.find_all('a'):
        if text in a.text.lower():
            if 'href' in a.attrs.keys():
                return a.attrs['href']
            else:
                raise ValueError('\'a\' element has no href')
    raise ValueError(f'No element with \'{text}\' found')

