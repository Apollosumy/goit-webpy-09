import requests
from bs4 import BeautifulSoup
import json
from time import sleep


BASE_URL = "http://quotes.toscrape.com"


quotes_data = []
authors_data = []


authors_visited = {}

def scrape_quotes(page_url):
    """Функция для скрапинга цитат с одной страницы"""
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    
    quotes = soup.select("div.quote")
    for quote in quotes:
        text = quote.select_one("span.text").get_text(strip=True)
        author = quote.select_one("span small.author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select("div.tags a.tag")]

       
        quotes_data.append({
            "quote": text,
            "author": author,
            "tags": tags
        })

        
        author_link = quote.select_one("span a")["href"]
        author_url = BASE_URL + author_link
        if author not in authors_visited:
            authors_visited[author] = author_url


    next_page = soup.select_one("li.next a")
    if next_page:
        next_page_url = BASE_URL + next_page["href"]
        scrape_quotes(next_page_url)

def scrape_author(author_url):
    """Функция для скрапинга данных об авторе"""
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, "html.parser")

    
    name = soup.select_one("h3.author-title").get_text(strip=True)
    birth_date = soup.select_one("span.author-born-date").get_text(strip=True)
    birth_place = soup.select_one("span.author-born-location").get_text(strip=True)
    description = soup.select_one("div.author-description").get_text(strip=True)

    # Добавление данных об авторе
    authors_data.append({
        "name": name,
        "birth_date": birth_date,
        "birth_place": birth_place,
        "description": description
    })

def main():
    
    print("Начинаем скрапинг цитат...")
    scrape_quotes(BASE_URL)


    print("Начинаем скрапинг авторов...")
    for author, url in authors_visited.items():
        scrape_author(url)
        sleep(1)  

    
    print("Сохраняем данные в JSON-файлы...")
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=4)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors_data, f, ensure_ascii=False, indent=4)

    print("Скрапинг завершен! Данные сохранены в файлы quotes.json и authors.json.")

if __name__ == "__main__":
    main()
