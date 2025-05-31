import requests
from bs4 import BeautifulSoup


def scrape_more_links(url: str) -> str:
    """
    Scrapes the "more" url from the OTH Regensburg blackboard page and returns the text.
    Does a little markdown formatting for the time.
    Args:
        url: The URL of the "more" link to scrape.
    Returns:
        The text content of the page at the given URL.
    """
    res = requests.get(url)
    res.raise_for_status()  # Check for HTTP errors
    soup = BeautifulSoup(res.text, 'html.parser')

    # find the time of creation
    time=soup.find('time', itemprop='datePublished')
    # Find the content in the page
    content = soup.find('span', itemprop='description')


    if content:
        return f'**{time.get_text(strip=True)}** {content.get_text(strip=True)}' # type: ignore
    else:
        raise ValueError(f"No content found at {url}. The structure of the page may have changed.")

def scrape_oth_blackboard(url: str) -> list[tuple[str, str]]:
    """
    Scrape the OTH Regensburg blackboard for entries.
    Args:
        url: The URL of the OTH Regensburg blackboard.
    Returns:
        A list of tuples containing the header and teaser text of each entry.
    """
    # Note: The User-Agent header is commented out, as it may not be necessary.
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    soup = BeautifulSoup(response.text, 'html.parser')
    entries = soup.find_all('div', class_='header')
    more_links = soup.find_all('a', class_='more')
    
    result = []
    for header, more_url in zip(entries, more_links, strict=True):
        header_text = header.get_text(strip=True)

        complete_url = url[:url.rfind('/')] + more_url['href']  # type: ignore

        content_text = scrape_more_links(complete_url)

        result.append((header_text, content_text))
    return result

def save_to_markdown(entries: list[tuple[str, str]], filename: str):
    """
    Save the scraped entries to a markdown file.
    Args:
        entries: The list of entries to save.
        filename: The name of the markdown file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for header, teaser in entries:
            f.write(f"## {header}\n\n{teaser}\n\n")

if __name__ == "__main__":
    url = 'https://informatik-mathematik.oth-regensburg.de/schwarzes-brett'
    entries = scrape_oth_blackboard(url)
    save_to_markdown(entries, 'oth_blackboard.md')