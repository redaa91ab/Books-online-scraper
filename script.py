import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from pathlib import Path
import re



session = requests.Session()
def get_soup(url):
    """Returns a BeautifulSoup object from the HTML content of the given URL."""
    response = session.get(url)
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, "html.parser")


def clean_file_name(title):
    """Cleans a title to make it a valid image file name."""
    clean_title = re.sub(r'[^\w\-_\. ]', '_', title.strip())  # replaces specials characters and removes spaces, /n, etc
    return clean_title + ".jpg"

def clean_folder_name(name):
    """Cleans a folder name to make it a valid folder name"""
    return re.sub(r'[^\w\-\_\.\ ]', '_', name.strip())


def get_data_book(url_book) :
    """Retrieves a book's information and downloads its image.
    
    Returns a dictionary containing the extracted data.
    """

    soup = get_soup(url_book)

    #Extracts and stores each information in a variable.
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
        product_description = "No description"

    category = soup.select("ul.breadcrumb li a")[2].text

    review_rating_before = soup.find("p", attrs = {'class': "instock availability"})
    review_rating_list = review_rating_before.find_next_sibling("p")["class"]
    review_rating = "Star rating : " + review_rating_list[1] + " out of Five."

    image_url_div = soup.find('div', attrs = {'class' : "item active"})
    image_url_relative = image_url_div.find("img")["src"]
    image_url = urljoin("https://books.toscrape.com/",image_url_relative)


    # Create the category folder where to save the image
    (Path("images") / clean_folder_name(category)).mkdir(parents=True, exist_ok=True)
    folder_name = clean_folder_name(category)
    file_name = clean_file_name(title)
    full_path = Path("images") / folder_name / file_name 

    # Save the image
    response = requests.get(image_url)
    with open(full_path, "wb") as f:
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
    """Retrieves data from all the books in a category and saves it to a .csv file """
    all_books_data = []
    next_page_url = url_category

    while next_page_url:
        soup = get_soup(next_page_url)


        all_h3 = soup.find_all("h3")
        for h3 in all_h3:
            relative_url = h3.find("a")["href"]
            full_url = urljoin(next_page_url, relative_url)
            book_data = get_data_book(full_url)
            all_books_data.append(book_data)

        next_button = soup.select_one("li.next a")
        if next_button:
            next_href = next_button["href"]
            next_page_url = urljoin(next_page_url, next_href)
        else:
            break

    category_name = soup.select_one("ul.breadcrumb li.active").text.strip()
    file_name = category_name + ".csv"

    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_books_data[0].keys())
        writer.writeheader()
        writer.writerows(all_books_data)


def get_data_website(url):
    """Scrapes all the categories from the website and saves the data of each book."""
    soup = get_soup(url)
    if soup is None:
        print("Unable to retrieve the homepage.")
        return
    
    Path("images").mkdir(parents=True, exist_ok=True)

    category_links = soup.select("div.side_categories ul li ul li a")

    for link in category_links:
        href = link["href"]
        url_category = urljoin(url, href)
        get_data_category(url_category)


if __name__ == "__main__":
    try:
        url = "https://books.toscrape.com/index.html"
        get_data_website(url)
    except Exception as e:
        print("The script has failed.")
        print(f"Error : {e}")