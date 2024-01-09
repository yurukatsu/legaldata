import warnings
from typing import List, Literal, Optional, TypeAlias
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from legaldata.formatter import format_url
from legaldata.loader import BaseLink, BaseLoader, get_content


class FSAPublicCommentLink(BaseLink):
    description: str = "金融庁（FSA）パブリックコメント"
    category: str = "FSA"
    name: str = "FSAパブリックコメント"
    extension: str = "pdf"
    publish_date: str = Field(description="公表日", exclude=False)
    project_name: str = Field(description="案件名", exclude=False)


class FSAPublicComment(BaseModel):
    date: str = Field(description="公表日")
    pj_name: Optional[str] = Field(description="案件名")
    pj_name_url: Optional[str] = Field(description="案件名のURL")
    deadline: Optional[str] = Field(description="締め切り日")
    etc: Optional[str] = Field(description="備考")
    etc_url: Optional[str] = Field(description="備考のURL")


class FSAPublicCommentLoader(BaseLoader):
    """
    Loader for FSA Public Comment data.
    """

    base_url: str = "https://www.fsa.go.jp"

    def __init__(self, yyyy: int) -> None:
        """
        Args:
            yyyy (int): year (>= 2000 and <= 2100)
        """
        self.__yyyy = yyyy
        self.__url_template = "https://www.fsa.go.jp/public/{yyyy}.html"

    @property
    def url(self) -> str:
        """
        Get URL.
        """
        return self.__url_template.format(yyyy=self.__yyyy)

    @property
    def yyyy(self) -> int:
        """
        Get year.
        """
        return self.__yyyy

    @yyyy.setter
    def yyyy(self, yyyy: int) -> None:
        """
        Set year.

        Args:
            yyyy (int): year (>= 2000 and <= 2100)
        """
        if yyyy < 2000:
            raise ValueError("Year must be greater than or equal to 2000.")
        if yyyy > 2100:
            raise ValueError("Year must be less than or equal to 2100.")
        self.__yyyy = yyyy

    def get_public_comments(self) -> List[FSAPublicComment]:
        """
        Get list of public comment.
        """
        content = get_content(self.url)
        soup = BeautifulSoup(content, "html.parser")
        # search elements
        css_selector = "div#main tbody tr"
        trs = soup.select(css_selector)
        results = []
        for i, tr in enumerate(trs):
            tds = tr.find_all("td")
            try:
                date = tds[0].text
                if pj := tds[1].find("a"):
                    pj_name = pj.text
                    pj_name_url = format_url(pj.get("href"), self.base_url)
                else:
                    pj_name = tds[1].text
                    pj_name_url = None
                deadline = tds[2].text
                if e := tds[3].find("a"):
                    etc = e.text
                    etc_url = format_url(e.get("href"), self.base_url)
                else:
                    etc = tds[3].text
                    etc_url = None
                results.append(
                    FSAPublicComment(
                        date=date,
                        pj_name=pj_name,
                        pj_name_url=pj_name_url,
                        deadline=deadline,
                        etc=etc,
                        etc_url=etc_url,
                    )
                )
            except Exception as e:
                warnings.warn(f"process {i} is failed because that {e}. skip it.")
        return results

    def get_links(self, public_comment: FSAPublicComment) -> List[FSAPublicCommentLink]:
        """
        Get links to data.

        Args:
            public_comment: public comment data.

        Returns:
            list of links.
        """
        content = get_content(public_comment.pj_name_url)
        soup = BeautifulSoup(content, "html.parser")
        elements = soup.find_all("a", href=lambda href: href and href.endswith(".pdf"))
        return [
            FSAPublicCommentLink(
                url=format_url(element.get("href"), self.base_url),
                publish_date=public_comment.date,
                project_name=public_comment.pj_name,
            )
            for element in elements
        ]


class FSANewsLink(BaseLink):
    description: str = "金融庁（FSA）ニュース"
    category: str = "FSA"
    name: str = "FSAニュース"
    extension: str = "html"
    year: int = Field(description="年", exclude=False)


class FSANewsLoader(BaseLoader):
    """
    Loader for FSA News data.
    """

    base_url: str = "https://www.fsa.go.jp"

    def __init__(self, yyyy: int) -> None:
        self.__yyyy = yyyy

    @property
    def yyyy(self) -> int:
        """
        Get year.

        Returns:
            int: year.
        """
        return self.__yyyy

    @yyyy.setter
    def yyyy(self, yyyy: int) -> None:
        """
        Set year.

        Args:
            yyyy (int): year.
        """
        self.__yyyy = yyyy

    def _convert_to_japanese_calendar(self, yyyy: str) -> str:
        """
        Convert to Japanese calendar.

        Args:
            yyyy (str): year.

        Returns:
            str: Japanese calendar.
        """
        if yyyy >= 2019:
            return f"r{yyyy - 2018}"
        else:
            return str(yyyy - 1988)

    @property
    def year_jp(self) -> str:
        """
        Get Japanese calendar.

        Returns:
            str: Japanese calendar.
        """
        return self._convert_to_japanese_calendar(self.yyyy)

    @property
    def url(self) -> str:
        """
        Get URL.
        """
        url = urljoin(self.base_url, f"news/{self.year_jp}_news_menu.html")
        if requests.get(url).status_code != 200:
            url = urljoin(self.base_url, f"news/index.html")
        return url

    def get_links(self) -> List[FSANewsLink]:
        """
        Get links to data.

        Returns:
            list of links.
        """
        content = get_content(self.url)
        soup = BeautifulSoup(content, "html.parser")
        selector = "div#main div.inner ul li a"
        elements = soup.select(selector)
        return [
            FSANewsLink(
                url=format_url(element.get("href"), self.base_url),
                year=self.yyyy,
                description=element.text,
            )
            for element in elements
        ]
