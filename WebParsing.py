# -*- coding: utf-8 -*-
import requests
import bs4
import json
import re
import codecs
'''
def get_sector(code):
    url = 'http://finance.naver.com/item/main.nhn?code=' + code
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    sector = ""
    h4 = soup.find('h4', {'class':'h_sub sub_tit7'})
    if h4 is not None:
        sector = h4.a.text
    return sector

url = 'http://www.krx.co.kr/por_kor/popup/JHPKOR13008.jsp'
response = requests.post(url, data={'mkt_typ':'S','market_gubun':'kospiVal'})

soup = bs4.BeautifulSoup(response.text, "html.parser")
table = soup.find('table', {'id':'tbl1'})
trs = table.findAll('tr')

stock_list = []
for tr in trs[1:]:
    stock = {}
    cols = tr.findAll('td')
    stock['code'] = cols[0].text[1:]
    stock['name'] = unicode(cols[1].text.replace(":", ""))
    stock['full_code'] = cols[2].text
    stock['sector'] = get_sector(cols[0].text[1:])
    stock_list.append(stock)

j = json.dumps(stock_list)
with open('kospi.json','w') as f:
    f.write(j)
    '''
'''
url = 'http://fx.keb.co.kr/FER1101C.web'
r = requests.get(url)
soup = bs4.BeautifulSoup(r.text, "html.parser")
printArea = soup.find("div", {"id":"gridPosition"})

for data in printArea:
    print data
'''
#url = 'http://www.645lotto.net/lotto645Confirm.do?method=allWin'
#url = 'http://land.naver.com/article/articleList.nhn?rletNo=14&rletTypeCd=A01&tradeTypeCd=A1'
#r = requests.get(url)
#f = file('source.html','w')
#f.write(r.text.encode('utf-8'))
#f.close()
def writeJSON(fname, apt_list):
    j = json.dumps(apt_list)
    with open(fname,'w') as f:
        f.write(j)
    f.close()


def getList2(list):
    apt_list = []
    num_list =  (len(list)-1)/2
    for i in range(num_list):
    #for i in range(1):
        targetIdx = (i+1) * 2 - 1
        subStr = list[targetIdx].findAll('div', {"class" : "inner"})
        print i
        apt = {}
        if len(subStr) == 8:
            apt['class'] = subStr[0].text
            apt['date'] = subStr[1].text.strip()
            apt['complex'] = subStr[2].text.strip()
            apt['area_display'] = subStr[3].text.split()[0]
            apt['area_supply'] = subStr[3].text.split()[2]
            apt['net_area'] = subStr[3].text.split()[4]
            apt['block'] = subStr[4].text.strip()
            apt['floor'] = subStr[5].text.strip()
            apt['price'] = subStr[6].text.split()[0]
            apt['store'] = subStr[7].find('span')['title']
            apt['store_tel'] = subStr[7].find('span', {"class" : "tel"} ).text
            try:
                tmp = subStr[7].find('a').get('href')
                code = tmp.split('(',1)[1].split(')')[0].split("'",1)[1].split("'")[0]
            except AttributeError:
                code = 'NoCode'
            #vals = tmp.split('(',1)[1].split(')')[0]

            apt['store_code'] = code
            apt_list.append(apt)
        elif len(subStr) == 9:
            apt['class'] = subStr[0].text
            apt['date'] = subStr[1].text.strip()
            apt['complex'] = subStr[3].find('a')['title']
            apt['area_display'] = subStr[4].text.split()[0]
            apt['area_supply'] = subStr[4].text.split()[2]
            apt['net_area'] = subStr[4].text.split()[4]
            apt['block'] = subStr[5].text.strip()
            apt['floor'] = subStr[6].text.strip()
            apt['price'] = subStr[7].text.split()[0]
            apt['store'] = subStr[8].find('span')['title']
            apt['store_tel'] = subStr[8].find('span', {"class" : "tel"} ).text
            try:
                tmp = subStr[8].find('a').get('href')
                code = tmp.split('(',1)[1].split(')')[0].split("'",1)[1].split("'")[0]
            except AttributeError:
                code = 'NoCode'
            apt['store_code'] = code
            apt_list.append(apt)

    return apt_list


def getList(list):
    apt_list = []
    num_list =  (len(list)-1)/2
    for i in range(num_list):
        print i

        targetIdx = (i+1) * 2 - 1
        subStr = list[targetIdx].findAll('div', {"class" : "inner"})
        apt = {}
        apt['class'] = subStr[0].text
        apt['date'] = subStr[1].text.strip()
        apt['complex'] = subStr[2].text.strip()
        apt['area_display'] = subStr[3].text.split()[0]
        apt['area_supply'] = subStr[3].text.split()[2]
        apt['net_area'] = subStr[3].text.split()[4]
        apt['block'] = subStr[4].text.strip()
        apt['floor'] = subStr[5].text.strip()
        apt['price'] = subStr[6].text.split()[0]
        apt['store'] = subStr[7].find('span')['title']
        apt['store_tel'] = subStr[7].find('span', {"class" : "tel"} ).text
        tmp = subStr[7].find('a')['href']
        #vals = tmp.split('(',1)[1].split(')')[0]
        code = tmp.split('(',1)[1].split(')')[0].split("'",1)[1].split("'")[0]
        try:
            tmp = subStr[7].find('a').get('href')
            code = tmp.split('(',1)[1].split(')')[0].split("'",1)[1].split("'")[0]
        except AttributeError:
            code = 'NoCode'
        apt['store_code'] = code
        apt_list.append(apt)

f = file('source.html','r')
s = f.read()
r = s.decode('utf-8')

#soup = bs4.BeautifulSoup(r.text, "html.parser")
soup = bs4.BeautifulSoup(r, "html.parser")
table = soup.find('table', {"class" : "sale_list _tb_site_img NE=a:cpm"})
list = table.findAll('tr')

apt_list = getList2(list)
writeJSON('kayang.json',apt_list)


with open('kayang.json','r') as f:
    aptLoad_list = json.load(f)

for aa in aptLoad_list:
    print aa['price'], aa['class'], aa['date'], aa['complex'], aa['area_display'], aa['store'], aa['store_tel'], aa['store_code']

