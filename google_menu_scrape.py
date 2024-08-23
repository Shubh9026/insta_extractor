from bs4 import BeautifulSoup
import os
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException


def extract_data(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    foods=soup.find_all('div', class_='gq9CCd')
    prcs=soup.find_all('span', class_='fUcQpe Pip93e UxcJDf jI4Erf')
    title=soup.find('h2',class_="qrShPb pXs6bb PZPZlf q8U8x aTI8gc PPT5v").find("span").text.strip()
    subdic={}
    results = []
    dic={}
    for x,y in zip(foods,prcs):
       subdic[x.text.strip()]=y.text.strip()
    dic[title]=subdic
    results.append(dic)
    return results


def download_menu(url="https://www.google.com/search?client=ubuntu-sn&hs=e5c&sa=X&sca_esv=6eac42e19cef7bdf&sca_upv=1&channel=fs&tbs=lrf:!1m5!1u2!2m2!2m1!2e8!4e2!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3north_1indian_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3vegetarian_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!2m4!1e2!5m2!2m1!2e4!3sCg8SDXJhdGluZ19maWx0ZXIgASoCSU4,lf:1,lf_ui:9&tbm=lcl&sxsrf=ADLYWIIxzn5_2icTUpWgOFXdTE_Du1xQZA:1723641434662&q=top%20restaurants%20in%20lucknow&rflfq=1&num=10&ved=2ahUKEwi8meeo0fSHAxXY_DgGHb-nOkgQwywoBnoECAUQGA&biw=1366&bih=651&dpr=1&rlfi=hd:;si:&rlst=f"):
    sr=Service('/snap/bin/geckodriver')
    driver=webdriver.Firefox(service=sr)
    driver.get(url)
    time.sleep(5)
    
    links = driver.find_elements(By.CLASS_NAME, "vwVdIc.wzN8Ac.rllt__link.a-no-hover-decoration")
    if len(links)==0:
        print("Successfully extracted data")
        exit()
    for i in range(len(links)):
        links[i].click()
        time.sleep(5)
        menu_el=driver.find_element(by=By.XPATH,value='/html/body/div[2]/div/div[8]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/div[1]/g-sticky-content/div/div[1]/g-tabs/div/div/a[2]')
        menu_el.click()
        time.sleep(5)
        page_source=driver.page_source
        data=extract_data(page_source=page_source)
            
        csv_file = "restaurant_menu.csv"
        menu_ls= []

        for restaurant, menu in data[0].items():
                for food_name, price in menu.items():                   
                    menu_ls.append({
                        "restaurant": restaurant,
                        "food_name": food_name,
                        "price": price
                    })

        try:
            df = pd.read_csv(csv_file)
            new_df = pd.DataFrame(menu_ls)
            df = pd.concat([df, new_df], ignore_index=True)
            df = df.drop_duplicates()
            df = df.reset_index(drop=True)
            df.to_csv(csv_file, index=False)
            print("restaurant_menu.csv updated successfully.")

        except FileNotFoundError:
            fieldnames = ['restaurant', 'food_name', 'price']
            df = pd.DataFrame(columns=fieldnames)
            new_df = pd.DataFrame(menu_ls)
            df = pd.concat([df, new_df], ignore_index=True)
            df = df.drop_duplicates()
            df = df.reset_index(drop=True)
            df.to_csv(csv_file, index=False)
            print("CSV file 'restaurant_menu.csv' has been created successfully.")

        driver.back()
        time.sleep(5)
        if i==len(links)-1:
            driver.execute_script('window.scrollBy(0,document.body.scrollHeight)')
            next=driver.find_elements(By.ID,"pnnext")
            next.click()
            time.sleep(5)
          
   