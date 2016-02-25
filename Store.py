# -*- coding:utf-8 -*-
import bs4
import requests
import requests.exceptions
import time
import IO
import re
from selenium import webdriver

class Store:
    def __init__(self):
        self.__drug_gswatsons = list()
        self.__drug_oliveyoung = list()

        self.__store_emart = list()
        self.__store_homeplus = list()
        
        self.__cvs_gs25 = list()

        self.__cafe_ediya = list()

        self.__fastfood_mac = list()

        self.__DEBUG = True
        self.__RETRIES = 10
        self.__TIMEOUT = 1.0
        self.__webdriver = None
        self.__SLEEPTIME = 2.0

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

        IO.writeJSON('drug_oliveyoung.json', self.__drug_oliveyoung)

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

            self.__drug_oliveyoung.append(item)

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
        IO.writeJSON('store_homeplus.json', self.__store_homeplus)

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
            print(req.content)
            self.__get_parsing_ediya(req.content)

        IO.writeJSON('cafe_ediya.json', self.__cafe_ediya)

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
            self.__cafe_ediya.append(item)
            print(item['StoreName'],item['StoreAddress'])

    def get_cvs_gs25(self):
        #driver = webdriver.Firefox()
        if self.__webdriver is None:
            self.__webdriver = webdriver.PhantomJS(executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')

        self.__get_gs25()
        self.__webdriver.close()
        IO.writeJSON('cvs_gs25.json', self.__cvs_gs25)

    def __get_gs25(self):
        url = 'http://gs25.gsretail.com/gscvs/ko/store-services/locations'
        self.__webdriver.get(url)
        self.__webdriver.find_element_by_link_text('마지막 페이지로 이동').click()
        time.sleep(self.__SLEEPTIME)
        lastpage = self.__get_cvs_gs25_lastpage(self.__webdriver.page_source)
        self.__webdriver.find_element_by_link_text('처음 페이지로 이동').click()
        time.sleep(self.__SLEEPTIME)

        for idx in range(int(lastpage)):
            print(idx+1,'page / ',lastpage)
            self.__get_parsing_gs25(self.__webdriver.page_source)
            self.__webdriver.find_element_by_link_text('다음 페이지로 이동').click()
            time.sleep(self.__SLEEPTIME)

    def __get_parsing_gs25(self, text):
        soup = bs4.BeautifulSoup(text, 'html.parser')
        table_border = soup.find('tbody', {'id': 'storeInfoList'})
        table_lists = table_border.findAll('tr')
        for store_list in table_lists:
            item = dict()
            item['StoreName'] = store_list.findAll('td')[0].find('a').text
            item['StoreAddress'] = store_list.findAll('td')[1].find('a').text
            self.__cvs_gs25.append(item)
            print(item['StoreName'],item['StoreAddress'])

    @staticmethod
    def __get_cvs_gs25_lastpage(text):
        soup = bs4.BeautifulSoup(text, 'html.parser')
        pagelist = soup.find('span', {'id': 'pagingTag'})

        return pagelist.findAll('a')[-1].text

    def get_drug_gswatsons(self):
        #driver = webdriver.Firefox()
        if self.__webdriver is None:
            self.__webdriver = webdriver.PhantomJS(executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')

        self.__get_gswatsons()
        self.__webdriver.close()
        IO.writeJSON('drug_gswatsons.json', self.__drug_gswatsons)

    def __get_gswatsons(self):
        url = 'http://watsons.gsretail.com/watsons/ko/market-info'
        self.__webdriver.get(url)
        self.__webdriver.find_element_by_link_text('마지막 페이지로 이동').click()
        time.sleep(self.__SLEEPTIME)
        lastpage = self.__get_drug_gswatsons_lastpage(self.__webdriver.page_source)
        self.__webdriver.find_element_by_link_text('처음 페이지로 이동').click()
        time.sleep(self.__SLEEPTIME)

        for idx in range(int(lastpage)):
            print(idx+1,'page / ',lastpage)
            self.__get_parsing_gswatsons(self.__webdriver.page_source)
            self.__webdriver.find_element_by_link_text('다음 페이지로 이동').click()
            time.sleep(self.__SLEEPTIME)

    def __get_parsing_gswatsons(self, text):
        soup = bs4.BeautifulSoup(text, 'html.parser')
        table_border = soup.find('div', {'id': 'searchList'})
        table_lists = table_border.findAll('li')
        for store_list in table_lists:
            item = dict()
            item['StoreName'] = store_list.find('p').text
            item['StoreAddress'] = store_list.findAll('strong')[1].nextSibling.replace(':','').strip()
            self.__drug_gswatsons.append(item)
            print(item['StoreName'],item['StoreAddress'])

    @staticmethod
    def __get_drug_gswatsons_lastpage(text):
        soup = bs4.BeautifulSoup(text, 'html.parser')
        pagelist = soup.find('span', {'class': 'num'})

        return pagelist.findAll('a')[-1].text

    def get_fastfood_mac(self, c1code):
        url = 'http://www.mcdonalds.co.kr/www/kor/findus/district.do?&sSearch_yn=Y&skey=2&skey1=&skey2=&skey4=&skey5=&skeyword2=&sflag1=&sflag2=&sflag3=&sflag4=&sflag5=&sflag6=&sflag=N&skeyword=&sSearch_yn=Y&skey=2&skey1=&skey2=&skeyword=&skey4=&skey5=&skeyword2=&sflag1=&sflag2=&sflag3=&sflag4=&sflag5=&sflag6=&sflag=N'
        r = requests.get(url)
        self.__get_parsing_mac(r.text, url)
        IO.writeJSON('fastfood_mac.json', self.__fastfood_mac)

    def __get_parsing_mac(self, text, url):
        soup = bs4.BeautifulSoup(text, "html.parser")
        lastpage = soup.find('a', {'class': 'btn_last'})['href'].split('&')[0].split('=')[-1]
        print(lastpage)

        for idx in range(int(lastpage)):
        #for idx in range(1):
            url_request = url + '&pageIndex=' + str(idx+1)
            print(idx+1)
            r = requests.get(url_request)
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            table_border = soup.find('ul', {'class': 'resultList'})
            table_lists = table_border.findAll('li')
            for store_list in table_lists:
                item = dict()
                item['StoreName'] = store_list.find('dt').text.strip()
                item['StoreCoordX'] = store_list.find('dt').find('a')['href'].split("'")[1]
                item['StoreCoordY'] = store_list.find('dt').find('a')['href'].split("'")[3]
                item['StoreAddress'] = re.sub("[\(\[].*?[\)\]]", "", store_list.find('dd', {'class': 'road'}).text)
                print(item['StoreName'],item['StoreAddress'])
                self.__fastfood_mac.append(item)

                '''
                utility_lists = store_list.find('dd', {'class': 'infoCheck'}).findAll('span')
                for utility in utility_lists:
                    flag = utility.find('img')
                    if flag:
                        print('yes')
                    else:
                        print('no')
                '''

