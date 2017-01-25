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
# Index page is last so empty string matches all url's
test_website_content[''] = b'''<html>
<h1>Hello world</h1>
<ul>
    <li><a href="/thing1">link1</a></li>
    <li><a href="/thing2">link2</a></li>
    <li><a href="/thing3">link3</a></li>
</ul>
</html>'''

cyclic_website_url = 'http://localhost:99998'
test_cyclic_website_content = OrderedDict()
test_cyclic_website_content['part1'] = b'''<html><a href="/part2">link2</a>'''
test_cyclic_website_content['part2'] = b'''<html><a href="/">link3</a>'''
test_cyclic_website_content[''] = b'''<html><a href="/part1">link1</a>'''

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    def mocked_get(url, *_):
        resp = requests.Response()
        if '99999' in url:
            website_content = test_website_content
        elif '99998' in url:
            website_content = test_cyclic_website_content
        for name, content in website_content.items():
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

def test_stops_cycles():
    expected_pages = [test_cyclic_website_content[name] for name in ['', 'part1', 'part2']]

    spider = Spider(cyclic_website_url)
    count = 0
    for _ in spider:
        assert count <= 3
        count += 1 #Infinite loop protection
    assert count == 3
