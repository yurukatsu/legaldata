import re
from typing import List, Literal, NewType, Optional, TypeAlias

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from legaldata.formatter import format_url
from legaldata.loader import BaseLink, BaseLoader, get_content

SESCHoudouCategories: List[str] = ["kinshou", "hukousei", "kaiji", "others"]
SESCHoudouCategory: TypeAlias = Literal["kinshou", "hukousei", "kaiji", "others"]


class SESCHoudouLink(BaseLink):
    """
    Link to SESC Houdou.
    """

    description: str = "SESC報道"
    category: str = "SESC"
    name: str = "SESC報道"
    extension: str = "html"
    preprocessed: bool = Field(default=False, description="Preprocessed", exclude=False)
    yyyy: int = Field(description="年", exclude=False)
    houdou_category: SESCHoudouCategory = Field(description="カテゴリ", exclude=False)


class SESCHoudouLoader(BaseLoader):
    """
    Loader for SESC Houdou.
    """

    start_url: str = "https://www.fsa.go.jp/sesc/houdou"
    url_template: str = "https://www.fsa.go.jp/sesc/houdou/{yyyy}{category}.html"
    format_base_url: str = "https://www.fsa.go.jp"

    def __init__(self, yyyy: int, category: SESCHoudouCategory) -> None:
        """
        Args:
            yyyy (int): year
            category (SESCHoudouCategory):
                category. One of "kinshou" (金融商品取引業関係),
                "hukousei" (不公正取引関係), "kaiji" ("開示規制違反関係"),
                "others" (年次好評等).
        """
        self.__yyyy = yyyy
        self.__category: SESCHoudouCategory = category
        self.years = self._get_available_years()

    def _get_available_years(self) -> List[int]:
        """
        Get available years.
        """
        content = get_content(self.start_url)
        soup = BeautifulSoup(content, "html.parser")
        selector = "h3.layout-3"
        text_pattern = r"\d{4}"
        return [
            int(re.search(text_pattern, e.text).group()) for e in soup.select(selector)
        ]

    @property
    def yyyy(self) -> int:
        """
        Get year.
        """
        if self.__yyyy not in self.years:
            raise ValueError(f"year must be one of {self.years}.")
        return self.__yyyy

    @yyyy.setter
    def yyyy(self, yyyy: int) -> None:
        """
        Set year.

        Args:
            yyyy (int): year
        """
        self.__yyyy = yyyy

    @property
    def category(self) -> SESCHoudouCategory:
        """
        Get category.
        """
        if self.__category not in SESCHoudouCategories:
            raise ValueError(
                "category must be one of 'kinshou', 'hukousei', 'kaiji', 'others'."
            )
        return self.__category

    @category.setter
    def category(self, category: SESCHoudouCategory) -> None:
        """
        Set category.

        Args:
            category (SESCHoudouCategory):
                category. One of "kinshou" (金融商品取引業関係),
                "hukousei" (不公正取引関係), "kaiji" ("開示規制違反関係"),
                "others" (年次好評等).
        """
        self.__category = category

    @property
    def url(self) -> str:
        """
        Get URL.
        """
        return self.url_template.format(yyyy=self.yyyy, category=self.category)

    def get_links(self) -> List[SESCHoudouLink]:
        """
        Get links to data.
        """
        content = get_content(self.url)
        soup = BeautifulSoup(content, "html.parser")
        selector = "div#main li"
        return [
            SESCHoudouLink(
                url=format_url(e.find("a").get("href"), self.format_base_url),
                yyyy=self.yyyy,
                houdou_category=self.category,
                description=e.text,
            )
            for e in soup.select(selector)
        ]
