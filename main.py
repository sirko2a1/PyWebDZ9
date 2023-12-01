import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes_and_authors(base_url):
    all_quotes = []
    all_authors = []
    all_page_links = []

    current_page = 1
    while True:
        url = f"{base_url}/page/{current_page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        all_page_links.append(url)

        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').text
            author_elem = quote.find('small', class_='author')
            
            author_name = auth_name(author_elem.text) if author_elem else ""
            author_link = base_url + author_elem.find_next('a')['href'] if author_elem else ""
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]

            quote_details = {
                "tags": tags,
                "author": author_name,
                "quote": text,
            }

            if quote_details not in all_quotes:
                all_quotes.append(quote_details)

            if author_name and author_name not in [a['fullname'] for a in all_authors]:
                author_details = get_author_details(author_link)
                all_authors.append(author_details)

        next_page_button = soup.find('li', class_='next')
        if not next_page_button:
            break

        current_page += 1

    return all_quotes, all_authors

def get_author_details(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    fullname_elem = soup.find('h3', class_='author-title')
    born_date_elem = soup.find('span', class_='author-born-date')
    born_location_elem = soup.find('span', class_='author-born-location')
    description_elem = soup.find('div', class_='author-description')

    fullname = fullname_elem.text.strip() if fullname_elem else ""
    born_date = born_date_elem.text.strip() if born_date_elem else ""
    born_location = born_location_elem.text.strip() if born_location_elem else ""
    description = description_elem.text.strip() if description_elem else ""

    author_details = {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description,
    }

    return author_details

def auth_name(author_text):
    return author_text.replace("by", "").strip()

base_url = "http://quotes.toscrape.com"
all_quotes, all_authors = scrape_quotes_and_authors(base_url)

with open('qoutes.json', 'w', encoding='utf-8') as quotes_file:
    json.dump(all_quotes, quotes_file, ensure_ascii=False, indent=2)

with open('authors.json', 'w', encoding='utf-8') as authors_file:
    json.dump(all_authors, authors_file, ensure_ascii=False, indent=2)
