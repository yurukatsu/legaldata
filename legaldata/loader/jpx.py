import json
import os
import re
from typing import List

from bs4 import BeautifulSoup, ResultSet, Tag
from pydantic import BaseModel, Field

from legaldata.formatter import extract_text, format_url
from legaldata.loader import BaseLink, BaseLoader, get_content


class JPXRuleLink(BaseLink):
    description: str = "JPX定款等諸規則／諸規則内規"
    category: str = "JPX"
    name: str = "JPX定款等諸規則／諸規則内規"
    extension: str = "html"
    preprocessed: bool = Field(default=False, description="Preprocessed", exclude=False)


class JPXRuleLoader(BaseLoader):
    """
    Loader for JPX Rules.
    """

    __url: str = "https://jpx-gr.info"

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

    def get_links(self) -> List[JPXRuleLink]:
        """
        Get links to data.
        """
        content = get_content(self.url)
        soup = BeautifulSoup(content, "html.parser")
        elements = soup.select("dd a")
        return [
            JPXRuleLink(url=format_url(element.get("href"), self.url))
            for element in elements
        ]

    @classmethod
    def save_text(cls, link: JPXRuleLink, filename: str) -> None:
        """
        Download data from URL and extract text.

        Args:
            link (BaseLink): Link to data.
            filename (str): Filename of data.
        """
        try:
            with open(filename, "wb") as f:
                content = get_content(link.url)
                extracted_text = extract_text(content).encode("utf-8")
                f.write(extracted_text)
        except Exception as e:
            raise e

    @classmethod
    def save_text_w_metadata(
        cls,
        link: BaseLink,
        save_dir: str,
        filename: str = "content",
        metadata_name: str = "metadata",
    ) -> None:
        """
        Extract data from downloaded data from URL with metadata.

        Args:
            link (BaseLink): Link to data.
            save_dir (str): Directory to save data.
            filename (str, optional): Filename of data w/o extension. Defaults to "content".
            metadata_name (str, optional): Filename of metadata. Defaults to "metadata".
        """
        if os.path.exists(save_dir) is False:
            os.makedirs(save_dir)
        try:
            with open(os.path.join(save_dir, f"{filename}.txt"), "wb") as f:
                content = get_content(link.url)
                extracted_text = extract_text(content).encode("utf-8")
                f.write(extracted_text)
            with open(os.path.join(save_dir, f"{metadata_name}.json"), "w") as f:
                link.extension = "txt"
                link.preprocessed = True
                json.dump(link.__dict__, f, ensure_ascii=False, indent=4)
        except Exception as e:
            raise e


class JPXPublicComment(BaseModel):
    """
    Data class for public comment.
    """

    date: str = Field(description="公表日", exclude=False)
    pj_name: str = Field(description="案件名", exclude=False)
    pj_name_url: str = Field(description="案件名のURL", exclude=True)
    deadline: str = Field(default=None, description="締め切り日", exclude=True)
    corporation: str = Field(default=None, description="法人名", exclude=True)


class JPXPublicCommentLink(BaseLink):
    """
    Link class for public comment.
    """

    description: str = "日本取引所グループ（JPX）パブリックコメント"
    category: str = "JPX"
    name: str = "JPXパブリックコメント"
    extension: str = "pdf"
    publish_date: str = Field(description="公表日", exclude=False)
    project_name: str = Field(description="案件名", exclude=False)


class JPXPublicCommentLoader(BaseLoader):
    """
    Loader for FSA Public Comment data.
    """

    base_url: str = "https://www.jpx.co.jp"

    def __init__(self, yyyy: int) -> None:
        """
        Args:
            yyyy (int): year (>= 2006 and <= latest)
        """
        self.__yyyy = yyyy
        self.__url_template = (
            "https://www.jpx.co.jp/rules-participants/public-comment/{index}.html"
        )
        self.years = self._get_years()
        self.max_yyyy = max(self.years)
        self.table_css_selector = "div.component-normal-table table"

    def _get_years(self) -> List[int]:
        """
        Get years.
        """
        url = "https://www.jpx.co.jp/rules-participants/public-comment/"
        content = get_content(url)
        soup = BeautifulSoup(content, "html.parser")
        return [
            int(year)
            for year in soup.select("select.backnumber")[0]
            .text.split("\n")[1]
            .split("年")
            if year
        ]

    def _year_to_index(self, yyyy: int) -> str:
        """
        Convert year to index.

        Args:
            yyyy (int): year

        Returns:
            str: index
        """
        if yyyy == self.max_yyyy:
            return "index"
        else:
            return f"archives-{self.max_yyyy - yyyy:02d}"

    @property
    def yyyy(self) -> int:
        """
        Get year.
        """
        if self.__yyyy not in self.years:
            raise ValueError(f"Year must be in {self.years}.")
        return self.__yyyy

    @yyyy.setter
    def yyyy(self, yyyy: int) -> None:
        """
        Set year.

        Args:
            yyyy (int): year (>= 2006 and <= 2100)
        """
        self.__yyyy = yyyy

    @property
    def url(self) -> str:
        """
        Get URL.
        """
        return self.__url_template.format(index=self._year_to_index(self.yyyy))

    def _select_table(self) -> ResultSet[Tag]:
        """
        Select table.

        Returns:
            ResultSet[Tag]: table
        """
        html = get_content(self.url)
        soup = BeautifulSoup(html, "html.parser")
        return soup.select(self.table_css_selector)[0]

    def _get_n_cols_of_table(self, table: ResultSet[Tag]) -> int:
        """
        Get number of columns.

        Arg:
            table (ResultSet[Tag]): table

        Returns:
            int: number of columns
        """
        return len(table.find_all("th"))

    def _get_public_comment_4_cols(self, td_list: List[Tag]) -> JPXPublicComment:
        """
        Get public comment from td elements.

        Args:
            td_list (List[Tag]): list of td elements

        Returns:
            JPXPublicComment: public comment
        """
        return JPXPublicComment(
            date=td_list[0].text,
            pj_name=td_list[3].text,
            pj_name_url=format_url(td_list[3].find("a").get("href"), self.base_url),
            deadline=td_list[1].text,
            corporation=re.sub(r"[\r\n\s]", "", td_list[2].text),
        )

    def _get_public_comment_2_cols(self, td_list: List[Tag]) -> JPXPublicComment:
        """
        Get public comment from td elements.

        Args:
            td_list (List[Tag]): list of td elements

        Returns:
            JPXPublicComment: public comment
        """
        return JPXPublicComment(
            date=td_list[0].text,
            pj_name=td_list[1].text,
            pj_name_url=format_url(td_list[1].find("a").get("href"), self.base_url),
        )

    def get_public_comments(self) -> List[JPXPublicComment]:
        """
        Get list of public comment.

        Returns:
            List[JPXPublicComment]: list of public comment
        """
        table = self._select_table()
        n_cols = self._get_n_cols_of_table(table)
        results = []
        if n_cols == 4:
            for tr in table.find_all("tr"):
                if td_list := tr.find_all("td"):
                    results.append(self._get_public_comment_4_cols(td_list))
        elif n_cols == 2:
            for tr in table.find_all("tr"):
                if td_list := tr.find_all("td"):
                    results.append(self._get_public_comment_2_cols(td_list))
        return results

    @classmethod
    def get_links(cls, public_comment: JPXPublicComment) -> List[JPXPublicCommentLink]:
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
            JPXPublicCommentLink(
                url=format_url(element.get("href"), cls.base_url),
                publish_date=public_comment.date,
                project_name=public_comment.pj_name,
            )
            for element in elements
        ]
