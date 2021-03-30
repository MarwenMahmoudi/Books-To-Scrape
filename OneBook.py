import requests
from bs4 import BeautifulSoup
import csv


# write data to csv
def load_data(file_name, headers, titles, product_page_url, category, product_desc, img_url, upc, p_in_tax, p_ex_tax, rating, num_av):
    with open(file_name, 'w', encoding='utf-8',  newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(headers)
        for i in range(len(titles)):
            row = [titles[i], product_page_url[i], category[i], product_desc[i], img_url[i], upc[i], p_in_tax[i], p_ex_tax[i], rating[i], num_av[i]]
            writer.writerow(row)


# get all category links
def category_links(categories_list):
    url = 'https://books.toscrape.com/index.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    ul_tag = soup.find(class_='nav nav-list').find_all('a')
    for hrf in ul_tag[1:51]:
        hrf_att = hrf['href']
        category_link = "https://books.toscrape.com/" + hrf_att
        categories_list.append(category_link)


# get number of pages per category and books links
def books_urls(result):

    categories_list = []
    category_links(categories_list)
    for lin in categories_list:

        html = requests.get(lin)
        page = BeautifulSoup(html.content, 'html.parser')
        # pagination
        # get number of pages per category
        test = page.find(class_='current')
        if test is None:
            num_pages = 1
        else:
            page_indicator = page.find(class_='current').get_text().split()
            num_pages = int(page_indicator[3])

        html_split = lin.split("index")
        current_html = html_split[0]
        category_pages_links = []

        if num_pages == 1:
            category_pages_links.append(lin)
        else:
            for i in range(1, num_pages + 1):
                page_link = current_html + "page-" + str(i) + ".html"
                category_pages_links.append(page_link)

        # print(category_pages_links)
        sub_list = []
        for x in category_pages_links:
            html = requests.get(x)
            text = BeautifulSoup(html.content, 'html.parser')
            # get books links
            container = text.find_all(class_='image_container')

            for link in container:
                href_att = link.a['href']
                href_txt = href_att.split("../../..")
                book_link = "https://books.toscrape.com/catalogue" + href_txt[1]
                sub_list.append(book_link)
        # print(sub_list)
        result.append(sub_list)


# main
def main():
    result = []
    books_urls(result)
    for cat in result:
        # print(len(cat))
        headers = ["Title", "Product_page_url", "Category", "Product_description", "Image_url", "Upc",
                   "Price_including_tax", "Price_excluding_tax", "Rating", "Num_available"]
        titles = []
        product_desc = []
        category = []
        product_page_url = []
        img_url = []
        upc = []
        p_in_tax = []
        p_ex_tax = []
        rating = []
        num_av = []
        for i in range(len(cat)):
            url = cat[i]
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            product_page = page.url
            product_page_url.append(product_page)

            title = soup.find('h1').get_text()
            titles.append(title)

            category_a = soup.find(class_="breadcrumb").find_all('a')
            category_v = category_a[2].string
            category.append(category_v)

            product_description = soup.find(class_="sub-header").findNext('p').get_text()
            product_desc.append(product_description)

            src_txt = soup.find(class_='item active').img.get('src')
            part = src_txt.split("../../")
            image_url = ('https://books.toscrape.com/' + part[1])
            img_url.append(image_url)

            product_information = soup.find(class_='table table-striped').find_all('td')

            universal_product_code = product_information[0].get_text()
            upc.append(universal_product_code)

            price_excluding_tax = product_information[2].get_text()
            p_ex_tax.append(price_excluding_tax)

            price_including_tax = product_information[3].get_text()
            p_in_tax.append(price_including_tax)

            number_available = product_information[5].get_text()
            num_av.append(number_available)

            p_rating = soup.find(class_='col-sm-6 product_main').find_all('p')
            star = p_rating[2]['class']
            review_rating = star[1]
            rating.append(review_rating)

        csv_name = category_v + '.csv'
        load_data(csv_name, headers, titles, product_page_url, category, product_desc, img_url, upc, p_in_tax, p_ex_tax, rating, num_av)
        for j, lien in enumerate(img_url):
            response = requests.get(lien)
            image_name = category_v + str(j + 1) + '.jpg'
            with open(image_name, 'wb') as file:
                file.write(response.content)


main()
