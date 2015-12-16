import bs4
import requests
import time
import copy

def getTick():
    return time.clock()

def getCortarNoC2(text):
    # target parsing context
    cortarNo_list = []
    soup = bs4.BeautifulSoup(text, "html.parser")

    #checking class2?
    address_list = soup.find('div', {"class" : "address_list  NE=a:lcl"})
    flagNumberStr = address_list.find('h3', {"class" : "area_tit"})
    span = flagNumberStr.find('span')
    if span is None:
        c1NameTable = soup.find('select', {"class" : "selectbox-source forload"})
        c1Name = c1NameTable.find('option', selected=True)

        table = soup.find('div', {"class" : "area scroll"})
        listItem = table.findAll('li')

        for i in range(len(listItem)):
            cortarNo = {}
            tmp = listItem[i].find('a')["onclick"]
            code = tmp.split('(',1)[1].split(')')[0].split("'",1)[1].split("'")[0]
            cortarNo["c1NameKR"] = c1Name.text
            cortarNo["nameKR"] = listItem[i].text
            cortarNo["code"] = code
            cortarNo_list.append(cortarNo)

    else:
        selectBox = soup.find('form', {"id" : "paramForm"})
        table = selectBox.find('input', {"id" : "cortarNo"})

        c1NameTable = soup.find('select', {"class" : "selectbox-source"})
        c1Name = c1NameTable.find('option', selected=True)

        cortarNo = {}
        cortarNo["c1NameKR"] = c1Name.text
        cortarNo["nameKR"] = c1Name.text
        cortarNo["code"] = table["value"]
        cortarNo_list.append(cortarNo)

    return cortarNo_list



def getc2List(c1_code):
    url1 = 'http://land.naver.com/article/cityInfo.nhn?rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=&cpId=&location=&siteOrderCode=&cortarNo='
    requests.adapters.DEFAULT_RETRIES = 2

    c2List = []
    for i in range(len(c1_code)):
        url = url1 + c1_code[i]
        try:
            r = requests.get(url, timeout = 5.0)
            cortarNoC2 = getCortarNoC2(r.text)
            for sub in cortarNoC2:
                c2ListSub = {}
                c2ListSub['c1Code'] = c1_code[i]
                c2ListSub['c1NameKR'] = sub['c1NameKR']
                c2ListSub['c2Code'] = sub['code']
                c2ListSub['c2NameKR'] = sub['nameKR']
                c2List.append(c2ListSub)
        except requests.exceptions.ConnectionError as e:
            print 're-requesting...'

    return c2List

def getCortarNoC3(text):
    cortarNo_list = []
    '''
    update....

    apt : apartment : A01
    oft : officetel : A02
    bun : bunyangkwon (selling in lots) : B01
    hos : ju-taeck (house) : C03
    lnd : to-ji (land) : E03
    onr : one-room : C01
    shp : sang-ga (shop) : D02
    ofc : sa-mu-sil (office) : D01
    fct : gong-jang (factory) : E02
    rdv : jae-gae-bal (redevelopment) : F01
    etc : keon-bul (building) : D03
    '''

    soup = bs4.BeautifulSoup(text, "html.parser")
    wrap = soup.find('div', {"id" : "wrap"})
    map_text = wrap.find('div', {"id" : "map"})
    map_viewer = map_text.find('div', {"class" : "map_viewer"})
    regionList = map_viewer.find('div', {"class" : "address_list  NE=a:lcl"})
    areaScroll = regionList.find('div', {"class" : "area scroll"})
    listItem = areaScroll.findAll('li')

    for i in range(len(listItem)):
        cortarNo = {}
        tmp = listItem[i].find('a')["onclick"]
        code = tmp.split('{',1)[1].split('}')[0].split(":")[1]

        cortarNo["c3NameKR"] = listItem[i].text.split("(")[0]
        cortarNo["count"] = listItem[i].text.split("(")[1].replace(")","")
        cortarNo["code"] = code
        cortarNo_list.append(cortarNo)

    return cortarNo_list

def getc3List(c2List, typeCode):
    c3List = []
    #typeCode = 'A02'
    requests.adapters.DEFAULT_RETRIES = 2
    url1 = 'http://land.naver.com/article/divisionInfo.nhn?cortarNo='
    url2 = '&rletNo=&rletTypeCd='
    url3 = '&tradeTypeCd=&hscpTypeCd='
    url4 = '%3AA03%3AA04&cpId=&location=&siteOrderCode='

    for subC2 in c2List:
        url = url1 + subC2['c2Code'] + url2 + typeCode + url3 + typeCode + url4
        print url
        try:
            r = requests.get(url, timeout=5.0)
            cortarNoC3 = getCortarNoC3(r.text)
            for subC3 in cortarNoC3:
                c3ListSub = {}
                c3ListSub['c1Code'] = subC2['c1Code']
                c3ListSub['c1NameKR'] = subC2['c1NameKR']
                c3ListSub['c2Code'] = subC2['c2Code']
                c3ListSub['c2NameKR'] = subC2['c2NameKR']
                c3ListSub['c3Code'] = subC3['code']
                c3ListSub['c3NameKR'] = subC3['c3NameKR']
                c3ListSub['count'] = subC3['count']
                c3List.append(c3ListSub)
        except requests.exceptions.ConnectionError as e:
            print 're-requesting...'

    return c3List

def getcortarNoC4(text):
    soup = bs4.BeautifulSoup(text, "html.parser")
    #wrap = soup.find('div', {"id" : "wrap"})
    #map = wrap.find('div', {"id" : "map"})
    #map_viewer = map.find('div', {"class" : "map_viewer"})
    #address_list = map_viewer.find('div', {"class" : "address_list  NE=a:lcl"})
    #map_tab = address_list.find('div', {"class" : "map_tab"})
    #first_tab = map_tab.find('ul', {"class" : "lst_tab"})
    #apt_on = first_tab.find('li', {"class" : "on"})
    scroll_list = soup.find('div', {"class" : "housing scroll"})
    listItem = scroll_list.findAll('li')

    cortarNo_list = []
    for i in range(len(listItem)):
        ### Check!!!
        cortarNo = {}
        tmp = listItem[i].text.split()[-1].replace("(","").replace(")","")
        strLen = len(tmp)
        sale = tmp[0:strLen-1].split('/')

        cortarNo['name'] = ' '.join(listItem[i].text.split()[0:-1])
        cortarNo['code'] = listItem[i].find('a')['hscp_no']
        cortarNo['mapx'] = listItem[i].find('a')['mapx']
        cortarNo['mapy'] = listItem[i].find('a')['mapy']
        cortarNo['sale_trade'] = int(sale[0])
        cortarNo['sale_lease'] = int(sale[1])
        cortarNo['sale_rent'] = int(sale[2])
        cortarNo['sale_total'] = int(sale[0]) + int(sale[1]) + int(sale[2])
        #print aptName['name'], aptName['sale_trade'], aptName['sale_lease'], aptName['sale_rent']
        ### Check!!!
        cortarNo_list.append(cortarNo)

    return cortarNo_list

def getc4List(c3List, typeCode):
    c4List = []
    url1 = 'http://land.naver.com/article/articleList.nhn?rletTypeCd='
    url2 = '&tradeTypeCd=&hscpTypeCd='
    url3 = '%3AA03%3AA04&cortarNo='
    requests.adapters.DEFAULT_RETRIES = 2

    for subC3 in c3List[0:466]:
        code = subC3['c3Code']
        url = url1 + typeCode + url2 + typeCode + url3 + code

        try:
            r = requests.get(url)
            cortarNoC4 = getcortarNoC4(r.text)

            for subC4 in cortarNoC4:
                c4ListSub = {}

                c4ListSub['c1Code'] = subC3['c1Code']
                c4ListSub['c1NameKR'] = subC3['c1NameKR']
                c4ListSub['c2Code'] = subC3['c2Code']
                c4ListSub['c2NameKR'] = subC3['c2NameKR']
                c4ListSub['c3Code'] = subC3['c3Code']
                c4ListSub['c3NameKR'] = subC3['c3NameKR']
                c4ListSub['count'] = subC3['count']

                c4ListSub['c4NameKR'] = subC4['name']
                c4ListSub['c4Code'] = subC4['code']
                c4ListSub['c4Mapx'] = subC4['mapx']
                c4ListSub['c4Mapy'] = subC4['mapy']
                c4ListSub['c4SaleTrade'] = subC4['sale_trade']
                c4ListSub['c4SaleLease'] = subC4['sale_lease']
                c4ListSub['c4SaleRent'] = subC4['sale_rent']
                c4ListSub['c4SaleTotal'] = subC4['sale_total']
                c4List.append(c4ListSub)

        except requests.exceptions.ConnectionError as e:
            print 're-requesting...'

    return c4List

def getc5List(c4List, typeCode):
    c5List = []
    requests.adapters.DEFAULT_RETRIES = 2

    for subC4 in c4List:
        c5ListSub = {}
        c5ListSubElement = []

        # 30 : 1 page has 30 lists
        nPage = subC4['c4SaleTotal'] / 30 + 1
        url1 = 'http://land.naver.com/article/articleList.nhn?rletTypeCd='
        url2 = '&tradeTypeCd=&rletNo='
        url3 = '&cortarNo='
        url4 = '&hscpTypeCd='
        url5 = '%3AA03%3AA04&mapX=&mapY=&mapLevel=&page='
        url6 = '&articlePage=&ptpNo=&rltrId=&mnex=&bildNo=&articleOrderCode=&cpId=&period=&prodTab=&atclNo=&atclRletTypeCd=&location=2520&bbs_tp_cd=&sort=&siteOrderCode=#_content_list_target'

        for i in range(nPage):
            url = url1 + typeCode + url2 + subC4['c4Code'] + url3 + subC4['c3Code'] + url4 + typeCode + url5 + unicode(i+1) + url6
            print url
            try:
                r = requests.get(url, timeout=10.0)
                getc5SubList(r.text, c5ListSubElement)

            except requests.exceptions.ConnectionError as e:
                print 're-requesting...'

        for subElement in c5ListSubElement:
            c5ListSub['c1Code'] = subC4['c1Code']
            c5ListSub['c1NameKR'] = subC4['c1NameKR']
            c5ListSub['c2Code'] = subC4['c2Code']
            c5ListSub['c2NameKR'] = subC4['c2NameKR']
            c5ListSub['c3Code'] = subC4['c3Code']
            c5ListSub['c3NameKR'] = subC4['c3NameKR']
            c5ListSub['count'] = subC4['count']

            c5ListSub['c4NameKR'] = subC4['c4NameKR']
            c5ListSub['c4Code'] = subC4['c4Code']
            c5ListSub['c4Mapx'] = subC4['c4Mapx']
            c5ListSub['c4Mapy'] = subC4['c4Mapy']
            c5ListSub['c4SaleTrade'] = subC4['c4SaleTrade']
            c5ListSub['c4SaleLease'] = subC4['c4SaleLease']
            c5ListSub['c4SaleRent'] = subC4['c4SaleRent']
            c5ListSub['c4SaleTotal'] = subC4['c4SaleTotal']

            c5ListSub['c5AptTradeType'] = subElement['class']
            c5ListSub['c5AptRegisterDate'] = subElement['date']
            c5ListSub['c5AptTradeFlag'] = subElement['tradeFlag']
            c5ListSub['c5AptComplexNameKR'] = subElement['complex']
            c5ListSub['c5AptAreaDisplay'] = subElement['area_display']
            c5ListSub['c5AptAreaSupply'] = subElement['area_supply']
            c5ListSub['c5AptNetArea'] = subElement['net_area']
            c5ListSub['c5AptBlock'] = subElement['block']
            c5ListSub['c5AptFloor'] = subElement['floor']
            c5ListSub['c5AptPrice'] = subElement['price']
            c5ListSub['c5AptBrokerStoreNameKR'] = subElement['store']
            c5ListSub['c5AptBrokerStoreTel'] = subElement['store_tel']
            c5ListSub['c5AptBrokerStoreCode'] = subElement['store_code']

            c5List.append(copy.deepcopy(c5ListSub))

    return c5List

def getc5SubList(text, c4SubList):

    soup = bs4.BeautifulSoup(text, "html.parser")
    wrap = soup.find('div', {"id" : "wrap"})
    container = wrap.find('div', {"id" : "container"})
    sale_info = container.find('div', {"class" : "sale_info"})
    table = sale_info.find('table', {"class" : "sale_list _tb_site_img NE=a:cpm"})

    try:
        listItem = table.findAll('tr')
    except AttributeError:
        print 'passing'
        return None

    num_list =  (len(listItem)-1)/2
    for i in range(num_list):
    #for i in range(1):
        targetIdx = (i+1) * 2 - 1
        subStr = listItem[targetIdx].findAll('div', {"class" : "inner"})
        subList = {}

        if len(subStr) == 8:
            subList['class'] = subStr[0].text
            subList['date'] = subStr[1].text.strip()
            subList['tradeFlag'] = ''.join(subStr[1].find('span')['class'])
            subList['complex'] = subStr[2].text.strip()
            subList['area_display'] = subStr[3].text.split()[0]
            subList['area_supply'] = subStr[3].text.split()[2]
            subList['net_area'] = subStr[3].text.split()[4]
            subList['block'] = subStr[4].text.strip()
            subList['floor'] = subStr[5].text.strip()
            subList['price'] = subStr[6].text.split()[0]
            subList['store'] = subStr[7].find('span')['title']
            subList['store_tel'] = subStr[7].find('span', {"class" : "tel"} ).text
            try:
                tmp = subStr[7].find('a').get('href')
                code = tmp.split('(',1)[1].split(')')[0].split("'",1)[1].split("'")[0]
            except AttributeError:
                code = 'NoCode'
            #vals = tmp.split('(',1)[1].split(')')[0]

            subList['store_code'] = code
            #print subList['class'],subList['date'],subList['complex'],subList['floor'],subList['tradeFlag']
            #c4SubList.append(subList)
        elif len(subStr) == 9:
            subList['class'] = subStr[0].text
            subList['date'] = subStr[1].text.strip()
            subList['tradeFlag'] = ''.join(subStr[1].find('span')['class'])
            subList['complex'] = subStr[3].find('a')['title']
            subList['area_display'] = subStr[4].text.split()[0]
            subList['area_supply'] = subStr[4].text.split()[2]
            subList['net_area'] = subStr[4].text.split()[4]
            subList['block'] = subStr[5].text.strip()
            subList['floor'] = subStr[6].text.strip()
            subList['price'] = subStr[7].text.split()[0]
            subList['store'] = subStr[8].find('span')['title']
            subList['store_tel'] = subStr[8].find('span', {"class" : "tel"} ).text
            try:
                tmp = subStr[8].find('a').get('href')
                code = tmp.split('(',1)[1].split(')')[0].split("'",1)[1].split("'")[0]
            except AttributeError:
                code = 'NoCode'
            subList['store_code'] = code
        print subList['class'],subList['date'],subList['complex'],subList['floor'],subList['tradeFlag']
        c4SubList.append(copy.deepcopy(subList))
