from bs4 import Tag
from enum import Enum
from helpers import build_url
from scrapers.scraper import BaseScraper
from typing import List, Iterator, Tuple, Mapping


class FileType(Enum):
    """ Represents available sequence filetypes """
    SNAPGENE = 'snapgene'
    GENBANK = 'genbank'


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
        if self._get_files_list(self.soup) is not None:
            return True
        return False

    @staticmethod
    def _get_files_list(root: Tag) -> Iterator[Tag]:
        """ Get file list element.

        Returns
        `Tag` with file list element if page has sequence data

        Raises
        `ValueError` when downloaded page does not contain 'download-files-list' element
        """
        divs = root.find_all('div')
        if divs is None:
            raise ValueError('HTML does not contain \'download-files-list\' element')

        for div in divs:
            if 'id' in div.attrs.keys():
                if 'download-files-list' in div.attrs['id']:
                    yield div

    def _full_links(self, filetype: FileType) -> Mapping[SequenceType, List[str]]:
        # partition HTML sections for full sequences
        # each section represents sequence type. More than one link may be extracted.
        sections = {}
        for _type, section in self._sequence_sections():
            if _type is SequenceType.DEPOSITOR_FULL or _type is SequenceType.ADDGENE_FULL:
                sections[_type] = section

        # extract links from sections
        links = {}
        for _type, section in sections.items():
            _section_links = []
            sequences = self._get_files_list(section)
            for sequence in sequences:
                _link = _get_link_from_text(sequence, filetype.value)
                _section_links.append(_link)
            links[_type] = _section_links

        return links

    def _sequence_sections(self) -> Iterator[Tuple[SequenceType, Tag]]:
        terms = [
            ('depositor-full', SequenceType.DEPOSITOR_FULL),
            ('addgene-full', SequenceType.ADDGENE_FULL),
            ('depositor-partial', SequenceType.DEPOSITOR_PARTIAL),
            ('addgene-partial', SequenceType.ADDGENE_PARTIAL),
        ]
        for _id, _type in terms:
            element = self.soup.find('section', attrs={'id': _id})
            if element is not None:
                yield _type, element

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
    """ Get the link for an anchor element that contains the given text

    Example:
        tag = "<div><a href="example.com">first</a><a href="testing.com">second</'a>"
        assert _get_link_from_text(tag, 'first') == 'example.com'
        assert _get_link_from_text(tag, 'second') == 'testing.com'
    """
    for a in tag.find_all('a'):
        if text in a.text.lower():
            if 'href' in a.attrs.keys():
                return a.attrs['href']
            else:
                raise ValueError('\'a\' element has no href')
    raise ValueError(f'No element with \'{text}\' found')
