import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes_and_authors(base_url):
    all_quotes = []
    all_authors = []

    current_page = 1
    while True:
        url = f"{base_url}/page/{current_page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]

            # Перевіряємо, чи ця цитата вже збережена
            if {'author': author, 'quote': text} not in all_quotes:
                all_quotes.append({'tags': tags, 'author': author, 'quote': text})

            # Перевіряємо, чи цей автор вже збережений
            if author not in [a['fullname'] for a in all_authors]:
                # Assuming you can extract author details from the site, replace the following with actual code
                author_details = {
                    "fullname": author,
                    "born_date": "",
                    "born_location": "",
                    "description": ""
                }
                all_authors.append(author_details)

        next_page_button = soup.find('li', class_='next')
        if not next_page_button:
            break

        current_page += 1

    return all_quotes, all_authors

base_url = "http://quotes.toscrape.com"
all_quotes, all_authors = scrape_quotes_and_authors(base_url)

with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
    json.dump(all_quotes, quotes_file, ensure_ascii=False, indent=2)

with open('authors.json', 'w', encoding='utf-8') as authors_file:
    json.dump(all_authors, authors_file, ensure_ascii=False, indent=2)
