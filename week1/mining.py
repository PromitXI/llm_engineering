import requests
from bs4 import BeautifulSoup
import re

# Standard headers to mimic a browser
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}


def get_data_from_url(url: str, max_chars: int = 4000) -> str:
    """
    Fetch and clean the visible text from a product page or any website.
    Optimized for review-heavy pages like Amazon, Flipkart, etc.

    Returns: A clean string (title + main text), truncated to `max_chars`.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=15,verify=False)
        response.raise_for_status()  # Raises an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        return f"[Error fetching {url}: {e}]"

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title safely
    title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

    # Remove irrelevant elements that clutter reviews or text
    for tag in soup(["script", "style", "img", "svg", "noscript", "meta", "input", "button", "nav", "footer", "header"]):
        tag.decompose()

    # Get all visible text, normalize spacing
    text = soup.get_text(separator="\n", strip=True)
    text = re.sub(r"\n{2,}", "\n", text)  # collapse multiple newlines
    text = re.sub(r"\s{2,}", " ", text)   # collapse multiple spaces

    # Truncate at sensible limit
    clean_text = (title + "\n\n" + text).strip()[:max_chars]

    return clean_text
