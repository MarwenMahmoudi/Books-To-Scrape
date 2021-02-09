import pandas as pd
import requests
from bs4 import BeautifulSoup

html = requests.get("https://books.toscrape.com/catalogue/category/books/mystery_3/page-1.html")
text = BeautifulSoup(html.content, 'html.parser')

# pagination
# get number of pages per category
page_indicator = text.find(class_='current').get_text().split()
num_pages = int(page_indicator[3])
# print(num_pages)

Category_pages_links = []
current_html = "https://books.toscrape.com/catalogue/category/books/mystery_3/"

for i in range(1, num_pages+1):
    page_link = current_html+"page-"+str(i)+".html"
    Category_pages_links.append(page_link)
# print(Category_pages_list)

Category_books_links = []
for x in Category_pages_links:
    html = requests.get(x)
    text = BeautifulSoup(html.content, 'html.parser')
    # get books links
    Container = text.find_all(class_='image_container')
    for link in Container:
        href_att = link.a['href']
        href_txt = href_att.split("../../..")
        booksLink = "https://books.toscrape.com/catalogue" + href_txt[1]
        Category_books_links.append(booksLink)
# print(Category_books_links)

# Lists of contents to use later in a dictionary
Titles = []
Product_page_url = []
Categories = []
Product_DescriptionS = []
Image_urlS = []
upc = []
PIncTax = []
PExTax = []
ratings = []
Num_available = []
for current_link in Category_books_links:
    r = requests.get(current_link)
    soup = BeautifulSoup(r.content, 'html.parser')

    Product_page = r.url
    Product_page_url.append(Product_page)

    Title = soup.find('h1').get_text()
    Titles.append(Title)


    Category_a = soup.find(class_="breadcrumb").find_all('a')
    Category = Category_a[2].string
    Categories.append(Category)


    Product_Description = soup.find(class_="sub-header").findNext('p').get_text()
    Product_DescriptionS.append(Product_Description)

    src_txt = soup.find(class_='item active').img.get('src')
    jpg = src_txt.split("../../")
    Image_url = ('https://books.toscrape.com/' + jpg[1])
    Image_urlS.append(Image_url)

    Product_information = soup.find(class_='table table-striped').find_all('td')

    universal_product_code = Product_information[0].get_text()
    upc.append(universal_product_code)

    price_excluding_tax = Product_information[2].get_text()
    PExTax.append(price_excluding_tax)

    price_including_tax = Product_information[3].get_text()
    PIncTax.append(price_including_tax)

    number_available = Product_information[5].get_text()
    Num_available.append(number_available)

    p_rating = soup.find(class_='col-sm-6 product_main').find_all('p')
    star = p_rating[2]['class']
    review_rating = star[1]
    ratings.append(review_rating)

# Dictionary containing all the details
d = {
        'title': Titles,
        'Product page url': Product_page_url,
        'Category': Categories,
        'Product Description': Product_DescriptionS,
        'Image url': Image_urlS,
        'review rating': ratings,
        'universal_product_code': upc,
        'price_excluding_tax': PExTax,
        'price_including_tax': PIncTax,
        'number_available': Num_available
    }

# Using the dictionary for the DataFrame and creating a csv file
Book_details = pd.DataFrame(d, index=[1])
print(Book_details)
Book_details.to_csv('booksScraping.csv')
