import data as data
import requests
from bs4 import BeautifulSoup
import re
import csv

# Year A
URL = "https://rclstaging.233analytics.com/daily-readings/?y=17134"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

readings_sections = soup.find_all("div", {"class": "daily-readings"})

prod_res = {}
if readings_sections:
    for reading_section in readings_sections:
        # Find all <tr> elements within the table
        reading_elements = reading_section.find_all("div", {"class": "reading"})

        # Loop through the reading elements
        for reading_div in reading_elements:
            inner_links = reading_div.find_all('a')

            if len(inner_links) > 0:
                date_string = inner_links[0].find('p', {"class": "date"}).text.strip()
                verse_string = inner_links[0].find('p', {"class": "verse"}).text.strip()
                is_sunday = False
                liturgical_day = ""

                # If there's a complementary verse add it to the verse string
                comp_verse_element = reading_div.find('p', {"class": "complementary-verse"})
                if comp_verse_element:
                    verse_string += comp_verse_element.text.strip();

                # If there's a small element, it's a sunday and the verse
                small_element = reading_div.find('small')
                if small_element:
                    liturgical_day = verse_string
                    verse_string = small_element.text.strip()
                    is_sunday = True


                # print("Date => " + date_string)
                # print("Liturgical => " + liturgical_day)
                # print("verse => " + verse_string)

                temp_res = {
                    'liturgical_day': liturgical_day,
                    'verse_string': verse_string,
                    'is_sunday': is_sunday,
                    'sorted_verses': ''.join(sorted(re.sub(r'[^a-zA-Z0-9]', '', verse_string)))
                }

                prod_res[date_string] = temp_res


else:
    print("Table with class 'index' not found")

# local new Year A
URL = "http://localhost/rcl/daily-readings/?y=4928"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

readings_sections = soup.find_all("div", {"class": "daily-readings"})


dev_res = {}
if readings_sections:
    for reading_section in readings_sections:
        # Find all <tr> elements within the table
        reading_elements = reading_section.find_all("div", {"class": "reading"})

        # Loop through the reading elements
        for reading_div in reading_elements:
            inner_links = reading_div.find_all('a')


            if len(inner_links) > 0:
                date_string = inner_links[0].find('p', {"class": "date"}).text.strip()
                verse_string = inner_links[0].find('p', {"class": "verse"}).text.strip()
                is_sunday = False
                liturgical_day = ""

                # If there's a complementary verse add it to the verse string
                comp_verse_element = reading_div.find('p', {"class": "complementary-verse"})
                if comp_verse_element:
                    verse_string += comp_verse_element.text.strip();

                # If there's a small element, it's a sunday and the verse
                small_element = reading_div.find('small')
                if small_element:
                    liturgical_day = verse_string
                    verse_string = small_element.text.strip()
                    is_sunday = True

                temp_res = {
                    'liturgical_day': liturgical_day,
                    'verse_string': verse_string,
                    'is_sunday': is_sunday,
                    'sorted_verses': ''.join(sorted(re.sub(r'[^a-zA-Z0-9]', '', verse_string)))
                }

                dev_res[date_string] = temp_res


else:
    print("Table with class 'index' not found")

print("PROD => ")
print(prod_res)

print("DEV => ")
print(dev_res)

#
# perfect_match_count = 0
# out_of_ordered = 0
# books_are_wrong = 0
#
# dev_wrong_books = {}
# prod_wrong_books = {}
#
# for prod_citation, prod_result in prod_res.items():
#
#     if prod_citation in dev_res:
#         dev_result = dev_res[prod_citation]
#
#         # Check for perfect match
#         if prod_result == dev_result:
#             perfect_match_count = perfect_match_count + 1
#
#         # Check up if books are all there but out of order
#         if not prod_result['book_title'] == dev_result['book_title']:
#             if prod_result['sorted_books'] == dev_result['sorted_books']:
#                 out_of_ordered = out_of_ordered + 1
#             else:
#                 books_are_wrong = books_are_wrong + 1
#
#                 dev_wrong_books[dev_result['citation']] = dev_result['book_title']
#                 prod_wrong_books[prod_result['citation']] = prod_result['book_title']
#
#     else:
#         print(f"citation doesn't exist -> {prod_citation}")
#
#
# print("============== WRONG BOOKS ===============")
# csv_file = "C:/Users/MattHaslem/Desktop/233_Analytics/projects/rcl/temp/problems/daily_plugin_1_23_2024_9.csv"
# issues = {}
# with open(csv_file, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["citation", "PROD", "DEV"])
#
#     for prod_citation, prod_value in prod_wrong_books.items():
#         print(f"Prod => {prod_citation}")
#         print(prod_value)
#         print(f"DEV => {prod_citation}")
#         print(dev_wrong_books[prod_citation])
#
#         temp_issues = [prod_citation, prod_value, dev_wrong_books[prod_citation]]
#         issues[prod_citation] = temp_issues
#
#
#
#         writer.writerow([prod_citation, prod_value, dev_wrong_books[prod_citation]])
# print("=========================================")
# print(f"Perfect Matches => {perfect_match_count}")
# print(f"Books out of order => {out_of_ordered}")
# print(f"Books are wrong => {books_are_wrong}")
# print("PROD COUNT => " + str(len(prod_res)))
# print("DEV COUNT => " + str(len(dev_res)))

