# -*- coding:utf-8 -*-
import bs4
import requests
import requests.exceptions
import time
import IO
from selenium import webdriver

class Store:
    def __init__(self):
        self.__store_oliveyoung = list()
        self.__store_emart = list()
        self.__store_homeplus = list()

        self.__cafe_ediya = list()

        self.__DEBUG = True
        self.__RETRIES = 10
        self.__TIMEOUT = 1.0
        self.__webdriver = None

    def get_oliveyoung(self):
        start_time = time.clock()
        url = 'http://www.oliveyoung.co.kr/store/store_list.asp'
        for i in range(1000):
            url_request = url + '?p=' + str(i)
            r = requests.get(url_request)
            print(url_request)
            flag_empty = self.__is_empty_oliveyoung(r.text)
            if flag_empty == True:
                break
            else:
                self.__get_parsing_oliveyoung(r.text)

        end_time = time.clock()

        IO.writeJSON('store_oliveyoung.json', self.__store_oliveyoung)

    @staticmethod
    def __is_empty_oliveyoung(text):
        soup = bs4.BeautifulSoup(text, "html.parser")
        table_border = soup.find('table', {'class': 'board_store_n mb30'})
        empty_message = table_border.find('td').text
        if empty_message == '등록된 매장이 없습니다':
            return True
        else:
            return False

    def __get_parsing_oliveyoung(self, text):
        soup = bs4.BeautifulSoup(text, "html.parser")
        table_border = soup.find('table', {'class': 'board_store_n mb30'})
        table_body = table_border.find('tbody')
        table_lists = table_body.findAll('tr')

        for store_list in table_lists:
            items = store_list.findAll('td')

            item = dict()
            item['StoreName'] = items[0].text
            item['StoreLink'] = items[0].find('a')['href']
            item['StoreRegion'] = items[1].text
            item['StoreAddress'] = items[2].text
            item['StoreSubway'] = items[3].text
            item['storeTel'] = items[4].text
            print(item['StoreName'], item['StoreRegion'])

            self.__store_oliveyoung.append(item)

    def get_emart(self):
        self.__webdriver = webdriver.PhantomJS(executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')

        url = 'https://store.emart.com/branch/list.do'
        r = requests.get(url)
        branch_url = self.__get_store_emart_branch(r.text)
        for sub_url in branch_url:
            print(sub_url)
            self.__get_parsing_emart(sub_url)

        self.__webdriver.close()
        IO.writeJSON('store_emart.json', self.__store_emart)

    def __get_parsing_emart(self, url):
        self.__webdriver.get(url)
        soup = bs4.BeautifulSoup(self.__webdriver.page_source, "html.parser")
        store_border = soup.find('div', {'class': 'store_intro '})

        item = dict()
        item['StoreName'] = store_border.find('h2').text
        item['StoreAddress'] = store_border.find('li', {'class': 'addr'}).text.split('\n')[1].strip()
        item['StoreLink'] = url
        print(item['StoreName'], item['StoreAddress'])

        self.__store_emart.append(item)

    @staticmethod
    def __get_store_emart_branch(text):
        soup = bs4.BeautifulSoup(text, "html.parser")
        store_border = soup.find('div', {'class': 'tab_wrap type13'})
        region_list = store_border.findAll('li')

        url_list = list()
        for region in region_list:
            char_href = region.find('a')['href']
            if char_href != '#':
                url_list.append('https://store.emart.com'+char_href)

        return url_list

    def get_homeplus(self):
        url = 'http://corporate.homeplus.co.kr/store/hypermarket.aspx?searchKeyword=all&searchRegionNo=&pageNo='
        for i in range(1000):
            url_request = url + str(i+1)
            r = requests.get(url_request)
            print(url_request)
            flag_empty = self.__is_empty_homeplus(r.text)
            if flag_empty:
                break
            else:
                self.__get_parsing_homeplus(r.text)
        IO.writeJSON('store_homeplus.json', self.__store_oliveyoung)

    @staticmethod
    def __is_empty_homeplus(text):
        soup = bs4.BeautifulSoup(text, "html.parser")
        table_border = soup.find('div', {'class': 'formTable'})
        empty_message = table_border.find('td').text
        if empty_message == '매장 정보가 없습니다.':
            return True
        else:
            return False

    def __get_parsing_homeplus(self, text):
        soup = bs4.BeautifulSoup(text, "html.parser")
        table_border = soup.find('div', {'class': 'formTable'})
        table_body = table_border.find('tbody')
        table_lists = table_body.findAll('tr')
        for store_list in table_lists:
            item = dict()
            item['StoreName'] = store_list.find('th').text
            item['StoreAddress'] = store_list.findAll('td')[0].text

            self.__store_homeplus.append(item)

    def get_cafe_ediya(self):
        url = 'http://www.ediya.com/board/listing/brd/store/page/1'
        r = requests.get(url)
        num_lastpage = self.__get_parsing_edity_lasgpage(r.text)

        for i in range(num_lastpage):
            url_request = 'http://www.ediya.com/board/listing/brd/store/page/' + str(i+1)
            req = requests.get(url_request)
            #print(req.headers['Content-type'])
            print(req.text.encode('utf-8'))
            self.__get_parsing_ediya(req.text)

    @staticmethod
    def __get_parsing_edity_lasgpage(text):
        soup = bs4.BeautifulSoup(text, "html.parser")
        paging_border = soup.find('div', {'class': 'paging'})
        a_lists = paging_border.findAll('a')
        last_page = int(a_lists[3]['href'].split('/')[-1])

        return last_page

    def __get_parsing_ediya(self, text):
        soup = bs4.BeautifulSoup(text, "html.parser")
        table_border = soup.find('table', {'class': 'list'})
        table_body = table_border.find('tbody')
        table_lists = table_body.findAll('tr')
        for sub_list in table_lists:
            item = dict()
            sub = sub_list.findAll('td')
            item['StoreName'] = sub[1].text
            item['StoreRegion'] = sub[0].text
            item['StoreAddress'] = sub[2].text
            print(item['StoreName'],item['StoreAddress'])

