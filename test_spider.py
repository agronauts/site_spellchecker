import pytest
import requests

from spider import Spider

website_url = 'http://localhost:99999'

test_website_content = b'''<html>
    <h1>Hello world</h1>
</html>'''

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.setattr(requests, 'get', lambda x: requests.Response())
    monkeypatch.setattr(requests.Response, 'content', test_website_content)

def test_gets_initial_page_contents(monkeypatch):
    spider = Spider(website_url)

    assert next(iter(spider)) == test_website_content

    #Crawl local site
    #Run test server on testing
