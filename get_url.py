from bs4 import BeautifulSoup
import requests
import time
import csv

base_url = 'https://www.whitelabs.com/yeast-bank?page={}'
yeast_data_list = []

for page_num in range(1, 11):
    response = requests.get(base_url.format(page_num))
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    yeast_blocks = soup.select('div.search-preview__header')

    for block in yeast_blocks:
        yeast_url = block.find('a')['href']
        yeast_name = block.find('h5').text
        yeast_code = block.find('p').text

        yeast_data_list.append({
            'Yeast Name': yeast_name,
            'Yeast Code': yeast_code,
            'URL': yeast_url
        })
        time.sleep(2)

with open('yeast_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Yeast Name', 'Yeast Code', 'URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in yeast_data_list:
        writer.writerow(data)