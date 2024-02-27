import data as data
import requests
from bs4 import BeautifulSoup
import re
import csv


URL = "https://lectionary.library.vanderbilt.edu/daily-citationindex.php"
# URL = "https://lectionary.library.vanderbilt.edu/citationindex.php"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

prod_table = soup.find('table', class_='index')

prod_res = {}
if prod_table:
    # Find all <tr> elements within the table
    tr_elements = prod_table.find_all('tr')

    # Loop through the <tr> elements
    for tr in tr_elements:
        inner_tds = tr.find_all('td')

        if len(inner_tds) > 0:
            citation = inner_tds[0].text
            book = inner_tds[1]
            book_title = book.text.replace("--", "-")

            # Check if the book has a link
            temp_link = book.find_all('a')
            link_exists = ""
            if len(temp_link) > 0:
                link_exists = "Link"

            # Put row content in dictionary
            temp_res = {
                'citation': citation,
                'book_title': book_title,
                'link_exists': link_exists,
                'sorted_books': ''.join(sorted(re.sub(r'[^a-zA-Z0-9]', '', book_title)))
            }

            prod_res[citation] = temp_res

else:
    print("Table with class 'index' not found")


# URL = "http://localhost/rcl/daily-citations/"
# URL = "http://localhost/rcl/sunday-citation-test/"
URL = "http://localhost/rcl/daily-citation-test/"
# URL = "https://rclstaging.233analytics.com/daily-citations/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

dev_table = soup.find('table', id='slideshows-table')

dev_res = {}
if dev_table:
    # Find all <tr> elements within the table
    tr_elements = dev_table.find_all('tr')

    # Loop through the <tr> elements
    for tr in tr_elements:
        # Do something with each <tr> element
        # print(tr)
        inner_tds = tr.find_all('td')

        if len(inner_tds) > 0:
            citation = inner_tds[0].text
            book = inner_tds[1]
            book_title = book.text.replace("--", "-")
            # book_title = re.sub(r'\n', '', book_title)

            # print("citation => " + citation)
            # print("book => " + book_title)

            # Check if the book has a link
            temp_link = book.find_all('a')
            link_exists = ""
            if len(temp_link) > 0:
                link_exists = "Link"

            # Put row content in dictionary
            temp_res = {
                'citation': citation,
                'book_title': book_title,
                'link_exists': link_exists,
                'sorted_books': ''.join(sorted(re.sub(r'[^a-zA-Z0-9]', '', book_title)))
            }

            # dev_res.append(temp_res)
            dev_res[citation] = temp_res

perfect_match_count = 0
out_of_ordered = 0
books_are_wrong = 0

dev_wrong_books = {}
prod_wrong_books = {}

for prod_citation, prod_result in prod_res.items():

    if prod_citation in dev_res:
        dev_result = dev_res[prod_citation]

        # Check for perfect match
        if prod_result == dev_result:
            perfect_match_count = perfect_match_count + 1

        # Check up if books are all there but out of order
        if not prod_result['book_title'] == dev_result['book_title']:
            if prod_result['sorted_books'] == dev_result['sorted_books']:
                out_of_ordered = out_of_ordered + 1
            else:
                books_are_wrong = books_are_wrong + 1

                dev_wrong_books[dev_result['citation']] = dev_result['book_title']
                prod_wrong_books[prod_result['citation']] = prod_result['book_title']

    else:
        print(f"citation doesn't exist -> {prod_citation}")


print("============== WRONG BOOKS ===============")
csv_file = "C:/Users/MattHaslem/Desktop/233_Analytics/projects/rcl/temp/problems/daily_plugin_1_23_2024_9.csv"
issues = {}
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["citation", "PROD", "DEV"])

    for prod_citation, prod_value in prod_wrong_books.items():
        print(f"Prod => {prod_citation}")
        print(prod_value)
        print(f"DEV => {prod_citation}")
        print(dev_wrong_books[prod_citation])

        temp_issues = [prod_citation, prod_value, dev_wrong_books[prod_citation]]
        issues[prod_citation] = temp_issues



        writer.writerow([prod_citation, prod_value, dev_wrong_books[prod_citation]])
print("=========================================")
print(f"Perfect Matches => {perfect_match_count}")
print(f"Books out of order => {out_of_ordered}")
print(f"Books are wrong => {books_are_wrong}")
print("PROD COUNT => " + str(len(prod_res)))
print("DEV COUNT => " + str(len(dev_res)))

