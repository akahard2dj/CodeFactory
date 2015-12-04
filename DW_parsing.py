import bs4
import requests
import time

def getTick():
    return time.clock()

def getCortarNoC2(str):
    # target parsing context
    cortarNo_list = []
    soup = bs4.BeautifulSoup(str, "html.parser")

    #checking class2?
    address_list = soup.find('div', {"class" : "address_list  NE=a:lcl"})
    flagNumberStr = address_list.find('h3', {"class" : "area_tit"})
    span = flagNumberStr.find('span')
    if span == None:
        c1NameTable = soup.find('select', {"class" : "selectbox-source forload"})
        c1Name = c1NameTable.find('option', selected=True)

        table = soup.find('div', {"class" : "area scroll"})
        list = table.findAll('li')

        for i in range(len(list)):
            cortarNo = {}
            tmp = list[i].find('a')["onclick"]
            code = tmp.split('(',1)[1].split(')')[0].split("'",1)[1].split("'")[0]
            cortarNo["c1NameKR"] = c1Name.text
            cortarNo["nameKR"] = list[i].text
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

def getCortarNoC3(str):
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

    soup = bs4.BeautifulSoup(str, "html.parser")
    wrap = soup.find('div', {"id" : "wrap"})
    map = wrap.find('div', {"id" : "map"})
    map_viewer = map.find('div', {"class" : "map_viewer"})
    regionList = map_viewer.find('div', {"class" : "address_list  NE=a:lcl"})
    areaScroll = regionList.find('div', {"class" : "area scroll"})
    list = areaScroll.findAll('li')

    for i in range(len(list)):
        cortarNo = {}
        tmp = list[i].find('a')["onclick"]
        code = tmp.split('{',1)[1].split('}')[0].split(":")[1]

        cortarNo["c3NameKR"] = list[i].text.split("(")[0]
        cortarNo["count"] = list[i].text.split("(")[1].replace(")","")
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
