import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_individual_yeast(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    def extract_detail(attribute_name):
        element = soup.find('h2', class_='table-title w-h2', text=lambda t: t and t.strip().startswith(attribute_name))
        return element.find_next('p').text.strip() if element else None

    beer_styles = soup.select('.beer_style li')
    suggested_beverages_and_styles = ', '.join([style_elem.text.strip() for style_elem in beer_styles])
    attenuation = extract_detail('ATTENUATION')
    flocculation = extract_detail('FLOCCULATION')
    alcohol_tolerance = extract_detail('ALCOHOL TOLERANCE')
    fermentation_temp = extract_detail('FERMENTATION TEMPERATURE')
    sta1 = extract_detail('STA1')

    return {
        'Attenuation': attenuation,
        'Flocculation': flocculation,
        'Alcohol Tolerance': alcohol_tolerance,
        'Fermentation Temperature': fermentation_temp,
        'STA1': sta1,
        'Suggested Beverages & Styles': suggested_beverages_and_styles
    }

scrape_individual_yeast('https://www.whitelabs.com/yeast-single?id=101&type=YEAST')


with open('yeast_data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    yeast_data_list = [row for row in reader]


for data in yeast_data_list:
    url = data['URL']
    details = scrape_individual_yeast(url)

    data.update(details)
    time.sleep(2)
with open('yeast_data2.csv', 'w', newline='') as csvfile:
    fieldnames = yeast_data_list[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in yeast_data_list:
        writer.writerow(data)




