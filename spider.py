import requests
import sys
import logging
import bs4

from contextlib import suppress

logging.StreamHandler(sys.stdout).setLevel(logging.DEBUG)

class Spider:

    def __init__(self, root_url, max_depth=5):
        self._root_url = root_url
        self._content = requests.get(root_url).content
        self.next_links = self._extract_links(self._content)
        self._visited_links = set([root_url])
        self._depth = 0
        self._max_depth = max_depth

    def _extract_links(self, page):
        soup = bs4.BeautifulSoup(page, 'html.parser')
        links = []
        for tag in soup('a'):
            with suppress(KeyError):
                links.append(self._root_url + tag['href'])
        return links

    def __iter__(self):
        while self.next_links != [] and self._depth < self._max_depth:
            yield self._content
            next_link = self.next_links.pop(0)
            print('Visiting', next_link)
            self._visited_links.add(next_link)
            self._content = requests.get(next_link).content
            extracted_links = self._extract_links(self._content)
            self.next_links.extend(link for link in extracted_links if link not in self._visited_links)
            self._depth += 1

