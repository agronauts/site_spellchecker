import requests
import bs4

class Spider:

    def __init__(self, root_url):
        self._root_url = root_url
        self._content = requests.get(root_url).content
        self.next_links = self._extract_links(self._content)

    def _extract_links(self, page):
        soup = bs4.BeautifulSoup(page, 'html.parser')
        links = [self._root_url + tag['href'] for tag in soup('a')]
        return links

    def __iter__(self):
        while self.next_links != []:
            yield self._content
            self._content = requests.get(self.next_links.pop(0)).content
            self.next_links.extend(self._extract_links(self._content))

