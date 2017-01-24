import pytest
import requests

from spider import Spider

website_url = 'http://localhost:99999'

test_website_content = b'''<html>
<h1>Hello world</h1>
<ul>
    <li><a href="/feature/thing1">link1</a></li>
    <li><a href="/feature/thing2">link2</a></li>
    <li><a href="/feature/thing3">link3</a></li>
</ul>
    
</html>'''

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.setattr(requests, 'get', lambda x: requests.Response())
    monkeypatch.setattr(requests.Response, 'content', test_website_content)

def test_gets_initial_page_contents():
    spider = Spider(website_url)

    assert next(iter(spider)) == test_website_content

def test_add_links_from_page_in_order():
    test_website_links = ['/feature/thing%d' % i for i in range(1, 4)]

    spider = Spider(website_url)

    assert spider.links == test_website_links
    #Crawl local site
    #Run test server on testing
