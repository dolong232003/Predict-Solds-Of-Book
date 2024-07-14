import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random

class ScrapeLazada:
    def scrape(self):
        url = 'https://www.lazada.vn/sach-tieng-viet-van-hoc/nxb-kim-dong--ipm-vi%E1%BB%87t-nam-123949007/?q=truy%E1%BB%87n'
        driver = webdriver.Chrome()
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#root")))
        time.sleep(2)

        products = []
        page_counter = 1
        while page_counter <= 1:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for item in soup.findAll('div', class_="Bm3ON"):
                product_name = item.find('div', class_="RfADt").text
                sale_off_element = item.find('span', class_='IcOsH')
                if sale_off_element:
                    sale_off = sale_off_element.text.replace('% Off', '')
                else:
                    sale_off = '0'

                price = item.find('span', class_="ooOxS").text.replace('₫', '').replace('.', '')

                rating_stars = len(item.findAll('i', class_='_9-ogB Dy1nx'))

                sold = ''
                span_elements = item.find_all('span', class_='_1cEkb')
                if span_elements:
                    for span_element in span_elements:
                        if 'Đã bán' in span_element.text:
                            sold = span_element.text.replace('Đã bán', '')
                            if span_element.text.replace('Đã bán', '') == '1k+ ':
                                sold = random.randint(1000,1500)
                            if span_element.text.replace('Đã bán', '') == '2k+ ':
                                sold = random.randint(2000,2500)
                            if span_element.text.replace('Đã bán', '') == '3k+ ':
                                sold = random.randint(3000,3500)
                else:
                    sold = '0'

                reviews_element = item.find('span', class_="qzqFw")
                reviews = reviews_element.text.strip('()') if reviews_element else "0"

                location = item.find('span', class_="oa6ri").text

                company = 'IPM Việt Nam'

                category = 'Sách Văn Học'

                products.append((product_name, company, category, sale_off, price, rating_stars, sold, reviews, location))
                

            time.sleep(5)

            next_button = driver.find_element(By.CSS_SELECTOR, ".ant-pagination-next > button")
            if not next_button.is_enabled() or page_counter == 1:
                break
            else:
                next_button.click()

                # Wait for the new page to load completely
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ant-pagination-next > button")))

            time.sleep(5)
            page_counter += 1

        df = pd.DataFrame(products, columns=['Product Name', 'Company', 'Category', 'Sale Off (%)', 'Price', 'Rating Stars', 'Sold', 'Review', 'Location'])

        print(df)

        df.to_excel('IPM Việt Nam, Sách Văn Học.xlsx', index=False)
        print('Data saved to local disk')

        driver.quit()


sl = ScrapeLazada()
sl.scrape()

