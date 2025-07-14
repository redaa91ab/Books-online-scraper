import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

session = requests.Session()

def get_data_book(url) :
    """
    Cette fonction prend en paramètre un site web, en extrait
    les informations suivantes et les stocks dans un dictionnaire """
    bookstoscrape = session.get(url)
    bookstoscrape.encoding = 'utf-8'
    soup = BeautifulSoup(bookstoscrape.text, "html.parser")

    product_page_url = url
    upc_th = soup.find('th', string ='UPC')
    upc = upc_th.find_next_sibling('td').text

    title = soup.find('h1').text

    price_including_tax_th = soup.find('th', string = 'Price (incl. tax)')
    price_including_tax = price_including_tax_th.find_next_sibling('td').text

    price_excluding_tax_th = soup.find('th', string = 'Price (excl. tax)')
    price_excluding_tax = price_excluding_tax_th.find_next_sibling('td').text

    number_available_th = soup.find('th', string = "Availability")
    number_available = number_available_th.find_next_sibling('td').text

    product_description_h2= soup.find(id = 'product_description')
    product_description = product_description_h2.find_next_sibling('p').text

    category = soup.select("ul.breadcrumb li a")[2].text

    review_rating_before = soup.find("p", attrs = {'class': "instock availability"}) 
    review_rating_liste = review_rating_before.find_next_sibling("p")["class"]
    review_rating = "Star rating : " + review_rating_liste[1] + " out of Five."

    image_url_div = soup.find('div', attrs = {'class' : "item active"})
    image_url_relative = image_url_div.find("img")["src"]
    image_url = urljoin("https://books.toscrape.com/",image_url_relative)

    return {"product_page_url": product_page_url,
    "upc": upc,
    "title": title,
    "price_including_tax": price_including_tax,
    "price_excluding_tax": price_excluding_tax,
    "number_available": number_available,
    "product_description": product_description,
    "category": category,
    "review_rating": review_rating,
    "image_url": image_url }
    


url_category = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"


def get_data_category(url_category):

    all_books_data = []
    next_page_url = url_category

    while next_page_url:
        response = session.get(next_page_url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        all_h3 = soup.find_all("h3")
        for h3 in all_h3:
            url_relatif = h3.find("a")["href"]
            url_entier = urljoin(next_page_url, url_relatif)
            book_data = get_data_book(url_entier)
            all_books_data.append(book_data)

        next_button = soup.select_one("li.next a")
        if next_button:
            next_href = next_button["href"]
            next_page_url = urljoin(next_page_url, next_href)
        else:
            break

    return(all_books_data)



all_book_data = get_data_category(url_category)


with open("phase2.csv", "w", newline="", encoding="utf-8") as phase2:
    writer = csv.DictWriter(phase2, fieldnames=all_book_data[0].keys())
    writer.writeheader()
    writer.writerows(all_book_data)





"""
def get_data_category(url_category) : 
    bookstoscrape = session.get(url_category)
    bookstoscrape.encoding = 'utf-8'
    soup = BeautifulSoup(bookstoscrape.text, "html.parser")
    page_next = soup.select("ul.pager li a")[0]["href"]
    all_h3 = soup.find_all("h3")
    each_page = url_category
    for each_page in range :
        bookstoscrape_next_page = session.get(each_page)
        bookstoscrape_next_page.encoding = 'utf-8'
        soup_next_page = BeautifulSoup(bookstoscrape_next_page.text, "html.parser")
        for h3 in all_h3 :
            urls = h3.find("a")["href"]
            all_url= urljoin (each_page, urls)
            print(all_url)
        each_page = urljoin(each_page,page_next)

get_data_category(url_category)
"""





