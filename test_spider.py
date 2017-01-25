import pytest
import requests

from spider import Spider
from collections import OrderedDict

website_url = 'http://localhost:99999'

test_website_content = OrderedDict()
for i in range(1,4):
    test_website_content['thing%d' % i] = b'''<html>
    <h1>Chinatown%d</h1>
    </html>''' % i
test_website_content[''] = b'''<html>
<h1>Hello world</h1>
<ul>
    <li><a href="/thing1">link1</a></li>
    <li><a href="/thing2">link2</a></li>
    <li><a href="/thing3">link3</a></li>
</ul>
</html>'''


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    def mocked_get(url, *_):
        resp = requests.Response()
        for name, content in test_website_content.items():
            if name in url:
                resp._content = content
                return resp

    monkeypatch.setattr(requests, 'get', mocked_get)

def test_gets_initial_page_contents():
    spider = Spider(website_url)

    assert next(iter(spider)) == test_website_content['']

def test_add_links_from_page_in_order():
    test_website_links = [website_url + '/thing%d' % i for i in range(1, 4)]

    spider = Spider(website_url)

    assert spider.next_links == test_website_links

def test_process_links_in_initial_page():
    expected_pages = [test_website_content['thing%d' % i] for i in range(1,4)]

    spider = Spider(website_url)
    gen = iter(spider)
    next(gen)

    assert len(spider.next_links) == 3
    for spider_page, expected_page in zip(gen, expected_pages):
        assert spider_page == expected_page
    #Crawl local site
    #Run test server on testing
