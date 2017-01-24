import requests
import bs4

class Spider:

    def __init__(self, root_url):
        self._content = requests.get(root_url).content
        print(self._content)
        self.links = self._extract_links(self._content)

    def _extract_links(self, page):
        soup = bs4.BeautifulSoup(page, 'html.parser')
        links = [tag['href'] for tag in soup('a')]
        return links

    def __iter__(self):
        yield self._content
