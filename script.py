import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from pathlib import Path


session = requests.Session()
def get_soup(url):
    response = session.get(url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, "html.parser")


import re
def nettoyer_nom_fichier(titre):
    titre_nettoye = re.sub(r'[^\w\-_\. ]', '_', titre.strip())  # remplace caractères spéciaux et supprime les espaces, /n, etc
    return titre_nettoye + ".jpg"

def nettoyer_nom_dossier(nom):
    return re.sub(r'[^\w\-\_\.\ ]', '_', nom.strip())


def get_data_book(url_book) :
    """
    Cette fonction prend en paramètre un site web, en extrait
    les informations suivantes et les stocks dans un dictionnaire """

    soup = get_soup(url_book)

    product_page_url = url_book
    upc_th = soup.find('th', string ='UPC')
    upc = upc_th.find_next_sibling('td').text

    title = soup.find('h1').text

    price_including_tax_th = soup.find('th', string = 'Price (incl. tax)')
    price_including_tax = price_including_tax_th.find_next_sibling('td').text

    price_excluding_tax_th = soup.find('th', string = 'Price (excl. tax)')
    price_excluding_tax = price_excluding_tax_th.find_next_sibling('td').text

    number_available_th = soup.find('th', string = "Availability")
    number_available = number_available_th.find_next_sibling('td').text

  
    product_description_h2 = soup.find(id='product_description')
    if product_description_h2:
        product_description = product_description_h2.find_next_sibling('p').text
    else:
        product_description = "Pas de description"

    category = soup.select("ul.breadcrumb li a")[2].text

    review_rating_before = soup.find("p", attrs = {'class': "instock availability"})
    review_rating_liste = review_rating_before.find_next_sibling("p")["class"]
    review_rating = "Star rating : " + review_rating_liste[1] + " out of Five."

    image_url_div = soup.find('div', attrs = {'class' : "item active"})
    image_url_relative = image_url_div.find("img")["src"]
    image_url = urljoin("https://books.toscrape.com/",image_url_relative)

    
    (Path("images") / nettoyer_nom_dossier(category)).mkdir(parents=True, exist_ok=True)
    nom_dossier = nettoyer_nom_dossier(category)
    nom_fichier = nettoyer_nom_fichier(title)
    chemin_complet = Path("images") / nom_dossier / nom_fichier 

    response = requests.get(image_url)
    with open(chemin_complet, "wb") as f:
        f.write(response.content)

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

def get_data_category(url_category):
    """Récupère les données de tous les livres d’une catégorie
    et les enregistre dans un fichier CSV nommé selon la catégorie.
    """
    all_books_data = []
    next_page_url = url_category

    while next_page_url:
        soup = get_soup(next_page_url)


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

    category_nom = soup.select_one("ul.breadcrumb li.active").text.strip()
    nom_fichier = category_nom + ".csv"

    with open(nom_fichier, "w", newline="", encoding="utf-8") as phase2:
        writer = csv.DictWriter(phase2, fieldnames=all_books_data[0].keys())
        writer.writeheader()
        writer.writerows(all_books_data)


def get_data_website(url):
    soup = get_soup(url)
    Path("images").mkdir(parents=True, exist_ok=True)
    # Trouve toutes les catégories dans la sidebar
    category_links = soup.select("div.side_categories ul li ul li a")

    for link in category_links:
        href = link["href"]
        url_category = urljoin(url, href)
        get_data_category(url_category)


url = "https://books.toscrape.com/index.html"
get_data_website(url)