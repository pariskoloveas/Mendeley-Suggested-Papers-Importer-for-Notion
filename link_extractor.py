import re
import requests
import os
import sys
from bs4 import BeautifulSoup
from NotionService import NotionService
from dotenv import load_dotenv
from hashlib import md5


def main(filename):

    entries = []

    notion = NotionService()
    entries = get_entries_from_html(filename)

    for entry in entries:
        notion.add_entries(entry)

    # print_entries(entries, headers)


def get_entries_from_html(filename):

    with open(file=os.path.join("files", filename), mode='r', encoding='utf-8') as f:
        html_page = f.read()

    soup = BeautifulSoup(html_page, features="lxml")
    tables = soup.findAll("table", {"class": re.compile('m_.*responsive-table')})[0].findAll("table")[0].findAll("table")

    entries = []
    for table in tables:
        tds = table.findAll("td")
        texts = [re.sub(r'\s+', ' ', td.get_text().replace("\n", "").strip()) for td in tds]
        link = get_redirected_link(tds[0].find('a').get('href'))
        hashed_title = get_md5_hash(texts[0])
        entry = texts + [link] + [hashed_title]
        entries.append(entry)

    return entries


def get_md5_hash(text):
    return md5(text.encode("utf-8")).hexdigest()


def get_redirected_link(link):
    response = requests.get(link)

    return response.url.split('?')[0]


def print_entries(entries):
    headers = ["Title", "Authors", "Venue", "URL", "Hashed Title"]
    for entry in entries:
        for text, header in zip(entry, headers):
            print(f"{header}: {text}")
        print()


if __name__ == "__main__":
    load_dotenv()
    args = sys.argv
    main(filename=args[1])
