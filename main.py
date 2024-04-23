#!/usr/bin/python3

#from asyncore import write
from bs4 import BeautifulSoup
import requests
import sys
import time
import datetime
import config
from config import index_url, webhook_url, filter_words

db_file = "db.txt"
filtered_file = "filtered.txt"
all_urls = []
new_ads = 0

def read_file(file_name):
    try:
        with open(file_name, 'r') as file_raw:
            lines = file_raw.readlines()
            for line in lines:
                all_urls.append(line.rstrip('\n'))
    except FileNotFoundError:
        print(f'File {file_name} not found - creating it...')
        open(file_name, 'w').close()

def write_list_to_file(file_name, list_name):
    with open(file_name, 'w') as file_raw:
        for item in list_name:
            file_raw.write(item + '\n')

def append_to_file(file_name, append_content):
    with open(file_name, 'a') as file_raw:
        file_raw.write(append_content+ '\n')

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
        print("Ad posted to Discord.")

def url_contains_no_filtered_words(input_url):
    for word in filter_words:
        if word in input_url:
            print(f"Filtered {input_url} for {word}")
            # log filtered output
            append_to_file(filtered_file, f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: '{word}' found in '{input_url}'")
            return False
    return True

def get_articles_from_index():
    index_result = requests.get(index_url, headers={'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0'})
    index_soup = BeautifulSoup(index_result.text, 'html.parser')
    for article in index_soup.find_all('article'):
        ad_url = article.get('data-href')
        ad_info = article.find('a', class_='ellipsis')
        ad_name = ad_info.string
        if ad_url not in all_urls:
            all_urls.append(ad_url)
            if url_contains_no_filtered_words(ad_url):
                print("New ad found! " + ad_name)
                notify(webhook_input = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Neue Wohnung!\n\n{ad_name}\nhttps://kleinanzeigen.de{ad_url}")
                time.sleep(15)  # take a nap to avoid hitting Discord's rate limit. TODO: get the actual time from response headers
            # new_ads = new_ads + 1 # TODO

print("Reading database file...")
read_file(db_file)
print("Scraping ads from Ebay Kleinanzeigen...")
get_articles_from_index()
#print("New ads found in this run: " + str(new_ads))
print("Writing database...")
write_list_to_file(db_file, all_urls)
print("Done.")