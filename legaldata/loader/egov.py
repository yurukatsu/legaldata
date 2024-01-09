import re
from functools import lru_cache
from typing import Dict, List, Optional, Union

from pydantic import Field

from legaldata.loader import BaseLink, BaseLoader, get_content, get_xml


class EGOVLink(BaseLink):
    """
    Link to law data with e-Gov (https://www.e-gov.go.jp/) site.
    """

    description: str = "e-Gov法令データ"
    category: str = "e-Gov"
    name: str = "e-Gov"
    extension: str = "xml"
    law_id: str = Field(description="法令ID", exclude=False)
    law_name: str = Field(description="法令名", exclude=False)
    law_number: str = Field(description="法令番号", exclude=False)
    promulgation_date: str = Field(description="公布日", exclude=False)


class EGOVLoader(BaseLoader):
    """
    Prepare law data with e-Gov (https://www.e-gov.go.jp/) site.

    Args:
        category (int): category number, like 1 (all), 2 (法令), 3 (政令), 4 (省令)
    """

    def __init__(self, category: int = 1) -> None:
        self.__category = category

    @property
    def category(self) -> int:
        """
        Get category number.
        """
        return self.__category

    @category.setter
    def category(self, category: int) -> None:
        """
        Set category number.

        Args:
            category (int): category number, like 1 (all), 2 (法令), 3 (政令), 4 (省令)
        """
        self.__category = category

    @property
    def url(self) -> str:
        """
        Get URL.
        """
        return f"https://elaws.e-gov.go.jp/api/1/lawlists/{self.category}"

    @classmethod
    def get_law_dict(cls, url: str) -> Dict[str, str]:
        """
        Return dictionary of law names and numbers.

        Args:
            url (str): URL

        Returns:
            Dict(str, str): dictionary of law names (keys) and numbers (values)
        """
        root = get_xml(url)
        names = [e.text for e in root.iter() if e.tag == "LawName"]
        numbers = [e.text for e in root.iter() if e.tag == "LawNo"]
        return {name: num for (name, num) in zip(names, numbers)}

    def _get_law_dict(self) -> Dict[str, str]:
        """
        Get dictionary of law names and numbers.
        """
        return self.get_law_dict(self.url)

    def get_links(self) -> List[EGOVLink]:
        """
        Get links to data.
        """
        root = get_xml(self.url)
        ids = [e.text for e in root.iter() if e.tag == "LawId"]
        names = [e.text for e in root.iter() if e.tag == "LawName"]
        numbers = [e.text for e in root.iter() if e.tag == "LawNo"]
        promulgation_dates = [
            e.text for e in root.iter() if e.tag == "PromulgationDate"
        ]
        return [
            EGOVLink(
                law_id=id_,
                law_name=name,
                law_number=number,
                promulgation_date=promulgation_date,
                url=f"https://elaws.e-gov.go.jp/api/1/lawdata/{number}",
            )
            for (id_, name, number, promulgation_date) in zip(
                ids, names, numbers, promulgation_dates
            )
        ]

    def get_raw(self, url: str) -> List[str]:
        """
        Args:
            number (str): Number of the law, like '平成九年厚生省令第二十八号'

        Returns:
            raw (List[str]): raw contents of J-GCP
        """
        root = get_xml(url)
        contents = [e.text.strip() for e in root.iter() if e.text]
        raw = [t for t in contents if t]
        return raw

    @staticmethod
    def pre_process(raw: List[str]) -> str:
        """
        Perform pre-processing on raw contents.

        Args:
            raw (List[str]): raw contents

        Returns:
            str: pre-processed string

        Notes:
            - Strings enclosed with （ and ） will be removed.
            - 「 and 」 will be removed.
        """
        contents = [s for s in raw if s.endswith("。")]
        string = "".join(contents)
        string = string.translate(str.maketrans({"「": "", "」": ""}))
        return re.sub("（[^（|^）]*）", "", string)
