from scrapers.scraper import BaseScraper
from helpers import build_url, get_inner_string


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
        for div in self.soup.find_all('div'):
            if 'id' in div.attrs.keys():
                if 'download-files-list' in div.attrs['id']:
                    return True
        return False

    @property
    def has_snapgene(self) -> bool:
        return False

    @property
    def has_genbank(self) -> bool:
        return False

    def get_snapgene(self) -> str:
        return NotImplemented

    def get_genbank(self) -> str:
        return NotImplemented
