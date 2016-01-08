import bs4
import requests
from selenium import webdriver
import IO
import codecs
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
vil : villa
'''
realEstate_code = {'APT': 'A1A3A4',
                    'OFT': 'A6',
                    'BUN': 'A2A5A7',
                    'HOS': 'C4C9CFCG',
                    'VIL': 'CDCE',
                    'ONR': 'C1',
                    'LND': 'CC',
                    'SHP': 'C8',
                    'OFC': 'C5',
                    'BLD': 'C6C7CB',
                    'FCT': 'CA',
                    'RDV': 'B1'}


def getc1Code(realEstateCode):
    url1 = 'http://realestate.daum.net/maemul/area/*/'
    url2 = '/*/summary'
    url = url1 + realEstateCode + url2
    r = requests.get(url)

    c1List = getc1Parsing(r.text)

    return c1List


def getc1Parsing(text):
    item_list = []
    soup = bs4.BeautifulSoup(text, "html.parser")
    areaInfo = soup.find('div', {"class": "all"})
    areaCode = areaInfo.findAll('area')
    for item in areaCode:
        items = {}
        items["c1Code"] = item['data-code']
        items["c1NameKR"] = item['alt']
        items["c1Coords"] = item['coords']
        item_list.append(items)

    return item_list

def getc2Code(c1List, realEstateCode):
    url_list = []
    for subItem in c1List:
        url1 = 'http://realestate.daum.net/maemul/area/'
        c1code = subItem['c1Code']
        estatecode = realEstateCode
        url2 = '*/summary'
        url = url1 + c1code + '/' + estatecode + '/' + url2
        url_list.append(url)

    c2List = []
    for idx, url in enumerate(url_list):
        #r = requests.get(url)
        #subc2List = getc2Parsing(r.text)
        print url
        driver = webdriver.PhantomJS(executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')
        driver.get(url)

        if c1List[idx]['c1Code'] == '1320000':
            subItem = {}
            subItem['c1Code'] = c1List[idx]['c1Code']
            subItem['c1NameKR'] = c1List[idx]['c1NameKR']
            subItem['c1Coords'] = c1List[idx]['c1Coords']
            subItem['c2Code'] = c1List[idx]['c1Code']
            subItem['c2NameKR'] = c1List[idx]['c1NameKR']
            c2List.append(subItem)

        else:
            subc2List = getc2Parsing(driver.page_source)

            for item in subc2List:
                subItem = {}
                subItem['c1Code'] = c1List[idx]['c1Code']
                subItem['c1NameKR'] = c1List[idx]['c1NameKR']
                subItem['c1Coords'] = c1List[idx]['c1Coords']
                subItem['c2Code'] = item['c2Code']
                subItem['c2NameKR'] = item['c2NameKR']
                c2List.append(subItem)

    return c2List

def getc2Parsing(text):
    item_list = []
    soup = bs4.BeautifulSoup(text, "html.parser")
    list_estateinfo = soup.find('ul', {"class": "list_estateinfo list_estateinfo4"})
    c2Items = list_estateinfo.findAll('li')
    for item in c2Items:
        items = {}
        items['c2Code'] = item.find('a')['href'].split('/')[3].encode('ascii','ignore')
        items['c2NameKR'] = item.text

        item_list.append(items)

    return item_list

def getc3Code(c2List, realEstateCode):
    url_list = []
    for subItem in c2List:
        url1 = 'http://realestate.daum.net/maemul/area/'
        c1code = subItem['c2Code']
        estatecode = realEstateCode
        url2 = '*/summary'
        url = url1 + c1code + '/' + estatecode + '/' + url2
        url_list.append(url)

    c3List = []
    for idx, url in enumerate(url_list):
        print url
        #r = requests.get(url)
        #subc3List = getc3Parsing(r.text)

        driver = webdriver.PhantomJS(executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')
        driver.get(url)
        subc3List = getc3Parsing(driver.page_source)

        for item in subc3List:
            subItem = {}
            subItem['c1Code'] = c2List[idx]['c1Code']
            subItem['c1NameKR'] = c2List[idx]['c1NameKR']
            subItem['c2Code'] = c2List[idx]['c2Code']
            subItem['c2NameKR'] = c2List[idx]['c2NameKR']
            subItem['c3Code'] = item['code']
            subItem['c3NameKR'] = item['nameKR']
            subItem['c3Counts'] = item['counts']

            c3List.append(subItem)

    return c3List

def getc3Parsing(text):
    item_list = []
    soup = bs4.BeautifulSoup(text, "html.parser")
    list_estateinfo = soup.find('ul', {"class": "list_estateinfo"})
    c2Items = list_estateinfo.findAll('li')
    for item in c2Items:
        items = {}
        items['code'] = item.find('a')['href'].split('/')[3].encode('ascii','ignore')
        tmpStr = item.text
        tmpStrList = tmpStr.split()
        items['nameKR'] = tmpStrList[0]
        items['counts'] = tmpStrList[1].split()[-1].replace("(","").replace(")","").encode('ascii','ignore')

        item_list.append(items)

    return item_list

def getc4Code(c3Code, realEstateCode):
    url_list = []
    for subItem in c3Code:
        url1 = 'http://realestate.daum.net/maemul/area/'
        c1code = subItem['c3Code']
        estatecode = realEstateCode
        url2 = '*/summary'
        url = url1 + c1code + '/' + estatecode + '/' + url2
        url_list.append(url)

    c4Code = []
    for idx, url in enumerate(url_list[0:1]):
        print url
        #r = requests.get(url)
        driver = webdriver.PhantomJS(executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')
        driver.get(url)

        subc4List = getc4Parsing(driver.page_source)

        for item in subc4List:
            subItem = {}
            subItem['c1Code'] = c3Code[idx]['c1Code']
            subItem['c1NameKR'] = c3Code[idx]['c1NameKR']
            subItem['c2Code'] = c3Code[idx]['c2Code']
            subItem['c2NameKR'] = c3Code[idx]['c2NameKR']
            subItem['c3Code'] = c3Code[idx]['c3Code']
            subItem['c3NameKR'] = c3Code[idx]['c3NameKR']
            subItem['c3Counts'] = c3Code[idx]['c3Counts']
            subItem['c4Code'] = item['code']
            subItem['c4NameKR'] = item['nameKR']
            subItem['c4TradeCounts'] = item['tradeCounts']
            subItem['c4LeaseCounts'] = item['leaseCounts']
            subItem['c4RentCounts'] = item['rentCounts']

            c4Code.append(subItem)

    return c4Code

def getc4Parsing(text):
    item_list = []
    soup = bs4.BeautifulSoup(text, "html.parser")
    list_estateinfo = soup.find('div', {"class": "detale_sort detail_on"})
    c4Items = list_estateinfo.findAll('li')

    for item in c4Items:
        items = {}
        items['code'] = item.find('a')['href'].split('/')[3].encode('ascii','ignore')
        tmpStr = item.text
        tmpStrList = tmpStr.split()
        items['nameKR'] = tmpStrList[0]
        tmpCounts = tmpStrList[1].split()[-1].replace("(","").replace(")","").encode('ascii','ignore').split('/')
        items['tradeCounts'] = tmpCounts[0]
        items['leaseCounts'] = tmpCounts[1]
        items['rentCounts'] = tmpCounts[2]

        item_list.append(items)

    return item_list

def getc4List(c4Code, realEstateCode):

    url_list = []
    for subItem in c4Code:
        url1 = 'http://realestate.daum.net/iframe/maemul/DanjiMaemulList.daum?mcateCode='
        estateCode = realEstateCode
        url2 = '&saleTypeCode=*&tabName=maemullist&fullload=Y&isSection=Y&danjiId='
        c4code = subItem['c4Code']
        url = url1 + estateCode + url2 + c4code
        url_list.append(url)

    c4List = []
    for idx, url in enumerate(url_list[0:1]):
        totalCounts = int(c4Code[idx]['c4TradeCounts']) + int(c4Code[idx]['c4LeaseCounts']) + int(c4Code[idx]['c4RentCounts'])
        if totalCounts:
            #driver = webdriver.PhantomJS(executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')
            #driver.get(url)

            text = IO.loadPageSource('sample1.html')
            #subc4List = getc4ListParsing(driver.page_source)
            subc4List = getc4ListParsing(text)

def getc4ListParsing(text):
    item_list = []
    soup = bs4.BeautifulSoup(text, "html.parser")
    box_info_tbl_top = soup.find('div', {"class": "box_info_tbl_top"})

    countFlag = len(box_info_tbl_top)

    if countFlag == 3:
        for idx, listItem in enumerate(box_info_tbl_top):
            if idx == 1:
                subItemList = listItem.find('tbody').findAll('tr')

                nSubItem = len(subItemList)/3
                for i in xrange(1):
                    subItem = subItemList[i*3 + 0].findAll('td')

                    #volume = soup.findAll("span", {"id": "volume"})[0].string
                    sellingType = subItem[0].findAll("a", {"class": "link_txt"})[0].string
                    sellingDate = subItem[0].findAll("em", {"class": "txt_date"})[0].string

                    estateType = subItem[1].findAll("a", {"class": "link_txt"})[0].string
                    c3Name = subItem[1].findAll("a", {"class": "link_txt"})[1].string

                    #2 to do


                    #areaName = subItem[3].findAll("span", {"class": "tit_size"})
                    areaValue = subItem[3].findAll("span", {"class": "txt_size"})
                    supplyArea = areaValue[0].string
                    netArea = areaValue[1].string
                    declareArea = subItem[3].findAll("a", {"class": "link_txt"})[0].string

                    sellingPrice = subItem[4].findAll("a", {"class": "link_txt"})[0].string

                    estateComplex = subItem[5].findAll("a", {"class": "link_txt"})[0].string

                    estateFloor = subItem[6].text.replace('\n','').strip().split('/')[0]
                    estateTotalFloor = subItem[6].findAll("span", {"class": "txt_num"})[0].string

                    print subItem[7].find('a').get('href')
                    print subItem[7].text

                    #print '2'
                    #print subItemList[i*3 + 1]
                    #print '3'
                    #print subItemList[i*3 + 2]



    '''
    # drilling

    url1 = 'http://realestate.daum.net/iframe/maemul/DanjiMaemulList.daum?mcateCode=A1A3A4&saleTypeCode=*&tabName=maemullist&fullload=Y&isSection=Y&danjiId=4753'
    url2 = 'http://realestate.daum.net/iframe/maemul/DanjiMaemulList.daum?mcateCode=A1A3A4&saleTypeCode=*&tabName=maemullist&fullload=Y&isSection=Y&danjiId=11719'
    url3 = 'http://realestate.daum.net/iframe/maemul/DanjiMaemulList.daum?mcateCode=A1A3A4&saleTypeCode=*&tabName=maemullist&fullload=Y&isSection=Y&danjiId=1006562'
    driver = webdriver.PhantomJS(executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')
    driver.get(url3)

    soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
    '''
    '''
    theme maemul len(box_info_tbl_top) == 5
    index = 3
    non them maemul len(box_info_tbl_top) == 3
    index = 2

    info_tbl = soup.find('div', {"class": "box_info_tbl_top"})
    print len(info_tbl)
    for aa in info_tbl:
        print '###'
        print aa
    '''
    '''
    nodata = soup.find('div', {"class" : "box_no_data box_no_data_type_2"})
    if nodata is None:
        print 'None'

    else:
        print 'String'

    # drilling
    '''

flag = 0
debug = 1

if flag == 1:
    c1Code = getc1Code(realEstate_code['APT'])
    IO.writeJSON('c1Code.json', c1Code)

    c2Code = getc2Code(c1Code, realEstate_code['APT'])
    IO.writeJSON('c2Code.json', c2Code)

    c3Code = getc3Code(c2Code, realEstate_code['APT'])
    IO.writeJSON('c3Code.json', c3Code)

    c4Code = getc4Code(c3Code, realEstate_code['APT'])
    IO.writeJSON('c4Code.json', c4Code)

else:
    c1Code = IO.staticLoadJSON('2016-01-08-c1List.json')
    c2Code = IO.staticLoadJSON('2016-01-08-c2List.json')
    c3Code = IO.staticLoadJSON('2016-01-08-c3List.json')
    c4Code = IO.staticLoadJSON('2016-01-08-c4code.json')


c4List = getc4List(c4Code, realEstate_code['APT'])


if debug == 0:
    for aa in c4Code:
        print aa['c1Code'], aa['c2Code'],  aa['c3Code'], aa['c4Code'], aa['c1NameKR'], aa['c2NameKR'], aa['c3NameKR'], aa['c4NameKR'], aa['c4TradeCounts'], aa['c4LeaseCounts'], aa['c4RentCounts']
