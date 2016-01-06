import bs4
import requests
from selenium import webdriver
import IO
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
        r = requests.get(url)
        subc2List = getc2Parsing(r.text)
        if c1List[idx]['c1Code'] == '1320000':
            subItem = {}
            subItem['c1Code'] = c1List[idx]['c1Code']
            subItem['c1NameKR'] = c1List[idx]['c1NameKR']
            subItem['c1Coords'] = c1List[idx]['c1Coords']
            subItem['c2Code'] = c1List[idx]['c1Code']
            subItem['c2NameKR'] = c1List[idx]['c1NameKR']
            c2List.append(subItem)
            '''
            for item in subc2List:
                subItem = {}
                subItem['c1Code'] = c1List[idx]['c1Code']
                subItem['c1NameKR'] = c1List[idx]['c1NameKR']
                subItem['c1Coords'] = c1List[idx]['c1Coords']
                subItem['c2Code'] =
                #subItem['c2Code'] = item['c2Code']
                subItem['c2NameKR'] = item['c2NameKR'].split()[0]
                c2List.append(subItem)
            '''

        else:
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
    list_estateinfo = soup.find('ul', {"class": "list_estateinfo"})
    c2Items = list_estateinfo.findAll('li')
    for item in c2Items:
        items = {}
        items['c2Code'] = item.find('a')['href'].split('/')[3].encode('ascii','ignore')
        items['c2NameKR'] = item.split()[0]

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
        r = requests.get(url)

        subc3List = getc3Parsing(r.text)
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

def getc4Code(c3List, realEstateCode):
    headers = {"Host": "realestate.daum.net",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
               "Accept-Encoding": "gzip, deflate"}
    url_list = []
    for subItem in c3List:
        url1 = 'http://realestate.daum.net/maemul/area/'
        c1code = subItem['c3Code']
        estatecode = realEstateCode
        url2 = '*/summary'
        url = url1 + c1code + '/' + estatecode + '/' + url2
        url_list.append(url)

    c4List = []
    for idx, url in enumerate(url_list[0:1]):
        print url
        r = requests.get(url)
        driver = webdriver.Firefox()
        driver.get(url)


        subc4List = getc4Parsing(driver.page_source)
        '''
        for item in subc4List:
            subItem = {}
            subItem['c1Code'] = c3List[idx]['c1Code']
            subItem['c1NameKR'] = c3List[idx]['c1NameKR']
            subItem['c2Code'] = c3List[idx]['c2Code']
            subItem['c2NameKR'] = c3List[idx]['c2NameKR']
            subItem['c3Code'] = item['code']
            subItem['c3NameKR'] = item['nameKR']
            subItem['c3Counts'] = item['counts']

            c4List.append(subItem)
        '''

    return c4List

def getc4Parsing(text):
    item_list = []
    soup = bs4.BeautifulSoup(text, "html.parser")
    list_estateinfo = soup.find('div', {"class": "detale_sort detail_on"})
    #c4Items = list_estateinfo.findAll('li')
    print list_estateinfo
    '''
    for item in c3Items:
        items = {}
        items['code'] = item.find('a')['href'].split('/')[3].encode('ascii','ignore')
        tmpStr = item.text
        tmpStrList = tmpStr.split()
        items['nameKR'] = tmpStrList[0]
        items['counts'] = tmpStrList[1].split()[-1].replace("(","").replace(")","").encode('ascii','ignore')

        item_list.append(items)
    '''

    return item_list



flag = 0
debug = 0

if flag == 1:
    c1List = getc1Code(realEstate_code['APT'])
    IO.writeJSON('c1List.json', c1List)

    c2List = getc2Code(c1List, realEstate_code['APT'])
    IO.writeJSON('c2List.json', c2List)

    c3List = getc3Code(c2List, realEstate_code['APT'])
    IO.writeJSON('c3List.json', c3List)

else:
    c1List = IO.staticLoadJSON('2016-01-06-c1List.json')
    c2List = IO.staticLoadJSON('2016-01-06-c2List.json')
    c3List = IO.staticLoadJSON('2016-01-06-c3List.json')

c4List = getc4Code(c3List, realEstate_code['APT'])

if debug == 1:
    for aa in c3List:
        print aa['c1Code'], aa['c2Code'],  aa['c3Code'], aa['c1NameKR'], aa['c2NameKR'], aa['c3NameKR']
