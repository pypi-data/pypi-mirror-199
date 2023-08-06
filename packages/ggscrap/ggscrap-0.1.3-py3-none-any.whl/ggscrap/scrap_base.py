from bs4 import BeautifulSoup
import requests
import requests_html
from requests_html import HTMLSession
import time
from typing import Optional, List, Dict
import urllib

RESPONSE = requests.models.Response
URL = str

HEADERS = [
    None,
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    },
    {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    },
]


class GGScrapException(Exception):
    pass


# waits for a connection, returns True if connected
def wait_for_connection(
        url: URL=               'http://ident.me/',
        logger=                 None,
        max_sec: Optional[int]= None,
) -> bool:

    connected = False
    loop_ix = 0
    while True:
        response = None
        try:
            response = requests.get(url=url, timeout=5)
            if logger: logger.info(f'waiting for connection, got: {response}')
        except Exception as e:
            if logger: logger.warning(f'got connection exception: {e}')
        if response and response.status_code == 200:
            connected = True
            if logger: logger.info(f'got nice connection!')
            break
        time.sleep(5)

        loop_ix += 1
        if max_sec is not None and max_sec <= loop_ix * 5:
            break

    return connected

# tries to download RESPONSE from URL
def download_response(
        url: URL,
        header: Optional[Dict]= None,
        proxy: Optional[str]=   None,
        logger=                 None) -> Optional[RESPONSE]:
    try:
        session = HTMLSession()
        proxies = {'http': f'http://{proxy}'} if proxy else None
        response = session.get(url, headers=header, proxies=proxies)
        if logger: logger.debug(f'download_response() got response: "{response}" from url: {url}, header: {header}, proxy: {proxy}')
        response.session = session
        return response
    except Exception as e:
        msg = f'download_response() got exception: "{e}", url: {url}, header: {header}, proxy: {proxy}'
        if logger: logger.warning(msg)
        return None

# extracts sub-urls from RESPONSE
def extract_subURLs(response:RESPONSE, logger=None) -> List[URL]:
    try:
        html = requests_html.HTML(
            session=            HTMLSession(),
            url=                response.url,
            html=               response.content,
            default_encoding=   response.encoding)
        return list(html.absolute_links)
    except Exception as e:
        msg = f'extract_subURLs() got exception: "{e}"'
        if logger: logger.warning(msg)
        return []

# extracts words from the url base
def get_head_words(url:URL) -> List[str]:
    url = url.replace('https://','')
    url = url.replace('http://', '')
    head = url.split('/')[0]
    head = head.split('.')
    head.pop(-1) # remove domain
    if 'www' in head: head.remove('www')
    return head

# filters given URLs, removes those containing any filter before first /
def filter_URLs(
        urls: List[URL],
        filters: List[str] # filter is a str, words space separated, like 'maps google', if both are in URL before / <- filter matches and URL is filtered out
) -> List[URL]:

    filters_split = [f.split() for f in filters]
    filtered = []
    for url in urls:
        head_words = get_head_words(url)
        url_ok = True
        for fs in filters_split:
            all_in = True
            for f in fs:
                if f not in head_words:
                    all_in = False
                    break
            if all_in:
                url_ok = False
                break
        if url_ok: filtered.append(url)

    return filtered

# extracts text from RESPONSE
def extract_text(
        response: RESPONSE,
        separator=      '\n',
        encode_decode=  True,
        logger=         None,
) -> Optional[str]:
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=separator)
        if encode_decode:
            text = text.encode("ascii", "ignore")
            text = text.decode()
        return text
    except Exception as e:
        msg = f'get_texts() got exception: "{e}"'
        if logger: logger.warning(msg)
        return None

# builds google search URL for given query
def build_google_url(query:str) -> str:
    if not query:
        raise GGScrapException('cannot build google url for empty query')
    return f'https://www.google.com/search?q={urllib.parse.quote_plus(query)}'