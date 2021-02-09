import pandas as pd
import requests
from bs4 import BeautifulSoup

Home = requests.get("https://books.toscrape.com/index.html")
First = BeautifulSoup(Home.content, 'html.parser')


Category_books_links = []
Category_pages_links = []
# create a list of all categories links
Categories_list = []
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

ul_tag = First.find(class_='nav nav-list').find_all('a')
for hrf in ul_tag[1:51]:
    hrf_att = hrf['href']
    CategoryLink = "https://books.toscrape.com/"+hrf_att
    Categories_list.append(CategoryLink)
#print(Categories_list)

for lin in Categories_list:
    html = requests.get(lin)
    wrt = BeautifulSoup(html.content, 'html.parser')
    # pagination
    # get number of pages per category
    Test = wrt.find(class_='current')
    if Test == None:
       num_pages = 1
    else:
        page_indicator = wrt.find(class_='current').get_text().split()
        num_pages = int(page_indicator[3])
    print(num_pages)
    html_split = lin.split("index")
    current_html = html_split[0]
    for i in range(1, num_pages + 1):
        page_link = current_html + "page-" + str(i) + ".html"
        Category_pages_links.append(page_link)
    # print(Category_pages_list)
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
    # Here we got all the links of all the books of one category
    # Now we go to extract the details of books
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
Book_details = pd.DataFrame(data=d)
# print(Book_details)
Book_details.to_csv('booksScrapingFinal.csv', index=None)
