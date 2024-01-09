from typing import List

from bs4 import BeautifulSoup

from legaldata.formatter import format_url
from legaldata.loader import BaseLink, BaseLoader, get_content


class JSDALink(BaseLink):
    description: str = "JSDA協会規約"
    category: str = "JSDA"
    name: str = "JSDA協会規約"
    extension: str = "pdf"


class JSDALoader(BaseLoader):
    """
    Loader for JSDA.
    """

    __url: str = "https://www.jsda.or.jp/about/kisoku"

    @property
    def url(self) -> str:
        """
        Get URL.
        """
        return self.__url

    @url.setter
    def url(self, url: str) -> None:
        """
        Set URL.

        Args:
            url (str): URL
        """
        self.__url = url

    def get_links(self) -> List[JSDALink]:
        """
        Get links to data.
        """
        content = get_content(self.url)
        soup = BeautifulSoup(content, "html.parser")
        elements = soup.find_all("a", href=lambda href: href and href.endswith(".pdf"))
        return [
            JSDALink(url=format_url(element.get("href"), self.url))
            for element in elements
        ]
