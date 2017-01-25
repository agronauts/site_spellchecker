import requests
import bs4

class Spider:

    def __init__(self, root_url):
        self._root_url = root_url
        self._content = requests.get(root_url).content
        self.next_links = self._extract_links(self._content)
        self._visited_links = set([root_url])

    def _extract_links(self, page):
        soup = bs4.BeautifulSoup(page, 'html.parser')
        links = [self._root_url + tag['href'] for tag in soup('a')]
        return links

    def __iter__(self):
        while self.next_links != []:
            print(self.next_links)
            print(self._visited_links)
            yield self._content
            next_link = self.next_links.pop(0)
            self._visited_links.add(next_link)
            self._content = requests.get(next_link).content
            extracted_links = self._extract_links(self._content)
            print(extracted_links)
            self.next_links.extend(link for link in extracted_links if link not in self._visited_links)

