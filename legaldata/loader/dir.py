from typing import List, Literal, TypeAlias, Union

from bs4 import BeautifulSoup
from pydantic import Field

from legaldata.formatter import format_url
from legaldata.loader import BaseLink, BaseLoader, get_content
from legaldata.loader.base import BaseLink


class DIRReportSiteLink(BaseLink):
    """
    Link to Daiwa Institute of Research (DIR) site.
    """

    description: str = "大和総研レポート"
    category: str = "大和総研"
    name: str = "大和総研レポート"
    extension: str = "html"
    keyword: str = Field(description="キーワード", exclude=False)
    sub_keyword: str = Field(description="サブキーワード", exclude=False)


class DIRReportLink(BaseLink):
    """
    Link to Daiwa Institute of Research (DIR) data.
    """

    description: str = "大和総研レポート"
    category: str = "大和総研"
    name: str = "大和総研レポート"
    extension: str = "pdf"


DIRReportKeywords: List[str] = [
    "policy-analysis",
    "economics",
    "capital-mkt",
    "law-research",
    "introduction",
]

DIRReportKeyword: TypeAlias = Literal[
    "policy-analysis",
    "economics",
    "capital-mkt",
    "law-research",
    "introduction",
]

DIRReportLawResearchSubKeywords: List[str] = [
    "securities",
    "law-others",
    "tax",
]

DIRReportLawResearchSubKeyword: TypeAlias = Literal[
    "securities",
    "law-others",
    "tax",
]

DIRReportSubKeyword: TypeAlias = DIRReportLawResearchSubKeyword


class DIRReportLoader(BaseLoader):
    """
    Loader for Daiwa Institute of Research (DIR) data.
    """

    base_url: str = "https://www.dir.co.jp"
    url_template: str = (
        "https://www.dir.co.jp/report/research/{keyword}/{sub_keyword}/{yyyy}.html"
    )

    def __init__(
        self,
        keyword: DIRReportKeyword = "law-research",
        sub_keyword: DIRReportSubKeyword = "securities",
        yyyy: int = 2024,
    ) -> None:
        """
        Args:
            keyword (DIRReportKeyword, optional): keyword. Defaults to "law-research".
            sub_keyword (DIRReportSubKeyword, optional): sub-keyword. Defaults to "securities".
            yyyy (int, optional): yyyy. Defaults to 2024.
        """
        self.__keyword = keyword
        if keyword != "law-research":
            raise NotImplementedError("Only law-research is supported.")
        self.__sub_keyword = sub_keyword
        self.yyyy = yyyy

    @property
    def keyword(self) -> DIRReportKeywords:
        """
        Get keyword.
        """
        return self.__keyword

    @keyword.setter
    def keyword(self, keyword: DIRReportKeyword) -> None:
        assert isinstance(keyword, DIRReportKeyword)
        if keyword != "law-research":
            raise NotImplementedError("Only law-research is supported.")
        self.__keyword = keyword

    @property
    def sub_keyword(self) -> DIRReportSubKeyword:
        return self.__sub_keyword

    @sub_keyword.setter
    def sub_keyword(self, sub_keyword: DIRReportSubKeyword) -> None:
        assert isinstance(sub_keyword, DIRReportSubKeyword)
        self.__sub_keyword = sub_keyword

    @property
    def yyyy(self) -> int:
        return self.__yyyy

    @yyyy.setter
    def yyyy(self, yyyy: int) -> None:
        self.__yyyy = yyyy

    @property
    def url(self):
        return self.url_template.format(
            keyword=self.keyword,
            sub_keyword=self.sub_keyword,
            yyyy=self.yyyy,
        )

    def _get_report_site_links(self) -> List[DIRReportSiteLink]:
        content = get_content(self.url)
        soup = BeautifulSoup(content, "html.parser")
        selector = "#main div li a.c-newsList-link"
        urls = [e.get("href") for e in soup.select(selector)]
        return [
            DIRReportSiteLink(
                url=format_url(url, self.base_url),
                keyword=self.keyword,
                sub_keyword=self.sub_keyword,
            )
            for url in urls
        ]

    @classmethod
    def get_pdf_links(cls, site_links: DIRReportSiteLink) -> List[DIRReportLink]:
        pdf_links = []
        for site_link in site_links:
            content = get_content(site_link.url)
            soup = BeautifulSoup(content, "html.parser")
            selector = "div#contents div.wrp-main-inner div.mod-btn-file.-left.-reportPdf.-emphasis a"
            # get pdf url
            url = soup.select(selector)[0].get("href")
            url = format_url(url, cls.base_url)
            pdf_links.append(
                DIRReportLink(
                    url=url,
                    keyword=site_link.keyword,
                    sub_keyword=site_link.sub_keyword,
                )
            )
        return pdf_links

    def get_links(self) -> List[DIRReportLink]:
        site_links = self._get_report_site_links()
        return self.get_pdf_links(site_links)
