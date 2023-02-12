#!/usr/bin/python3

#from asyncore import write
from bs4 import BeautifulSoup
import requests
import sys
import time
import datetime
import config

index_url = config.index_url
webhook_url = config.webhook_url
filter_words = config.filter_words

db_file = "db.txt"
all_urls = []
new_ads = 0

def read_file():
    try:
        with open(db_file, 'r') as db:
            lines = db.readlines()
            for line in lines:
                all_urls.append(line.rstrip('\n'))
    except FileNotFoundError:
        print('Database file nout found - creating it...')
        open('db.txt', 'w').close()

def write_file():
    with open(db_file, 'w') as db:
        for url in all_urls:
            db.write(url + '\n')

def notify(webhook_input):
    data = {
        "content" : webhook_input,
        "username" : "EbayKleinanzeigenBot"
    }
    result = requests.post(webhook_url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def filter_url(input_url):
    for word in filter_words:
        if word in input_url:
            print(f"{word} in {input_url}")
            print(f"URL {input_url} contains a filtered word. You won't be notified.")
            return False
    return True

def get_articles_from_index():
    index_result = requests.get(index_url, headers={'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0'})
    index_soup = BeautifulSoup(index_result.text, 'html.parser')
    for article in index_soup.find_all('article'):
        ad_url = article.get('data-href')
        ad_info = article.find('a', class_='ellipsis')
        try:
            ad_name = ad_info.string
        except AttributeError:
            ad_name = "Ad name empty"
        if ad_url not in all_urls:
            all_urls.append(ad_url)
            if filter_url(ad_url):
                print("New ad found! " + ad_name)
                notify(webhook_input = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Neues Inserat!\n\n{ad_name}\nhttps://ebay-kleinanzeigen.de{ad_url}")
                time.sleep(15)  # take a nap to avoid hitting Discord's rate limit. TODO: get the actual time from response headers
            # new_ads = new_ads + 1 # TODO

print("Reading database file...")
read_file()
print("Scraping ads from Ebay Kleinanzeigen...")
get_articles_from_index()
#print("New ads found in this run: " + str(new_ads))
print("Writing database...")
write_file()
print("Done.")