import requests
from bs4 import BeautifulSoup
import csv

def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {url}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    books = []
    
    # Find all book containers
    book_containers = soup.find_all('article', class_='product_pod')
    
    for container in book_containers:
        title = container.h3.a['title']
        price = container.find('p', class_='price_color').text
        books.append({'title': title, 'price': price})
    
    return books

def main():
    base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
    all_books = []
    
    # Scrape the first 5 pages for example
    for page in range(1, 6):
        url = base_url.format(page)
        books = scrape_books(url)
        all_books.extend(books)
        print(f"Scraped page {page}, found {len(books)} books")
    
    # Save to CSV
    with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for book in all_books:
            writer.writerow(book)
    
    print("Data saved to books.csv")

if __name__ == "__main__":
    main()