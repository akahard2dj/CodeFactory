import bs4
import requests
import json

kuName = ['kangnam', 'kangdong', 'kangbuk', 'kangseo','kwanak','kwangjin','kuro','kuemchoen','noone','dobong',
            'dongdaemun','dongjak','mapo','seodaemun','seocho','seongdong','seongbuk','songpa','yangcheon',
            'youngdeungpo','yongsan','eunpyong','jongro','jung','jungrang']

dongName = []
dongName.append( ['kaepo','nonhyun','daechi','dogok','samsung','saegok','suseo','shinsa','apgujeong','yeoksam','yulhyun','ilwon','jagok','cheongdam'])
dongName.append( ['kangil','kodeok','gil','dunchon','myungil','sangil','seongnae','amsa','cheonho'])
dongName.append( ['miah','beon','suyou','ui'])
dongName.append( ['kayang','kaehwa','gonghang','gwhahae','naebalsan','deungchon','magok','banghwa','yeomchang','ogok','osoe','oebalsan','hwagok'])
dongName.append( ['namhyun','bongchoen','shinlim'])
dongName.append( ['gwhangjang','kuui','kunja','nueong','jayang','junggok','hwayang'])
dongName.append( ['garibong','gaebong','gocheok','kuro','gung','shindorim','oryu','onsu','choenwang','hang'])
dongName.append( ['gasan','doksan','shiheung'])
dongName.append( ['gongreung','sanggae','wolgae','junggae','hagae'])
dongName.append( ['dobong','banghak','ssangmun','chang'])
dongName.append( ['dapshipri','shinseol','youngdu','yimun','jangan','jeonnong','jaeki','cheonryangri','hoeki','huikyung'])
dongName.append( ['noryangjin','daebang','dongjak','bon','sadang','sangdo1','snagdo','shindaebang','hukseok'])
dongName.append( ['gongdeok','kusu','nogosan','dangin','daeheung','dohwa','dongkyo','mapo','mangwon','sangsu','sangam','seokyo','seongsan','shingongdeok','shinsu','shinjeong','ahyun','yeonnam','yeomri','yongkang','jung','changcheon','tojeong','hajung','hapjeong','hyunseok'])
dongName.append( ['namgajwha','naengcheon','daeshin','daehyun','mikeun','bongwon','bukkwaja','bukahyun','shinchon','yeonhui','youngcheon','okcheon','changcheon','cheonyoun','chungjeongro2ga','chungjeongro3ga','hap','hyunjeo','honguen','hongjae'])
dongName.append( ['naegok','banpo','bangbae','seocho','shinwon','yangjae','yeomgok','umyeon','wonji','jamwon'])
dongName.append( ['keumho1ga','keumho2ga','keumho3ga','keumho4ga','doseon','majang','sakuen','sangwangshipri','seongsu1ga','seongsu2ga','songjeong','oksoo','youngdap','eungbon','hawangshipri','haengdand','hongik'])
dongName.append( ['kileum','donam','dongseon1ga','dongseon2ga','dongseon3ga','dongseon4ga','dongseon5ga','dongsomun1ga','dongsomun2ga','dongsomun3ga','dongsomun4ga','dongsomun5ga','dongsomun6ga','dongsomun7ga','bomun1ga','bomun2ga','bomun3ga','bomun4ga','bomun5ga','bomun6ga','bomun7ga','samseon1ga','samseon2ga','samseon3ga','samseon4ga','samseon5ga','sangwolgok','seokkwan','seongbuk','seongbuk1ga','anam1ga','anam2ga','anam3ga','anam4ga','anam5ga','jangui','jeongreung','jongam','hawolgok'])
dongName.append( ['garak','geoyoe','macheon','munjeong','bangyi','samjeon','seokchon','songpa','shincheon','okeum','jamshil','jangji','pungnap'])
dongName.append( ['mok','shinwol','shinjeong'])
dongName.append( ['dangsan','dangsan1ga','dangsan2ga','dangsan3ga','dangsan4ga','dangsan5ga','dangsan6ga','daerim','dorim','munrae1ga','munrae2ga','munrae3ga','munrae4ga','munrae5ga','munrae6ga','shingil','yangpyoeng','yangpyoeng1ga','yangpyoeng2ga','yangpyoeng3ga','yangpyoeng4ga','yangpyoeng5ga','yangpyoeng6ga','yanghwa','yeouido','youngdeungpo','youngdeungpo1ga','youngdeungpo2ga','youngdeungpo3ga','youngdeungpo4ga','youngdeungpo5ga','youngdeungpo6ga','youngdeungpo7ga','youngdeungpo8ga'])
dongName.append( ['kalwol','namyoung','dowon','dongbinggo','dongja','munbae','bokwhang','sancheon','seoke','seobinggo','shinke','shinchang','yongmun','yongsan1ga','yongsan2ga','yongsan3ga','yongsan4ga','yongsan5ga','yongsan6ga','wonhyoro1ga','wonhyoro2ga','wonhyoro3ga','wonhyoro4ga','yichon','yitaewon','juseong','cheongam','cheongpa1ga','cheongpa2ga','cheongpa3ga','hangangro1ga','hangangro2ga','hangangro3ga','hannam','hyochang','huam'])
dongName.append( ['kalhyun','kusan','nokbeon','daejo','bulkwang','susaek','shinsa','yeokchon','ungam','jungsan','jinkwan'])
dongName.append( ['kahui','kyunji','kyungun','ke','gongpyoeng','kwansu','kwancheol','kwanhun','kyonam','kyobuk','kuki','kungjeong','kwonnong','nakwon','naesoo','naeja','nusang','nuha','dangju','doryum','donui','dongsung','myungrun1ga','myungrun2ga','myungrun3ga','myungrun4ga','myo','muak','bongik','buam','sagan','sajik','samchoeng','seorin','saejong','sokyuk','songwol','songhyun','susong','sungin','shinkyo','shinmuro1ga','shinmuro2ga','shinyoung','ankuk','yeonkeon','yeonji','yeji','okin','waryong','unni','wonnam','wonseo','yihwa','ikseon','insa','inui','jangsa','jae','jeokseon','jongro1ga','jongro2ga','jongro3ga','jongro4ga','jongro5ga','jongro6ga','junghak','changseong','changshin','cheongun','cheongjin','chaebu','chungshin','tongui','tongin','palpan','pyeong','pyeongchang','pilun','haengchon','hyehwa','hongji','hongpa','hwa','hyoja','hyojae','hunjeong'])
dongName.append( ['kwanghui1ga','kwanghui2ga','namdaemunro1ga','namdaemunro2ga','namdaemunro3ga','namdaemunro4ga','namdaemunro5ga','namsan1ga','namsan2ga','namsan3ga','namchang','namhak','da','manri1ga','manri2ga','myung1ga','myung2ga','mukyo','muhak','mukjeong','bangsan','bongrae1ga','bongrae2ga','bukchang','sanrim','samkak','seosomun','sokong','supyo','suha','sunhwa','shindang','ssangrim','yekwan','yejang','ojang','eulji1ga','eulji2ga','eulji3ga','eulji4ga','eulji5ga','eulji6ga','eulji7ga','uiju1ga','uiju2ga','inhyung1ga','inhyung2ga','yipjeong','jangkyo','jangchung1ga','jangchung2ga','jeo1ga','jeo2ga','jeong','jukyo','juja','jungrim','cho','chungmuro1ga','chungmuro2ga','chungmuro3ga','chungmuro4ga','chungmuro5ga','chungjeongro1ga','taepyungro1ga','taepyungro2ga','pil1ga','pil2ga','pil3ga','hwanghak','hoehyun1ga','hoehyun2ga','hoehyun3ga','huengin'])
dongName.append( ['mangu','myeonmok','muk','sangbong','shinnae','junghwa'])

def writeJSON(fname, list):
    j = json.dumps(list)
    with open(fname,'w') as f:
        f.write(j)
    f.close()

def loadJSON(fname):
    with open(fname, 'r') as f:
        list = json.load(f)

    return list

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
    #print areaScroll
    list = areaScroll.findAll('li')

    for i in range(len(list)):
        cortarNo = {}
        tmp = list[i].find('a')["onclick"]
        code = tmp.split('{',1)[1].split('}')[0].split(":")[1]

        cortarNo["nameKR"] = list[i].text.split("(")[0]
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
        ### Check!!!
        aptName = {}
        tmp = list[i].text.split()[-1].replace("(","").replace(")","")
        strLen = len(tmp)
        sale = tmp[0:strLen-1].split('/')

        aptName['name'] = list[i].text.split()[0]
        aptName['code'] = list[i].find('a')['hscp_no']
        aptName['mapx'] = list[i].find('a')['mapx']
        aptName['mapy'] = list[i].find('a')['mapy']
        aptName['sale_trade'] = int(sale[0])
        aptName['sale_lease'] = int(sale[1])
        aptName['sale_rent'] = int(sale[2])
        ### Check!!!
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


# city(Seoul) parsing --> Ku list
'''
url = 'http://land.naver.com/article/cityInfo.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1100000000'
r = requests.get(url)
cortarNoKu_list = get_cortarNoKu(r.text)
'''

# Ku List json file generation.
'''
kuList = []
for i in range(len(kuName)):
    kuListElements = {}
    kuListElements['nameKR'] = cortarNoKu_list[i]['name']
    kuListElements['nameEN'] = kuName[i]
    kuListElements['index'] = i
    kuListElements['fname'] = kuName[i] + '.json'
    kuListElements['code'] = cortarNoKu_list[i]['code']

    kuList.append(kuListElements)

#for aa in kuList:
#    print aa['nameKR'],aa['nameEN'], aa['code'], aa['index'], aa['fname']

writeJSON('seoul_ku_list.json', kuList)
'''

# kuList --> Dong List
'''
kuList = loadJSON('seoul_ku_list.json')

idx = 0
for kuElements in kuList:
    url1 = 'http://land.naver.com/article/divisionInfo.nhn?cortarNo='
    url2 = '&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    kuCode = kuElements['code']
    url = url1 + kuCode + url2
    print url
    r = requests.get(url)
    dongList = get_cortarNoDong(r.text)

    newDongList = []
    for i in range(len(dongList)):
        newDong = {}
        newDong['nameKR'] = dongList[i]['nameKR']
        newDong['nameEN'] = dongName[idx][i]
        newDong['code'] = dongList[i]['code']
        newDong['count'] = dongList[i]['count']
        newDongList.append(newDong)

        print kuElements['nameKR'], newDong['nameKR'], newDong['nameEN'], newDong['code'], newDong["count"]

    fout = kuElements['fname']
    writeJSON(fout, newDongList)
    idx = idx + 1
'''


# dong list -> apt list
kuList = loadJSON('seoul_ku_list.json')
dongList = loadJSON(kuList[0]['fname'])

#print dongList[0]['code']
#url = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cortarNo=' + code
#print url
#r = requests.get(url)
#aptList = getcortarNoApt(r.text)

for kuSub in kuList:
    dongList = loadJSON(kuSub['fname'])
    for dongSub in dongList:
        url1 = 'http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cortarNo='
        code = dongSub['code']
        url = url1 + code
        print url
        r = requests.get(url)
        aptList = getcortarNoApt(r.text)
        print kuSub['nameKR'], dongSub['nameKR'],len(aptList)




'''
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
        url = url1 + list[0]['code'] + url2 + listDong[1]['code'] + url3 + unicode(i+1) + url4
        r = requests.get(url)
        getAptList(r.text, aList)

for aa in aList:
    print aa['price'], aa['class'], aa['date'], aa['complex'], aa['area_display'], aa['store'], aa['store_tel'], aa['store_code']
'''