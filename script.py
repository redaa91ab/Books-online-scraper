import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

session = requests.Session()

def get_data_book(url) :
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



""""
with open("phase1.csv", "w", newline = "") as file :
        csv.writer(file).writerow (["product_page_url", "universal_ product_code (upc)","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating", "image_url"])
        csv.writer(file).writerow([product_page_url, upc,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating, image_url])
"""

url_category = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"

def get_data_category(url_category) : 
    bookstoscrape = session.get(url_category)
    bookstoscrape.encoding = 'utf-8'
    soup = BeautifulSoup(bookstoscrape.text, "html.parser")
    all_h3 = soup.find_all("h3")
    for h3 in all_h3 :
        urls = h3.find("a")["href"]
        all_url= urljoin (url_category, urls)
        print(all_url)

get_data_category(url_category)
