import pandas as pd
import requests
from bs4 import BeautifulSoup

r = requests.get('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')
soup = BeautifulSoup(r.content, 'html.parser')


Product_page_url = r.url

Title = soup.find('h1').get_text()


Category_a = soup.find(class_="breadcrumb").find_all('a')
Category = Category_a[2].string

Product_Description = soup.find(class_="sub-header").findNext('p').get_text()

src_txt = soup.find(class_='item active').img.get('src')
jpg = src_txt.split("../../")
Image_url = ('https://books.toscrape.com/'+jpg[1])


Product_information = soup.find(class_='table table-striped').find_all('td')

universal_product_code = Product_information[0].get_text()

price_excluding_tax = Product_information[2].get_text()

price_including_tax = Product_information[3].get_text()

number_available = Product_information[5].get_text()

p_rating = soup.find(class_='col-sm-6 product_main').find_all('p')
star = p_rating[2]['class']
review_rating = star[1]

d = {
     'title': Title,
     'Product page url': Product_page_url,
     'Category': Category,
     'Product Description': Product_Description,
     'Image url': Image_url,
     'review rating': review_rating,
     'universal_product_code': universal_product_code,
     'price_excluding_tax': price_excluding_tax,
     'price_including_tax': price_including_tax,
     'number_available': number_available
     }

Book_details = pd.DataFrame(d, index=[1])
print(Book_details)
Book_details.to_csv('bookDetails.csv')
