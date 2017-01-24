from itertools import chain
import re
import sys
import pprint
import requests
import bs4
import logging

#logging.basicConfig(filename='spellchecker.log', level=logging.DEBUG)
logging.StreamHandler(sys.stdout).setLevel(logging.DEBUG)

urls = [
    'https://takingshape.com.au/',
    'https://www.sachadrake.com/',
    'https://www.smithscity.co.nz/',
    'https://www.allaboutagirl.co.nz/',
    'https://www.no1fitness.co.nz/',
    'https://www.mimco.com.au/',
    'https://www.swanndri.co.nz/',
    'https://www.roddandgunn.com/',
    'https://shop.jbhifi.co.nz/',
    'https://www.countryroad.com.au/',
    'https://www.witchery.com.au/',
]


def get_words(url):
    page = requests.get(url).content
    soup = bs4.BeautifulSoup(page, 'html.parser')
    words = set(re.findall(r'\b[a-z]+\b', soup.text, re.I))
    return words

def spell_check(words):
    logging.info('Checking: ', str(words))
    misspelt_words = check_spelling(words)
    return set(misspelt_words)

def website_check(words):
    page = requests.post('http://app.aspell.net/lookup', {'dict': 'en_AU', 'words': words}).content
    soup = bs4.BeautifulSoup(page, 'html.parser')
    misspelt_words = [tag.findChildren()[0].text for tag in soup.find_all(name='tr') if len(tag.findChildren()) == 8 and tag.findChildren()[2].text == 'NO']
    return set(misspelt_words)

def local_file_check():
    with open('words.txt', 'r') as dictionary_file:
        correct_words = set(word.strip() for word in dictionary_file)
    def inner(words):
        misspelt_words = [word for word in words if word not in correct_words]
        return misspelt_words
    return inner

check_spelling = local_file_check()


for url in urls:
    words = get_words(url)
    misspelt_words = spell_check(words)
    print(url, 'had', len(misspelt_words), 'misspelt words:')
    pprint.pprint(misspelt_words)


