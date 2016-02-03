# -*- coding: utf-8 -*-
import bs4
import requests
import IO

class EstateList:
    def __init__(self):
        self.DEBUG = False
        self.c1Code = []
        self.c2Code = []
        self.c3Code = []
        self.c4Code = []
        self.c4List = []
        self.estateCode = 'A01'
        self.RETRIES = 5
        self.TIMEOUT = 5.0

    def set_debug(self, flag):
        self.DEBUG = flag

    def set_estatecode(self, estatecode):
        self.estateCode = estatecode

    def get_c1code(self):
        url = 'http://land.naver.com/'

        nAttempts = 1
        while (nAttempts < self.RETRIES):
            if self.DEBUG:
                print 'DEBUG: get_c1cod: %s requesting...' % (url),

            try:
                r = requests.get(url, timeout=self.TIMEOUT)
            except requests.exceptions.RequestException as e:
                print e
                print 'Retry to connect ... %d/%d' % (nAttempts, self.RETRIES)
                nAttempts += 1
            else:
                self.c1Code = self.get_c1parsing(r.text)
                IO.writeJSON('c1Code.json', self.c1Code)
                print 'Done'
                break

    def set_c1code(self, fname, flag):
        if flag:
            self.c1Code = IO.loadJSON(fname)
        else:
            self.c1Code = IO.staticLoadJSON(fname)

    def set_c2code(self, fname, flag):
        if flag:
            self.c2Code = IO.loadJSON(fname)
        else:
            self.c2Code = IO.staticLoadJSON(fname)

    def set_c3code(self, fname, flag):
        if flag:
            self.c3Code = IO.loadJSON(fname)
        else:
            self.c3Code = IO.staticLoadJSON(fname)

    def set_c4code(self, fname, flag):
        if flag:
            self.c4Code = IO.loadJSON(fname)
        else:
            self.c4Code = IO.staticLoadJSON(fname)

    def get_c1parsing(self, text):
        soup = bs4.BeautifulSoup(text, "html.parser")
        selectbox = soup.find('select', {'class': 'selectbox-source'})
        option_list = selectbox.findAll('option')
        code_list = []
        for option in option_list:
            item = {}
            item['c1Code'] = option['value']
            item['c1CoordX'] = option['xcrdn']
            item['c1CoordY'] = option['ycrdn']
            item['c1NameKR'] = option.text
#            if self.DEBUG:
#                print 'DEBUG: getc1parsing: ', option['value'], option['xcrdn'], option['ycrdn'], option.text
            code_list.append(item)

        return code_list

    def get_c2code(self):
        if not self.c1Code:
            print 'Error: c1Code is empty.'
            return None

        url_list = []
        for code in self.c1Code:
            #http://land.naver.com/article/cityInfo.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=&cortarNo=1100000000
            url1 = 'http://land.naver.com/article/cityInfo.nhn?rletTypeCd='
            url2 = '&tradeTypeCd=&hscpTypeCd=&cortarNo='
            url = url1 + self.estateCode + url2 + code['c1Code']
            url_list.append(url)

        for idx, url in enumerate(url_list):
            #subc2code = []
            nAttempts = 1
            while (nAttempts < self.RETRIES):
                if self.DEBUG:
                    print 'DEBUG: get_c2code: %s requesting...' % (url),

                try:
                    r = requests.get(url, timeout=self.TIMEOUT)
                except requests.exceptions.RequestException as e:
                    print e
                    nAttempts += 1
                    print 'Retry to connect ... %d/%d' % (nAttempts, self.RETRIES)
                else:
                    if self.DEBUG:
                        print 'Done'
                        print 'DEBUB: getc2code: %s/%s (%d/%d) ...' % (self.c1Code[idx]['c1NameKR'], self.c1Code[idx]['c1Code'], (idx+1), len(self.c1Code)),
                        subc2code = self.get_c2parsing(r.text, idx)

                        if self.DEBUG:
                            print 'Done'
                        break

            for sub in subc2code:
                item = {}
                item['c1Code'] = self.c1Code[idx]['c1Code']
                item['c1CoordX'] = self.c1Code[idx]['c1CoordX']
                item['c1CoordY'] = self.c1Code[idx]['c1CoordY']
                item['c1NameKR'] = self.c1Code[idx]['c1NameKR']
                item['c2Code'] = sub['c2Code']
                item['c2NameKR'] = sub['c2NameKR']

                self.c2Code.append(item)

        IO.writeJSON('c2Code.json', self.c2Code)


    def get_c2parsing(self, text, index):
        code_list = []

        if self.c1Code[index]['c1Code'] == '3600000000':
            item = {}
            item['c2Code'] = '3611000000'.encode('utf-8')
            item['c2NameKR'] = self.c1Code[index]['c1NameKR']
            code_list.append(item)

        else:
            soup = bs4.BeautifulSoup(text, "html.parser")
            areaList = soup.find('div', {'class': 'area scroll'}).findAll('li')

            for subcode in areaList:
                temp = str(subcode.find('a')['class']).replace("[", "").replace("]", "").replace("'", "")

                item = {}
                item['c2Code'] = temp.split(':')[-1]
                item['c2NameKR'] = subcode.find('a').text
                code_list.append(item)

        return code_list

    def get_c3code(self):
        if not self.c2Code:
            print 'Error: c2Code is empty.'
            return None

        url_list = []
        for code in self.c2Code:
            #http://land.naver.com/article/divisionInfo.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=&articleOrderCode=&cortarNo=1168000000
            url1 = 'http://land.naver.com/article/divisionInfo.nhn?rletTypeCd='
            url2 = '&tradeTypeCd=&hscpTypeCd=&articleOrderCode=&cortarNo='
            url = url1 + self.estateCode + url2 + code['c2Code']
            url_list.append(url)

        for idx, url in enumerate(url_list):
            nAttempts = 1
            while (nAttempts < self.RETRIES):
                if self.DEBUG:
                    print 'DEBUG: get_c3code: %s requesting...' % (url),

                try:
                    r = requests.get(url, timeout=self.TIMEOUT)
                except requests.exceptions.RequestException as e:
                    print e
                    print 'Retry to connect ... %d/%d' % (nAttempts, self.RETRIES)
                    nAttempts += 1
                else:
                    if self.DEBUG:
                        print 'Done'
                        print 'DEBUB: getc3code: %s/%s (%d/%d) ...' % (self.c2Code[idx]['c2NameKR'], self.c2Code[idx]['c2Code'], (idx+1), len(self.c2Code)),
                        subc3code = self.get_c3parsing(r.text, idx)

                        if self.DEBUG:
                            print 'Done'
                        break

            for sub in subc3code:
                item = {}
                item['c1Code'] = self.c2Code[idx]['c1Code']
                item['c1CoordX'] = self.c2Code[idx]['c1CoordX']
                item['c1CoordY'] = self.c2Code[idx]['c1CoordY']
                item['c1NameKR'] = self.c2Code[idx]['c1NameKR']
                item['c2Code'] = self.c2Code[idx]['c2Code']
                item['c2NameKR'] = self.c2Code[idx]['c2NameKR']
                item['c3Code'] = sub['c3Code']
                item['c3NameKR'] = sub['c3NameKR']
                item['c3TotalCounts'] = sub['c3TotalCounts']

                self.c3Code.append(item)

        IO.writeJSON('c3Code.json', self.c3Code)

    def get_c3parsing(self, text, index):
        code_list = []
        soup = bs4.BeautifulSoup(text, "html.parser")
        areaList = soup.find('div', {'id': 'divisionScrollList'}).findAll('li')

        for subcode in areaList:
            c3info = str(subcode.find('a')['class']).replace("[", "").replace("]", "").replace("'", "")
            count = subcode.find('em').text.replace("(", "").replace(")", "")

            item = {}
            item['c3Code'] = c3info.split(':')[-1]
            item['c3NameKR'] = subcode.find('a').text
            item['c3TotalCounts'] = count

            code_list.append(item)

        return code_list

    def get_c4code(self):
        if not self.c3Code:
            print 'Error: c3Code is empty.'
            return None

        url_list = []
        for code in self.c3Code:
            #http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=&cortarNo=1168010300
            url1 = 'http://land.naver.com/article/articleList.nhn?rletTypeCd='
            url2 = '&tradeTypeCd=&hscpTypeCd=&cortarNo='
            url = url1 + self.estateCode + url2 + code['c3Code']
            url_list.append(url)

        for idx, url in enumerate(url_list):
            nAttempts = 1
            while (nAttempts < self.RETRIES):
                if self.DEBUG:
                    print 'DEBUG: get_c4code: %s requesting...' % (url),

                try:
                    r = requests.get(url, timeout=self.TIMEOUT)
                except requests.exceptions.RequestException as e:
                    print e
                    print 'Retry to connect ... %d/%d' % (nAttempts, self.RETRIES)
                    nAttempts += 1
                else:
                    if self.DEBUG:
                        print 'Done'
                        print 'DEBUB: getc3code: %s/%s (%d/%d) ...' % (self.c3Code[idx]['c3NameKR'], self.c3Code[idx]['c3Code'], (idx+1), len(self.c3Code)),
                        subc4code = self.get_c4parsing(r.text, idx)

                        if self.DEBUG:
                            print 'Done'
                        break

            for sub in subc4code:
                item = {}
                item['c1Code'] = self.c3Code[idx]['c1Code']
                item['c1CoordX'] = self.c3Code[idx]['c1CoordX']
                item['c1CoordY'] = self.c3Code[idx]['c1CoordY']
                item['c1NameKR'] = self.c3Code[idx]['c1NameKR']
                item['c2Code'] = self.c3Code[idx]['c2Code']
                item['c2NameKR'] = self.c3Code[idx]['c2NameKR']
                item['c3Code'] = self.c3Code[idx]['c3Code']
                item['c3NameKR'] = self.c3Code[idx]['c3NameKR']
                item['c3TotalCounts'] = self.c3Code[idx]['c3TotalCounts']
                item['c4Code'] = sub['c4Code']
                item['c4NameKR'] = sub['c4NameKR']
                item['c4CoordMapX'] = sub['c4CoordMapX']
                item['c4CoordMapY'] = sub['c4CoordMapY']
                item['c4TradeCounts'] = sub['c4TradeCounts']
                item['c4LeaseCounts'] = sub['c4LeaseCounts']
                item['c4RentCounts'] = sub['c4RentCounts']

                self.c4Code.append(item)

        IO.writeJSON('c4Code.json', self.c4Code)

    def get_c4parsing(self, text, index):
        code_list = []
        soup = bs4.BeautifulSoup(text, "html.parser")
        areaList = soup.find('div', {'class': 'housing_inner'}).findAll('li')

        for sub in areaList:
            item = {}
            tmp = sub.find('a')
            count = sub.find('em').text.replace("(", "").replace(")", "").split('/')

            item['c4Code'] = tmp['hscp_no']
            item['c4NameKR'] = tmp.text
            item['c4CoordMapX'] = tmp['mapx']
            item['c4CoordMapY'] = tmp['mapy']
            item['c4TradeCounts'] = count[0]
            item['c4LeaseCounts'] = count[1]
            item['c4RentCounts'] = count[2][:-1]
            item['c4TotalSalesCounts'] = int(count[0]) + int(count[1]) + int(count[2][:-1])

            code_list.append(item)

        return code_list

    def get_c4List(self):
        if not self.c4Code:
            print 'Error: c4Code is empty.'
            return None

        url_list = []
        index_list = []
        specificIdx = 8
        for idx, code in enumerate(self.c4Code[specificIdx:(specificIdx+1)]):
        #for idx, code in enumerate(self.c4Code[0:1]):
            #http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=&rletNo=103385&hscpTypeCd=&page=1
            nTotalSales = int(code['c4TradeCounts']) + int(code['c4LeaseCounts']) + int(code['c4RentCounts'])
            if nTotalSales:
                index_list.append(idx + specificIdx)
                url1 = 'http://land.naver.com/article/articleList.nhn?rletTypeCd='
                url2 = '&tradeTypeCd=&hscpTypeCd=&rletNo='

                url = url1 + self.estateCode + url2 + code['c4Code']
                url_list.append(url)

        for idx, url in enumerate(url_list):
            nAttempts = 1
            index = index_list[idx]
            while (nAttempts < self.RETRIES):
                if self.DEBUG:
                    print 'DEBUG: get_c4list: %s requesting...' % (url),

                try:
                    r = requests.get(url, timeout=self.TIMEOUT)
                except requests.exceptions.RequestException as e:
                    print e
                    print 'Retry to connect ... %d/%d' % (nAttempts, self.RETRIES)
                    nAttempts += 1
                else:
                    if self.DEBUG:
                        print 'Done'
                        print 'DEBUB: getc4list: %s/%s (%d/%d) ...' % (self.c4Code[index]['c3NameKR'], self.c4Code[index]['c3Code'], (idx+1), len(self.c4Code))
                        subc4code = self.get_c4listparsing(r.text, index, url)

                        if self.DEBUG:
                            print 'Done'
                        break

            for sub in subc4code:
                item = {}
                item['c1Code'] = self.c4Code[idx]['c1Code']
                item['c1CoordX'] = self.c4Code[idx]['c1CoordX']
                item['c1CoordY'] = self.c4Code[idx]['c1CoordY']
                item['c1NameKR'] = self.c4Code[idx]['c1NameKR']
                item['c2Code'] = self.c4Code[idx]['c2Code']
                item['c2NameKR'] = self.c4Code[idx]['c2NameKR']
                item['c3Code'] = self.c4Code[idx]['c3Code']
                item['c3NameKR'] = self.c4Code[idx]['c3NameKR']
                item['c3TotalCounts'] = self.c4Code[idx]['c3TotalCounts']
                item['c4Code'] = self.c4Code[idx]['c4Code']
                item['c4NameKR'] = self.c4Code[idx]['c4NameKR']
                item['c4CoordMapX'] = self.c4Code[idx]['c4CoordMapX']
                item['c4CoordMapY'] = self.c4Code[idx]['c4CoordMapY']
                item['c4TradeCounts'] = self.c4Code[idx]['c4TradeCounts']
                item['c4LeaseCounts'] = self.c4Code[idx]['c4LeaseCounts']
                item['c4RentCounts'] = self.c4Code[idx]['c4RentCounts']

                print sub['c4MaemulType'], sub['c4SellingType'], item['c4NameKR'], sub['c4SellingPrice']

                self.c4Code.append(item)

        IO.writeJSON('c4List.json', self.c4Code)

    def get_c4listparsing(self, text, index, url):
        soup = bs4.BeautifulSoup(text, "html.parser")
        maemulName = soup.findAll('caption', {'class': 'blind_caption'})

        checkMaemul = soup.find('table', {'class': 'sale_list _tb_site_img NE=a:cpm'})
        agentMaemul = soup.find('table', {'class': 'sale_list NE=a:prm'})

        nTotalSales = int(self.c4Code[index]['c4TradeCounts']) + int(self.c4Code[index]['c4LeaseCounts']) + int(self.c4Code[index]['c4RentCounts'])
        nPage = nTotalSales / 30 + 1

        subList = []
        self.get_c4listparsing_core(checkMaemul, subList, '확인 매물'.decode('utf-8'))
        self.get_c4listparsing_core(agentMaemul, subList, '공인중개사협회매물'.decode('utf-8'))

        for i in xrange(2, nPage+1):
            nAttempts = 1
            pageUrl = url + '&page=' + str(i)
            while (nAttempts < self.RETRIES):
                if self.DEBUG:
                    print 'DEBUG: get_c4list: %s requesting...' % (pageUrl),

                try:
                    r_sub = requests.get(pageUrl, timeout=self.TIMEOUT)
                except requests.exceptions.RequestException as e:
                    print e
                    print 'Retry to connect ... %d/%d' % (nAttempts, self.RETRIES)
                    nAttempts += 1
                else:
                    if self.DEBUG:
                        print 'Done'
                        print 'DEBUB: getc3code: %s (%d/%d) ...' % (self.c4Code[index]['c4NameKR'], i, nPage),
                        soup_sub = bs4.BeautifulSoup(r_sub.text, "html.parser")

                        checkMaemul_sub = soup_sub.find('table', {'class': 'sale_list _tb_site_img NE=a:cpm'})
                        agentMaemul_sub = soup_sub.find('table', {'class': 'sale_list NE=a:prm'})
                        self.get_c4listparsing_core(checkMaemul_sub, subList, '확인 매물'.decode('utf-8'))
                        self.get_c4listparsing_core(agentMaemul_sub, subList, '공인중개사협회매물'.decode('utf-8'))

                        if self.DEBUG:
                            print 'Done'
                        break


        return subList

    def get_c4listparsing_core(self, text, list, maemulName):
        try:
            item_list = text.find('tbody').findAll('tr')
        except AttributeError:
            return None
        else:
            nSubItems = len(item_list) / 2
            for i in xrange(nSubItems):
                item = {}

                item['c4MaemulType'] = maemulName
                subItems = item_list[i*2 + 0].findAll('td')
                #td 1
                sellingType = subItems[0].find('div', {'class': 'inner'}).text

                #td 7
                try:
                    sellingPrice = subItems[6].find('strong')['title']
                except KeyError:
                    sellingPrice = subItems[6].find('strong').text.strip()
                item['c4SellingType'] = sellingType
                item['c4SellingPrice'] = sellingPrice

                list.append(item)


aptList = EstateList()
aptList.set_debug(True)
aptList.set_c1code('c1Code.json', True)
aptList.set_c2code('c2Code.json', True)
aptList.set_c3code('c3Code.json', True)
aptList.set_c4code('c4Code.json', True)
aptList.get_c4List()
#aptList.get_c1code()
#aptList.get_c2code()
#aptList.get_c3code()
#aptList.get_c4code()
#c4code = IO.loadJSON('c4Code.json')
#print len(c4code)

#for ii in c4code:
#    print ii['c1NameKR'], ii['c2NameKR'], ii['c3NameKR'], ii['c4NameKR'], ii['c1Code'], ii['c2Code'], ii['c3Code'], ii['c4Code'], ii['c4TradeCounts'], ii['c4LeaseCounts'], ii['c4RentCounts']
