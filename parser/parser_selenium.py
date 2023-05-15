from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Time, Boolean, LargeBinary
from sqlalchemy import cast
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from argparse import Action
from ast import Break
from re import sub
import string 
from typing import List 
import requests
from bs4 import BeautifulSoup  
from selenium.webdriver import Chrome 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service 

from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep 
import pandas as pd
import openpyxl
from io import BytesIO
from PIL import Image
from time import sleep

# Base = declarative_base()

# class InitScrapeAlmaty(Base):
#     __tablename__ = 'init_scrape_almaty'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     link_id = Column(String)
#     title = Column(String)
#     price = Column(String)
#     location = Column(String)
#     description = Column(String)
#     is_mortgaged = Column(Boolean)
#     seller = Column(String)
#     city = Column(String)
#     date_creation = Column(String)
#     num_views = Column(Integer)
#     is_hot = Column(Boolean)
#     is_paid_up = Column(Boolean)
#     is_hyped_turbo = Column(Boolean)
#     is_cold_entry = Column(Boolean)
#     num_pictures = Column(Integer)
#     # picture = Column(LargeBinary)

#     def create_table(self):
#         Base.metadata.create_all(engine)

options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging']) 
options.add_argument("start-maximized")

driver=Chrome(service=Service(ChromeDriverManager().install()),options=options)


PAGE_LIMIT = 1000  # really covers all 1000
#url like https://krisha.kz/prodazha/kvartiry/almaty/?page={page}

df = pd.DataFrame(columns=['id', 'title', 'price', 'location', 'description', 'is_mortgaged', 'seller', 'city', 'date_creation', 'num_views', 'is_hot', 'is_paid_up', 'is_hyped_turbo', 'is_cold_entry', 'num_pictures'])


# engine = create_engine(f'postgresql+psycopg2://postgres:Rokka228@localhost:5432/RSDiploma', \
#                        echo=False, future=True)
# InitScrapeAlmaty().create_table()
                     
# with Session(engine) as db:
try:
    for page in range(1, PAGE_LIMIT + 1):
        # try:
        print(page)
        driver.get(f'https://krisha.kz/prodazha/kvartiry/almaty/?page={page}')

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'main-col')))
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'a-card')))
        
        soup = BeautifulSoup(driver.page_source, 'lxml') 

        sales = soup.find('div','main-col').find('section', 'a-list a-search-list a-list-with-favs').find_all('div', 'a-card a-storage-live ddl_product ddl_product_link not-colored is-visible')
        for sale in sales:  
            id = sale.find('a', 'a-card__title')['href'].replace('/a/show/', '')
            title = sale.find('a', 'a-card__title').text

            price = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in sale.find('div', 'a-card__price').text).replace(" ", "")

                # distict = sale.find('div','a-card__subtitle').text.split(",")[0].replace(" ", "").replace('\n','')
            location = sale.find('div', 'a-card__subtitle').text.strip()


            description = sale.find('div', 'a-card__text-preview').text.strip()
            try:
                is_mortgaged = sale.find('div', 'a-card__text-preview').find('span', 'a-is-mortgaged').text == 'В залоге'
            except: 
                is_mortgaged = False    

            try:
                seller = sale.find('span', 'a-card__owner-label').find('div').text.strip()
            except: 
                seller = 'Новостройка'

            card_stats = sale.find_all('div','card-stats__item')
        
            city = card_stats[0].text
                
            date_creation = card_stats[1].text.strip()

            num_views = card_stats[2].find('span', 'a-view-count status-item').text.strip()

            labels = sale.find('div', 'paid-labels')
                
            is_hot = bool(labels.find('span', 'fi-paid-hot'))
            is_paid_up = bool(labels.find('span', 'fi-paid-up'))
            is_hyped_turbo = bool(labels.find('span', 'fi-paid-turbo'))

            cold_entry = bool(sale.find('div', 'a-card__complex-label') == 'Новостройка')

            num_pictures = sale.find('a', 'a-card__image')['data-nb']
            # url_picture = sale.find('picture', 'is-moderated has-photo')['data-full-src']
                
            # if url_picture != None:
            #     image = requests.get(url_picture).content
            # else: image = None

            # db.add(InitScrapeAlmaty(
            #     link_id = id,
            #     title = title,
            #     price = price,
            #     location = location,
            #     description = description,
            #     is_mortgaged = is_mortgaged,
            #     seller = seller,
            #     city = city,
            #     date_creation = date_creation,
            #     num_views = num_views,
            #     is_hot = is_hot,
            #     is_paid_up = is_paid_up,
            #     is_hyped_turbo = is_hyped_turbo,
            #     is_cold_entry = cold_entry,
            #     num_pictures = num_pictures,
            # ))
            # db.commit()
            # print('commited')
            df.loc[len(df)] = [id, title, price, location, description, is_mortgaged, seller, city, date_creation, num_views, is_hot, is_paid_up, is_hyped_turbo, cold_entry, num_pictures]
        print('added')
        sleep(5)  
except Exception as e:
    print('ERROR', e)
    

driver.close()
df.to_excel('../data/init_dataset_almaty2023_2.xlsx')
print('END')

