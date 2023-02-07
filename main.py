import requests
import json
import os

from fake_useragent import UserAgent
from bs4 import BeautifulSoup

url = 'https://www.gorgany.com/sporiadzhennia/yizha-dlia-pokhodiv/batonchyky'

headers = {
    'UserAgent': UserAgent().msie
}
try:
    directory_name = input('Choose directory name: ')
    os.mkdir(directory_name)

except FileExistsError:
    print('Enter another name')

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, features='html.parser')
item_name_href_dict = {}
for item in soup.find_all('a', attrs={'class': 'product-item-link'}):
    item_name_href_dict[item.text.strip().replace(' ', '_')] = item.get('href').strip()


for item_name in item_name_href_dict.keys():
    r = requests.get(item_name_href_dict[item_name], headers=headers)
    item_html = BeautifulSoup(r.text, features='html.parser')
    data_html = item_html.find_all('script', attrs={'type': 'text/x-magento-init'})[9].text
    data = json.loads(data_html)
    c = data["[data-gallery-role=gallery-placeholder]"]["mage/gallery/gallery"]['data']
    count = 0
    os.mkdir(directory_name + '/' + item_name)
    for i in range(len(c)):
        count += 1
        req = requests.get(c[i]['full'], headers=headers)
        with open(f'{directory_name}/{item_name}/{count}.jpg', 'w+b') as file:
            file.write(req.content)

