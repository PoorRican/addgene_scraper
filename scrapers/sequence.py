from bs4 import Tag
from enum import Enum
from helpers import build_url
from requests import get
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
        if _get_files_list(self.soup) is not None:
            return True
        return False

    def get_best(self, filetype: FileType) -> bytes:
        """ Get best available sequence

        Returns
        The best available SnapGene or Genbank file is returned.

        See Also
        [`SequenceScraper.best_sequence`]
        """
        response = get(self.best_sequence(filetype))
        return response.content

    def best_sequence(self, filetype: FileType) -> str:
        """ Get the link to the best available sequence.

        Returns
        The best available full sequence is returned. The depositor's full sequence takes priority over AddGene's
        sequences.

        Raises
        If there are no full sequences available, an error is returned.
        """
        links = self._full_links(filetype)
        for sequence in (SequenceType.DEPOSITOR_FULL, SequenceType.ADDGENE_FULL):
            if sequence in links.keys():
                # there is usually only one full sequence, so return the first available
                return links[sequence][0]

    def _has_full_sequence(self) -> bool:
        """ Check to see if there is a full sequence available.

        Returns
        `True` if there are full sequences available
        `False` if there are no full sequences available
        """
        # checking both for assurance
        if self._full_links(FileType.GENBANK) == {} and self._full_links(FileType.SNAPGENE) == {}:
            return False
        return True

    def _full_links(self, filetype: FileType) -> Mapping[SequenceType, List[str]]:
        # partition HTML sections for full sequences
        # each section represents sequence type. More than one link may be extracted.
        sections = {}
        for _type, section in self._sequence_sections():
            if _type is SequenceType.DEPOSITOR_FULL or _type is SequenceType.ADDGENE_FULL:
                sections[_type] = section

        return _extract_links_from_sections(sections, filetype)

    def _partial_links(self, filetype: FileType) -> Mapping[SequenceType, List[str]]:
        # partition HTML sections for full sequences
        # each section represents sequence type. More than one link may be extracted.
        sections = {}
        for _type, section in self._sequence_sections():
            if _type is SequenceType.DEPOSITOR_PARTIAL or _type is SequenceType.ADDGENE_PARTIAL:
                sections[_type] = section

        return _extract_links_from_sections(sections, filetype)

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


def _extract_links_from_sections(sections: Mapping[SequenceType, Tag], filetype: FileType):
    links = {}
    for _type, section in sections.items():
        _section_links = []
        sequences = _get_files_list(section)
        for sequence in sequences:
            _link = _get_link_from_text(sequence, filetype.value)
            _section_links.append(_link)
        links[_type] = _section_links

    return links
