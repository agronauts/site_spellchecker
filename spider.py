import requests

class Spider:

    def __init__(self, root_url):
        self._content = requests.get(root_url).content

    def __iter__(self):
        yield self._content
