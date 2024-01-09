from bs4 import BeautifulSoup


def extract_text(html: str) -> str:
    """
    Extract text from HTML.

    Args:
        html (str): HTML to format.

    Returns:
        str: extracted text from HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    # extract text
    text = soup.get_text()
    # strip
    lines = [line.strip() for line in text.splitlines()]
    # remove empty lines
    text = "\n".join(line for line in lines if line)
    return text
