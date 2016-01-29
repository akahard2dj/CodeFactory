# -*- coding: utf-8 -*-
import bs4
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import platform
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


def getc1Code(realEstateCode, drvier):
    url1 = 'http://realestate.daum.net/maemul/area/*/'
    url2 = '/*/summary'
    url = url1 + realEstateCode + url2
    # r = requests.get(url)
    driver.get(url)

    # c1List = getc1Parsing(r.text)
    c1List = getc1Parsing(driver.page_source)

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


def getc2Code(c1List, realEstateCode, driver):
    url_list = []
    for subItem in c1List:
        url1 = 'http://realestate.daum.net/maemul/area/'
        c1code = subItem['c1Code']
        estatecode = realEstateCode
        url2 = '*/summary'
        url = url1 + c1code + '/' + estatecode + '/' + url2
        url_list.append(url)
    '''
    for idx, url in enumerate(url_list):
        nAttemps = 0
        successFlag = False
        while (nAttemps < 5):
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(10)
            try:
                driver.get(url)
                print 'c3GetCode: %s requesting...' % (url),
                subc3List = getc3Parsing(driver.page_source)

                for item in subc3List:

                successFlag = True
                print 'Done'
                break
            except TimeoutException as e:
                nAttemps += 1
                print '[%s] Retry to connect ... %d/%d' % (e.message, nAttemps+1, 5)

            if successFlag == False:
                pendingUrlList.append(url)
    '''
    c2List = []

    pendingUrlList = []
    for idx, url in enumerate(url_list):
        nAttempts = 0
        successFlag = False

        while (nAttempts < 5):
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(10)
            try:
                driver.get(url)
                print 'c2GetCode: %s requesting...' % (url),

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

                successFlag = True
                print 'Done'
                break

            except TimeoutException as e:
                print 'Retry to connect ... %d/%d' % (nAttempts + 1, 5)
                nAttempts += 1

            if successFlag == False:
                pendingUrlList.append(url)

    return c2List


def getc2Parsing(text):
    item_list = []
    soup = bs4.BeautifulSoup(text, "html.parser")
    list_estateinfo = soup.find('ul', {"class": "list_estateinfo list_estateinfo4"})
    c2Items = list_estateinfo.findAll('li')
    for item in c2Items:
        items = {}
        items['c2Code'] = item.find('a')['href'].split('/')[3].encode('ascii', 'ignore')
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

    pendingUrlList = []
    # driver = webdriver.PhantomJS(executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')
    for idx, url in enumerate(url_list):
        nAttemps = 0
        successFlag = False
        while (nAttemps < 5):
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(10)

            try:
                driver.get(url)
                print 'c3GetCode: %s requesting...' % (url),
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
                successFlag = True
                print 'Done'
                break
            except TimeoutException as e:
                nAttemps += 1
                print '[%s] Retry to connect ... %d/%d' % (e.message, nAttemps + 1, 5)

            if successFlag == False:
                pendingUrlList.append(url)

    return c3List


def getc3Parsing(text):
    item_list = []
    soup = bs4.BeautifulSoup(text, "html.parser")
    list_estateinfo = soup.find('ul', {"class": "list_estateinfo"})
    c2Items = list_estateinfo.findAll('li')
    for item in c2Items:
        items = {}
        items['code'] = item.find('a')['href'].split('/')[3].encode('ascii', 'ignore')
        tmpStr = item.text
        tmpStrList = tmpStr.split()
        items['nameKR'] = tmpStrList[0]
        items['counts'] = tmpStrList[1].split()[-1].replace("(", "").replace(")", "").encode('ascii', 'ignore')

        item_list.append(items)

    return item_list


def getc4Code(c3Code, realEstateCode, driver):
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
        # r = requests.get(url)
        #driver = webdriver.PhantomJS(
        #    executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')
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
        items['code'] = item.find('a')['href'].split('/')[3].encode('ascii', 'ignore')
        tmpStr = item.text
        tmpStrList = tmpStr.split()
        items['nameKR'] = tmpStrList[0]
        tmpCounts = tmpStrList[1].split()[-1].replace("(", "").replace(")", "").encode('ascii', 'ignore').split('/')
        items['tradeCounts'] = tmpCounts[0]
        items['leaseCounts'] = tmpCounts[1]
        items['rentCounts'] = tmpCounts[2]

        item_list.append(items)

    return item_list

def getc4List(c4Code, realEstateCode, driver):
    url_list = []
    for subItem in c4Code:
        nTotalSales = int(subItem['c4TradeCounts']) + int(subItem['c4LeaseCounts']) + int(subItem['c4RentCounts'])
        if nTotalSales:
            url1 = 'http://realestate.daum.net/iframe/maemul/DanjiMaemulList.daum?mcateCode='
            realEstateCode = realEstateCode
            url2 = '&saleTypeCode=*&isSection=Y&fullload=Y&tabName=maemullist&danjiId='
            c4code = subItem['c4Code']
            url = url1 + realEstateCode + url2 + c4code
            url_list.append(url)

    for idx, url in enumerate(url_list):
        driver.get(url)
        print url
        getc4ListParsing(url, driver.page_source, driver)


def getc4List2(c4Code, realEstateCode, driver):
    url_list = []
    for subItem in c4Code:
        url1 = 'http://realestate.daum.net/iframe/maemul/DanjiMaemulList.daum?mcateCode='
        realEstateCode = realEstateCode
        url2 = '&saleTypeCode=*&isSection=Y&fullload=Y&tabName=maemullist&danjiId='
        c4code = subItem['c4Code']

        url = url1 + realEstateCode + url2 + c4code
        url_list.append(url)

    c4List = []
    for idx, url in enumerate(url_list[0:1]):
        driver.get(url)
        # loading web address of maemul/sise/danji/photo/danjiSize/Tax/New/Comm
        item_tablist = getc4ListTabAdd(driver.page_source)

        totalCounts = int(c4Code[idx]['c4TradeCounts']) + int(c4Code[idx]['c4LeaseCounts']) + int(
                c4Code[idx]['c4RentCounts'])

        if totalCounts:
            pageIdx = 1
            validFlag = True

            while (validFlag == True):
                pageUrl = url + '&page=' + str(pageIdx)
                driver.get(pageUrl)
                validFlag = isValidSales(driver.page_source)
                if validFlag == True:
                    subc4list = getc4ListParsing(driver.page_source)
                    pageIdx += 1


def getc4ListTabAdd(text):
    soup = bs4.BeautifulSoup(text, "html.parser")
    tab_list_text = soup.find('div', {'class': 'tab_maemularea2 exclude_crawl'})

    tab_list = tab_list_text.findAll('li')
    tablist = []
    for tab in tab_list:
        sublist = []
        tabaddress = 'http://realestate.daum.net' + tab.find('a').get('href')
        tabname = tab.text.strip().replace(" ", "")
        sublist.append(tabaddress)
        sublist.append(tabname)
        tablist.append(sublist)

    return tablist


def isValidSales(text):
    soup = bs4.BeautifulSoup(text, "html.parser")
    nodata = soup.find('div', {"class": "box_no_data box_no_data_type_2"})

    if nodata is None:
        return True
    else:
        return False


def getc4ListParsing(url, text, driver):
    item_list = []
    soup = bs4.BeautifulSoup(text, "html.parser")
    box_info_tbl_top = soup.find('div', {"class": "box_info_tbl_top"})

    for idx, listItem in enumerate(box_info_tbl_top):
        if idx % 2 == 1:
            title_theme = listItem.find('h3', {"class": "tit_theme"})
            if title_theme.text == '테마매물'.decode('utf-8'):
                getc4ListParsingThemeMaemul(listItem, title_theme.text, driver)

            if title_theme.text == '추천매물'.decode('utf-8'):
                getc4ListParsingRecommMaemul(url, listItem, title_theme.text)

            if title_theme.text == '일반매물'.decode('utf-8'):
                getc4ListParsingGeneralMaemul(url, listItem, title_theme.text)

            if title_theme.text == '한국공인중개사협회매물'.decode('utf-8'):
                getc4ListParsingAgencyMaemul(url, listItem, title_theme.text)

def getc4ListParsing3Indexing(bs4List, titleName):
    subItemList = bs4List.find('tbody').findAll('tr')
    nSubItem = len(subItemList) / 3
    for i in xrange(nSubItem):
        subItem = subItemList[i * 3 + 0].findAll('td')

        # td 1
        sellingType = subItem[0].findAll("a", {"class": "link_txt"})[0].string
        try:
            sellingDate = subItem[0].findAll("em", {"class": "txt_date"})[0].string
        except IndexError:
            sellingDate = subItem[0].findAll("a")[1].string

        # td 2
        estateType = subItem[1].findAll("a", {"class": "link_txt"})[0].string
        c3Name = subItem[1].findAll("a", {"class": "link_txt"})[1].string

        # td 3
        estateNameKR = subItem[2].findAll("a", {"class": "link_apt"})[0].string

        # td 4
        areaValue = subItem[3].findAll("span", {"class": "txt_size"})
        supplyArea = areaValue[0].string
        netArea = areaValue[1].string
        declareArea = subItem[3].findAll("a", {"class": "link_txt"})[0].string
        declareTypeArea = declareArea.split('/')[0]

        # td 5
        sellingPrice = subItem[4].findAll("a", {"class": "link_txt"})[0].string
        # sellingPriceChangeIndex
        # 0 : unchagned
        # 1 : increased
        # -1 : decreased
        sellingPriceChangeIndex = 0
        sellingPriceBefore = sellingPrice
        sellingPriceChange = 0
        sellingPriceDate = sellingDate
        sellingPriceDateChange = sellingDate
        if sellingPrice is None:
            flagNameKR = subItem[4].findAll("span", {"class": "screen_out"})[0].text
            if flagNameKR == '매물가격 상승'.decode('utf-8'):
                attrName = 'ico_price ico_up'
                sellingPriceChangeIndex = 1
            if flagNameKR == '매물가격 하락'.decode('utf-8'):
                attrName = 'ico_price ico_down'
                sellingPriceChangeIndex = -1

            sellingPrice = subItem[4].findAll("span", {"class": attrName})[0].text.replace(flagNameKR, "").strip()

            priceChangeTag = subItem[4].findAll("span", {"class": "box_txt"})

            sellingPriceDateChange = priceChangeTag[1].text.split()[1]
            sellingPriceBefore = priceChangeTag[1].text.split()[2].replace("가격".decode('utf-8'),"")
            sellingPriceChange = subItem[4].findAll("span", {"class": "box_fluctuate"})[0].text.replace(flagNameKR, "").split()[1]


        # td 6
        estateComplex = subItem[5].findAll("a", {"class": "link_txt"})[0].string

        # td 7
        estateFloor = subItem[6].text.replace('\n', '').strip().split('/')[0]
        estateTotalFloor = subItem[6].findAll("span", {"class": "txt_num"})[0].string

        # td 8
        # to be needed refining a parsing tech.
        #try:
        #    contactLink = subItem[7].find("a")['href']
        #    contactNumber = subItem[7].findAll("a")[1].text
        #except TypeError:
        #    contactLink = 'none'
        #    contactNumber = subItem[7].find("span", {"class": "link_txt"}).text

        #try:
        #    contactNumber = subItem[7].findAll("a")[1].text
        #except IndexError:
        #    contactNumber = subItem[7].find("span", {"class": "link_txt"}).text


        subItem = subItemList[i * 3 + 1].findAll('td')
        # td 1
        estateDescList_text = subItem[0].find('span', {"class": "box_desc"})
        estateDescList = estateDescList_text.findAll("span")
        ## TBD

        print titleName, estateNameKR, sellingDate, sellingType, sellingPrice, i

def getc4ListParsingThemeMaemul(bs4List, titleName, driver):

    detailbtn = bs4List.find('div', {"class": "box_detailbtn"})
    title_theme = bs4List.find('h3', {"class": "tit_theme"})

    if title_theme.text == '테마매물'.decode('utf-8'):
        if detailbtn is None:
            getc4ListParsing3Indexing(bs4List, titleName)

        else:
            detailUrl = 'http://realestate.daum.net' + detailbtn.find("a")['href']

            pageIdx = 1
            validFlag = True

            while (validFlag == True):
                pageUrl = detailUrl + '&page=' + str(pageIdx)
                driver.get(pageUrl)
                validFlag = isValidSales(driver.page_source)
                if validFlag == True:
                    print validFlag, pageUrl
                    soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
                    box_info_tbl_top = soup.find('div', {"class": "box_info_tbl_top"})
                    getc4ListParsing3Indexing(box_info_tbl_top, titleName)
                    pageIdx += 1
    if title_theme.text == '한국공인중개사협회매물'.decode('utf-8'):
        getc4ListParsingAgencyMaemul(bs4List, title_theme.text)


def getc4ListParsingGeneralMaemul(url, bs4List, titleName):
    getc4ListParsing3Indexing(bs4List, titleName)

    pageWrap = bs4List.find('div', {"id": "pageWrap"})

    if pageWrap:
        pageIdx = 2
        validFlag = True

        while (validFlag == True):
            pageUrl = url + '&page=' + str(pageIdx)
            driver.get(pageUrl)
            validFlag = isValidSales(driver.page_source)
            if validFlag == True:
                print validFlag, pageUrl
                soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
                box_info_tbl_top = soup.find('div', {"class": "box_info_tbl_top"})
                title_theme = box_info_tbl_top.findAll('h3', {"class": "tit_theme"})
                box_info_tbl = box_info_tbl_top.findAll('div', {"class": "box_info_tbl"})

                for i in xrange(len(title_theme)):
                    tableTitleName = title_theme[i].text
                    if tableTitleName == '추천매물'.decode('utf-8'):
                        getc4ListParsing3Indexing(box_info_tbl[i], tableTitleName)
                    if tableTitleName == '일반매물'.decode('utf-8'):
                        getc4ListParsing3Indexing(box_info_tbl[i], tableTitleName)
                    elif tableTitleName == '한국공인중개사협회매물'.decode('utf-8'):
                        getc4ListParsing3Indexing(box_info_tbl[i], tableTitleName)
                pageIdx += 1

def getc4ListParsingRecommMaemul(url, bs4List, titleName):
    getc4ListParsing3Indexing(bs4List, titleName)

    pageWrap = bs4List.find('div', {"id": "pageWrap"})

    if pageWrap:
        pageIdx = 2
        validFlag = True

        while (validFlag == True):
            pageUrl = url + '&page=' + str(pageIdx)
            driver.get(pageUrl)
            validFlag = isValidSales(driver.page_source)
            if validFlag == True:
                print validFlag, pageUrl
                soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
                box_info_tbl_top = soup.find('div', {"class": "box_info_tbl_top"})
                title_theme = box_info_tbl_top.findAll('h3', {"class": "tit_theme"})
                box_info_tbl = box_info_tbl_top.findAll('div', {"class": "box_info_tbl"})

                for i in xrange(len(title_theme)):
                    tableTitleName = title_theme[i].text
                    if tableTitleName == '추천매물'.decode('utf-8'):
                        getc4ListParsing3Indexing(box_info_tbl[i], tableTitleName)
                    if tableTitleName == '일반매물'.decode('utf-8'):
                        getc4ListParsing3Indexing(box_info_tbl[i], tableTitleName)
                    elif tableTitleName == '한국공인중개사협회매물'.decode('utf-8'):
                        getc4ListParsing3Indexing(box_info_tbl[i], tableTitleName)
                pageIdx += 1


def getc4ListParsingAgencyMaemul(url, bs4List, titleName):
    getc4ListParsing3Indexing(bs4List, titleName)

    pageWrap = bs4List.find('div', {"id": "pageWrap"})

    if pageWrap:
            pageIdx = 2
            validFlag = True

            while (validFlag == True):
                pageUrl = url + '&page=' + str(pageIdx)
                driver.get(pageUrl)
                validFlag = isValidSales(driver.page_source)
                if validFlag == True:
                    print validFlag, pageUrl
                    soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
                    box_info_tbl_top = soup.find('div', {"class": "box_info_tbl_top"})
                    title_theme = box_info_tbl_top.findAll('h3', {"class": "tit_theme"})
                    box_info_tbl = box_info_tbl_top.findAll('div', {"class": "box_info_tbl"})

                    for i in xrange(len(title_theme)):
                        tableTitleName = title_theme[i].text
                        if tableTitleName == '추천매물'.decode('utf-8'):
                            getc4ListParsing3Indexing(box_info_tbl[i], tableTitleName)
                        if tableTitleName == '일반매물'.decode('utf-8'):
                            getc4ListParsing3Indexing(box_info_tbl[i], tableTitleName)
                        elif tableTitleName == '한국공인중개사협회매물'.decode('utf-8'):
                            getc4ListParsing3Indexing(box_info_tbl[i], tableTitleName)
                    pageIdx += 1



flag = 1
debug =1

if flag == 0:
    driver = webdriver.PhantomJS(
        executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')
    c1Code = getc1Code(realEstate_code['APT'], driver)
    IO.writeJSON('c1Code.json', c1Code)

    c2Code = getc2Code(c1Code, realEstate_code['APT'], driver)
    IO.writeJSON('c2Code.json', c2Code)

    c3Code = getc3Code(c2Code, realEstate_code['APT'])
    IO.writeJSON('c3Code.json', c3Code)

    # c4Code = getc4Code(c3Code, realEstate_code['APT'])
    # IO.writeJSON('c4Code.json', c4Code)

else:
    c1Code = IO.staticLoadJSON('2016-01-25-c1Code.json')
    c2Code = IO.staticLoadJSON('2016-01-25-c2Code.json')
    c3Code = IO.staticLoadJSON('2016-01-25-c3Code.json')
    c4Code = IO.staticLoadJSON('2016-01-28-c4Code.json')

driver = webdriver.PhantomJS(executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')
#c4Code = getc4Code(c3Code[0:1], realEstate_code['APT'], driver)
#IO.writeJSON('c4Code.json', c4Code)
c4List = getc4List(c4Code, realEstate_code['APT'], driver)

#driver = webdriver.PhantomJS(executable_path='C:\\Users\\User\\Downloads\\phantomjs-2.0.0-windows\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe')
#url = 'http://realestate.daum.net/iframe/maemul/DanjiMaemulList.daum?mcateCode=A1A3A4&saleTypeCode=*&tabName=maemullist&fullload=Y&isSection=Y&danjiId=4753'
#driver.get(url)

#c4List = getc4ListParsing(driver.page_source, driver)

if debug == 0:
    for aa in c4Code:
        # print aa['c1Code'], aa['c2Code'],  aa['c3Code'], aa['c4Code'], aa['c1NameKR'], aa['c2NameKR'], aa['c3NameKR'], aa['c4NameKR'], aa['c4TradeCounts'], aa['c4LeaseCounts'], aa['c4RentCounts']
        print aa['c1Code'], aa['c2Code'], aa['c3Code'], aa['c4Code'], aa['c1NameKR'], aa['c2NameKR'], aa['c3NameKR'], aa['c4NameKR']
