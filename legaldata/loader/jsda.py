from typing import Dict, List

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from legaldata.formatter import format_url
from legaldata.loader import BaseLink, BaseLoader, get_content
from legaldata.loader.base import BaseLink


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


JSDAHandbookCategoryIDName: Dict[str, str] = {
    "101": "kanri",
    "102": "jyugyoin",
    "103": "koukoku",
    "104": "kojin-jyoho",
    "105": "kabushiki",
    "106": "saiken",
    "107": "foreign",
    "108": "syoukenka",
    "109": "deri",
    "110": "rinri",
    "201": "kansyuu",
    "202": "hunsou",
    "203": "rijikai",
    "204": "seido",
    "301": "hourei",
    "302": "eigyo",
}

JSDAHandbookCategoryIDDescription: Dict[str, str] = {
    "101": "協会員における顧客管理、内部管理等",
    "102": "従業員、外務員関係",
    "103": "広告関係",
    "104": "個人情報関係",
    "105": "株式関係",
    "106": "債券関係",
    "107": "外国証券・取引関係",
    "108": "証券化商品関係",
    "109": "デリバティブ関係",
    "110": "倫理コード関係",
    "201": "統一慣習規則（※２）",
    "202": "紛争処理規則（※３）",
    "203": "理事会決議（※４）等",
    "204": "制度",
    "301": "法令等の解釈に関するＱ＆Ａ・ガイドライン等",
    "302": "営業ルール照会制度",
}


class JSDAHandbookLink(BaseLink):
    description: str = "JSDAハンドブック"
    category: str = "JSDA"
    name: str = "JSDAハンドブック"
    extension: str = "pdf"
    type_name: str = Field(description="文書の種類")
    type_desc: str = Field(description="文書の種類の説明")
    title: str = Field(description="文書のタイトル")


JSDAHandbookTypes: Dict[str, str] = {}


class JSDAHandbookLoader(BaseLoader):
    jsda_base_url: str = "https://www.jsda.or.jp"
    base_url: str = "https://www.jsda.or.jp/shijyo/seido/jishukisei/web-handbook"

    def __init__(self, type_id: str = "101"):
        self.__type_id = type_id

    @property
    def type_id(self) -> str:
        """
        Get type id.
        """
        if self.__type_id not in JSDAHandbookCategoryIDName:
            raise ValueError(f"Invalid type id: {self.__type_id}")
        return self.__type_id

    @type_id.setter
    def type_id(self, type_id: str) -> None:
        """
        Set type id.

        Args:
            type_id (str): Type id.
        """
        self.__type_id = type_id

    @property
    def type_name(self) -> str:
        """
        Get type name.
        """
        return JSDAHandbookCategoryIDName[self.type_id]

    @property
    def type_description(self) -> str:
        """
        Get type description.
        """
        return JSDAHandbookCategoryIDDescription[self.type_id]

    @property
    def url(self) -> str:
        """
        Get URL.
        """
        return f"{self.base_url}/{self.type_id}_{self.type_name}"

    def _get_links_less_than_300(self) -> List[JSDAHandbookLink]:
        content = get_content(self.url)
        soup = BeautifulSoup(content, "html.parser")
        selector = "table.web-handbook li a"
        elements = soup.select(selector)

        def _format_url(url: str) -> str:
            if url.startswith("/about"):
                return format_url(url, self.jsda_base_url)
            else:
                return format_url(url, self.url)

        return [
            JSDAHandbookLink(
                title=element.get_text(),
                url=_format_url(element.get("href")),
                type_name=self.type_name,
                type_desc=self.type_description,
            )
            for element in elements
        ]

    def _get_links_over_300(self) -> List[JSDAHandbookLink]:
        content = get_content(self.url)
        soup = BeautifulSoup(content, "html.parser")
        selector = "div.jsda_table01 table a"
        elements = soup.select(selector)

        def _format_url(url: str) -> str:
            if url.startswith("/about"):
                return format_url(url, self.jsda_base_url)
            else:
                return format_url(url, self.url)

        return [
            JSDAHandbookLink(
                title=element.get_text(),
                url=_format_url(element.get("href")),
                type_name=self.type_name,
                type_desc=self.type_description,
            )
            for element in elements
        ]

    def get_links(self) -> List[BaseLink]:
        if int(self.type_id) < 300:
            return self._get_links_less_than_300()
        else:
            return self._get_links_over_300()
