import requests
from bs4 import BeautifulSoup
import pandas as pd

PAGE_LIMIT = 1000  # really covers all
#url like https://krisha.kz/prodazha/kvartiry/almaty/?page={page}

# df = pd.DataFrame(columns='')
total_links = []
with open('./data/almaty_current_ids.txt','w') as f:
    for page in range(1, PAGE_LIMIT + 1):
        print(page)
        request = requests.get(f'https://krisha.kz/prodazha/kvartiry/almaty/?page={page}')
        soup = BeautifulSoup(request.text, 'lxml')
        vals = soup.find('section', 'a-search-list').find_all(attrs={'data-list-id':'main'})
        total_links.extend([val['data-id'] for val in vals])
        f.write('\n'.join(total_links)+'\n')

    