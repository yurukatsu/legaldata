import json
import os
from abc import ABC, abstractmethod
from typing import List, Optional
from urllib.parse import urlparse
from xml.etree import ElementTree

import requests
from pydantic import BaseModel, Field


def get_content(
    url: str, encoding: Optional[str] = None, errors: Optional[str] = "strict", **kwargs
) -> str:
    """
    GET content from URL.

    Args:
        url (str): URL to XML data.
        encoding (str, optional): Encoding of XML data.
        errors (str, optional):
            The error handling scheme to use for the handling of decoding errors.
            The default is 'strict' meaning that decoding errors raise a UnicodeDecodeError.
            Other possible values are 'ignore' and 'replace' as well as any other name
            registered with codecs.register_error that can handle UnicodeDecodeErrors.
        **kwargs: Keyword arguments passed to `requests.get`.

    Returns:
        str: content
    """
    response = requests.get(url, **kwargs)
    response.encoding = response.apparent_encoding
    if response.status_code != 200:
        raise Exception(f"Failed to get data from {url}")
    if encoding:
        return response.content.decode(encoding=encoding, errors=errors)
    else:
        return response.content


def get_xml(
    url: str, encoding: str = "utf-8", errors: str = "strict", **kwargs
) -> ElementTree.Element:
    """
    Get XML data from URL.

    Args:
        url (str): URL to XML data.
        encoding (str): Encoding of XML data.
        errors (str):
            The error handling scheme to use for the handling of decoding errors.
            The default is 'strict' meaning that decoding errors raise a UnicodeDecodeError.
            Other possible values are 'ignore' and 'replace' as well as any other name
            registered with codecs.register_error that can handle UnicodeDecodeErrors.
        **kwargs: Keyword arguments passed to `requests.get`.

    Returns:
        ElementTree.Element: element tree of XML data.
    """
    return ElementTree.fromstring(
        get_content(url=url, encoding=encoding, errors=errors, **kwargs)
    )


class BaseLink(BaseModel):
    url: str = Field(description="URL to data", exclude=False)
    extension: str = Field(description="Format of data", exclude=False)
    category: str = Field(description="Category of data", exclude=True)
    name: str = Field(description="Name of data", exclude=True)
    description: str = Field(description="Description of data", exclude=True)


class BaseLoader(ABC):
    """
    Base class for loader.

    Args:
        url (str): URL.
    """

    @property
    @abstractmethod
    def url(self) -> str:
        """
        Get URL.
        """

    @property
    def hostname(self) -> str:
        """
        Get hostname of URL.

        Returns:
            str: hostname of URL.
        """
        return urlparse(self.url).hostname

    @abstractmethod
    def get_links(self) -> List[BaseLink]:
        """
        Get links to data.
        """

    @classmethod
    def save_content(cls, link: BaseLink, filename: str) -> None:
        """
        Download data from URL.

        Args:
            link (BaseLink): Link to data.
            filename (str): Filename of data.
        """
        try:
            with open(filename, "wb") as f:
                content = get_content(link.url)
                f.write(content)
        except Exception as e:
            raise e

    @classmethod
    def save_content_w_metadata(
        cls,
        link: BaseLink,
        save_dir: str,
        filename: str = "content",
        metadata_name: str = "metadata",
    ) -> None:
        """
        Download data from URL with metadata.

        Args:
            link (BaseLink): Link to data.
            save_dir (str): Directory to save data.
            filename (str, optional): Filename of data w/o extension. Defaults to "content".
            metadata_name (str, optional): Filename of metadata. Defaults to "metadata".
        """
        if os.path.exists(save_dir) is False:
            os.makedirs(save_dir)
        try:
            with open(
                os.path.join(save_dir, f"{filename}.{link.extension}"), "wb"
            ) as f:
                content = get_content(link.url)
                f.write(content)
            with open(os.path.join(save_dir, f"{metadata_name}.json"), "w") as f:
                json.dump(link.__dict__, f, ensure_ascii=False, indent=4)
        except Exception as e:
            raise e
