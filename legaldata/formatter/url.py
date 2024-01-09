import re
from urllib.parse import urlparse


def format_url(url: str, base_url: str) -> str:
    """
    Format URL.

    Args:
        url (str): url to format.
        base_url (str): base url.

    Returns:
        str: formatted url.
    """
    if re.match(r"^https?://", url):
        return url
    elif url.startswith("/"):
        return base_url + url
    elif url.startswith("./"):
        return base_url + url[1:]
    elif url.startswith("../"):
        parsed_base_url = urlparse(base_url)
        path_parts = parsed_base_url.path.split("/")
        if len(path_parts) > 1:
            new_path = "/".join(path_parts[:-1])
        else:
            new_path = "/"
        new_base_url = parsed_base_url._replace(path=new_path)
        return new_base_url.geturl() + url[2:]
    else:
        return base_url + "/" + url
