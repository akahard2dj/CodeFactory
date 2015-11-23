import bs4
import requests
import json

#url = 'http://land.naver.com/article/cityInfo.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1100000000'
#r =

dongList = ['kangnam', 'kangdong', 'kangbuk', 'kangseo','kwanak','kwangjin','kuro','kuemchoen','noone','dobong',
            'dongdaemun','dongjak','mapo','seodaemun','seocho','seongdong','seongbuk','songpa','yangcheon',
            'youngdeungpo','yongsan','eunpyong','jongro','jung','jungrang']

def writeJSON(fname, apt_list):
    j = json.dumps(apt_list)
    with open(fname,'w') as f:
        f.write(j)
    f.close()

def get_cortarNoKu(str):
    cortarNo_list = []
    soup = bs4.BeautifulSoup(str, "html.parser")
    table = soup.find('div', {"class" : "area scroll"})
    list = table.findAll('li')

    for i in range(len(list)):
        cortarNo = {}
        tmp = list[i].find('a')["onclick"]
        code = tmp.split('(',1)[1].split(')')[0].split("'",1)[1].split("'")[0]
        cortarNo["name"] = list[i].text
        cortarNo["code"] = code
        cortarNo_list.append(cortarNo)

    return cortarNo_list

def get_cortarNoDong(str):
    cortarNo_list = []
    soup = bs4.BeautifulSoup(str, "html.parser")
    wrap = soup.find('div', {"id" : "wrap"})
    map = wrap.find('div', {"id" : "map"})
    map_viewer = map.find('div', {"class" : "map_viewer"})
    regionList = map_viewer.find('div', {"class" : "address_list  NE=a:lcl"})
    areaScroll = regionList.find('div', {"class" : "area scroll"})
    print areaScroll
    list = areaScroll.findAll('li')

    for i in range(len(list)):
        cortarNo = {}
        tmp = list[i].find('a')["onclick"]
        code = tmp.split('{',1)[1].split('}')[0].split(":")[1]

        cortarNo["name"] = list[i].text.split("(")[0]
        cortarNo["count"] = list[i].text.split("(")[1].replace(")","")
        cortarNo["code"] = code
        cortarNo_list.append(cortarNo)

    return cortarNo_list

def getcortarNoApt(str):
    soup = bs4.BeautifulSoup(str, "html.parser")
    wrap = soup.find('div', {"id" : "wrap"})
    map = wrap.find('div', {"id" : "map"})
    map_viewer = map.find('div', {"class" : "map_viewer"})
    address_list = map_viewer.find('div', {"class" : "address_list  NE=a:lcl"})
    map_tab = address_list.find('div', {"class" : "map_tab"})
    first_tab = map_tab.find('ul', {"class" : "lst_tab"})
    apt_on = first_tab.find('li', {"class" : "on"})
    scroll_list = first_tab.find('div', {"class" : "housing scroll"})
    list = scroll_list.findAll('li')

    aptName_list = []
    for i in range(len(list)):
        aptName = {}
        tmp = list[i].text.split()[1].replace("(","").replace(")","")
        strLen = len(tmp)
        sale = tmp[0:strLen-1].split('/')

        aptName['name'] = list[i].text.split()[0]
        aptName['code'] = list[i].find('a')['hscp_no']
        aptName['mapx'] = list[i].find('a')['mapx']
        aptName['mapy'] = list[i].find('a')['mapy']
        aptName['sale_trade'] = int(sale[0])
        aptName['sale_lease'] = int(sale[1])
        aptName['sale_rent'] = int(sale[2])
        aptName_list.append(aptName)

    return aptName_list

def getAptList(str, apt_list):

    soup = bs4.BeautifulSoup(str, "html.parser")

    wrap = soup.find('div', {"id" : "wrap"})
    container = wrap.find('div', {"id" : "container"})
    sale_info = container.find('div', {"class" : "sale_info"})
    table = sale_info.find('table', {"class" : "sale_list _tb_site_img NE=a:cpm"})
    list = table.findAll('tr')
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

f = file('gaepo.html','r')
s = f.read()
r = s.decode('utf-8')

#cortarNo_list = get_cortarNoKu(r)
'''
with open('city_ku.json','r') as f:
    cortarNo_list = json.load(f)

idx = 0
for cortarNo in cortarNo_list:
    url1 = 'http://land.naver.com/article/divisionInfo.nhn?cortarNo='
    url2 = '&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    code = cortarNo['code']
    url = url1 + code + url2
    print url
    r = requests.get(url)
    cortarNoDong = get_cortarNoDong(r.text)
    fout = dongList[idx] + '.json'
    writeJSON(fout, cortarNoDong)
    print idx, cortarNo['name']
    idx = idx + 1

for i in range(len(cortarNo_list)):
    fread = dongList[i] + '.json'

    with open(fread,'r') as f:
        list = json.load(f)

    for aa in list:
        print aa['name'], aa['count'], aa['code']
'''

#code = '1168010300'
#url = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cortarNo=' + code
#r = requests.get(url)

list = getcortarNoApt(r)

with open('kangnam.json','r') as f:
    listDong = json.load(f)

url1 = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=&rletNo='
url2 = '&cortarNo='
url3 = '&hscpTypeCd=A01%3AA03%3AA04&mapX=&mapY=&mapLevel=&page='
url4 = '&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=2520&bbs_tp_cd=&sort=&siteOrderCode=#_content_list_target'

totalSale = list[0]['sale_trade'] + list[0]['sale_lease'] + list[0]['sale_rent']
nPage = (totalSale / 30) + 1
print totalSale, nPage

aList = []
for i in range(nPage):
    if not totalSale == 0:
        url = url1 + list[1]['code'] + url2 + listDong[1]['code'] + url3 + unicode(i+1) + url4
        r = requests.get(url)
        getAptList(r.text, aList)

for aa in aList:
    print aa['price'], aa['class'], aa['date'], aa['complex'], aa['area_display'], aa['store'], aa['store_tel'], aa['store_code']
