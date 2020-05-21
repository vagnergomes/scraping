import requests
website_url = requests.get('https://en.wikipedia.org/wiki/List_of_Asian_countries_by_area ') .text

from bs4 import BeautifulSoup

soup = BeautifulSoup(website_url, 'html.parser')
# print(soup)
my_table = soup.find('table', {'class': 'wikitable sortable'})
# print(my_table)

links = my_table.findAll('a')
# print(links)

countries = []
for link in links:
    countries.append(link.get('title'))

print(countries)

