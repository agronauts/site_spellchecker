import requests

class Spider:

    def __init__(self, root_url):
        self._content = self._get_content(root_url)

    def _get_content(self, url):
        return requests.get(url)

    def __iter__(self):
        yield self._content
