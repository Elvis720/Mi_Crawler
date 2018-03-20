# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:32:08 2018

@author: sunginous
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import json
import time
import datetime

browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
wait = WebDriverWait(browser, 10)
userName = '15665518972'
passWord = '15665518972nn'
url = 'https://www.mi.com/'
urlGoods = 'https://item.mi.com/product/7528.html'
goods = '米家电磁炉'
startTime = '2018-01-18 09:59:58'
refreshTime = 1
cookies = ''


def search():
    print('执行用户名、密码登录')
    global cookies
    try:
        browser.get(url)
        login = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_userInfo > a:nth-child(1)'))
        )
        print(login.text)
        login.click()
        
        name = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#username'))
        )
        name.send_keys(userName)
        
        pwd = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pwd'))
        )
        pwd.send_keys(passWord)
        
        confirm = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#login-button'))
        )
        print(confirm.text)
        confirm.click()
        cookies += json.dumps(browser.get_cookies())
        #print(type(cookies))
        #print(json.loads(cookies))
        with open('cookie.json', 'w') as f:
            f.write(cookies)
    except TimeoutException:
        print('...........连接超时..........')
        return

def search_with_cookie():
    browser.delete_all_cookies()
    try:
        with open('cookie.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        for cookie in listCookies:
            browser.add_cookie(cookie)

        browser.get(urlGoods)
        print('用cookie登录的哦')
    except:
        print('cookie有误')
        search()

def buy():
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#search'))
        )
        input.clear()
        input.send_keys(goods)

        confirm = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_searchForm > input.search-btn.iconfont'))
        )
        confirm.click()

        #要改的主要是这里
        aimGoods = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div:nth-child(5) > div > div.goods-list-box > div > div:nth-child(2)'))
        )
        aimGoods.click()

        toBuy = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_headNav > div > div > div.right > a.btn.btn-small.btn-primary'))
        )
        toBuy.click()

    except WebDriverException or TimeoutException:
        search_with_cookie()

def order():
    try:
# =============================================================================
#         product = wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_list > div:nth-child(1) > ul > li.btn.btn-biglarge.active > a'))
#         )
#         product.click()
#         print('执行了1')
#         version = wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_list > div:nth-child(1) > ul > li.btn.btn-biglarge.active > a'))
#         )
#         version.click()
#         print('执行了2')
# =============================================================================
        shoppingCart = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_buyBtnBox > li > a'))
        )
        shoppingCart.click()
        print('执行了3')
        print(shoppingCart.text)
        if shoppingCart.text == '已设置到货通知' or shoppingCart.text == '到货通知':
            main(1)
        elif shoppingCart.text == '加入购物车':
            print('已加入购物车')
            return                    
    except WebDriverException or TimeoutException:
        search_with_cookie()
        
def main(page_num):
    for i in range(page_num):
        search_with_cookie()
        buy()
        order()
        time.sleep(refreshTime)
        browser.switch_to_window()
            

if __name__ == '__main__':
    start = datetime.datetime.now()
    stamp = '%Y-%m-%d %H:%M:%S'
    startTime = time.mktime(time.strptime(startTime, stamp))
    print(startTime)
    flag = 0
    while flag == 0:
        now = time.mktime(time.localtime())
        if now >= startTime:
            main(5)
            end = datetime.datetime.now()
            print(end-start)
            flag = 1