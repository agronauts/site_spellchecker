import pytest
import requests
from spider import Spider

website_url = 'http://localhost:99999'

def test_gets_initial_page_contents(monkeypatch):
    def test_website_content(*args, **kwargs):
        return b'''<html>
            <h1>Hello world</h1>
        </html>'''
    website_content = test_website_content()
    #website_content = requests.get(website_url).content
    monkeypatch.setattr(requests, 'get', test_website_content)

    spider = Spider(website_url)

    assert next(iter(spider)) == website_content

    #Crawl local site
    #Run test server on testing
