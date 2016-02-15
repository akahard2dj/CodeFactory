import bs4
import requests
import requests.exceptions
import time
import IO


class EstateList:

    def __init__(self):
        self.__c1Code = list()
        self.__c2Code = list()
        self.__c3Code = list()
        self.__c4Code = list()
        self.__c4List = list()
        self.__estateCode = 'A01'
        self.__RETRIES = 10
        self.__TIMEOUT = 1.0
        self.__DEBUG = True
        self.__elapsedtime_c1 = 0.0
        self.__elapsedtime_c2 = 0.0
        self.__elapsedtime_c3 = 0.0
        self.__elapsedtime_c4 = 0.0
        self.__elapsedtime_c4list = 0.0

    def set_debug(self, flag):
        self.__DEBUG = flag

    def set_estatecode(self, estatecode):
        self.__estateCode = estatecode

    @property
    def c1code(self):
        return self.__c1Code

    @c1code.setter
    def c1code(self, fname):
        self.__c1Code = IO.staticLoadJSON(fname)

    def parsing_c1code(self):
        start_time = time.clock()
        url = 'http://land.naver.com'

        num_attempts = 1
        while num_attempts < self.__RETRIES:
            if self.__DEBUG:
                print("DEBUG: get_c1code: %s requesting..." % url, end=" ")

            try:
                r = requests.get(url, timeout=self.__TIMEOUT)
            except requests.exceptions.RequestException as e:
                print("Requests Error Msg: %s" % e)
                print("Retrying to connect ... %d/%d" % (num_attempts+1, self.__RETRIES))
                num_attempts += 1
            else:
                self.__c1Code = self.__get_c1parsing(r.text)
                if self.__DEBUG:
                    print("Done")
                break

        end_time = time.clock()
        self.__elapsedtime_c1 = end_time - start_time

        if num_attempts == 5:
            print("Error: There is no parsed data.")
            return 0

        else:
            IO.writeJSON("c1Code.json", self.__c1Code)

            if self.__DEBUG:
                print("DEBUG: Elapsed time for c1 parsing : %f sec." % self.__elapsedtime_c1)

            return 1

    @staticmethod
    def __get_c1parsing(text):
        soup = bs4.BeautifulSoup(text, "html.parser")
        selectbox = soup.find("select", {"class": "selectbox-source"})
        option_lists = selectbox.findAll("option")
        code_list = []
        for option in option_lists:
            item = dict()
            item['c1Code'] = option['value']
            item['c1CoordX'] = option['xcrdn']
            item['c1CoordY'] = option['ycrdn']
            item['c1NameKR'] = option.text

            code_list.append(item)

        return code_list

    @property
    def c2code(self):
        return self.__c2Code

    @c2code.setter
    def c2code(self, fname):
        self.__c2Code = IO.staticLoadJSON(fname)

    def parsing_c2code(self):
        if not self.__c1Code:
            print('Error: c1code is empty')
            return None

        start_time = time.clock()
        url_list = []
        for code in self.__c1Code:
            url1 = "http://land.naver.com/article/cityInfo.nhn?rletTypeCd="
            url2 = "&tradeTypeCd=&hscpTypeCd=&cortarNo="
            url = url1 + self.__estateCode + url2 + code['c1Code']
            url_list.append(url)

        for idx, url in enumerate(url_list):
            num_attempts = 1
            subc2code = list()

            while num_attempts < self.__RETRIES:
                if self.__DEBUG:
                    print("DEBUG: get_c2code: %s requesting (%d/%d) ..." % (url, idx+1, len(self.__c1Code)), end=" ")

                try:
                    r = requests.get(url, timeout=self.__TIMEOUT)
                except requests.exceptions.RequestException as e:
                    print("Requests Error Msg: %s" % e)
                    print("Retrying to connect ... %d/%d" % (num_attempts+1, self.__RETRIES))
                    num_attempts += 1
                else:
                    subc2code = self.__get_c2parsing(r.text, idx)

                    if self.__DEBUG:
                        print("Done")
                    break

            for sub in subc2code:
                item = dict()
                item['c1Code'] = self.__c1Code[idx]['c1Code']
                item['c1CoordX'] = self.__c1Code[idx]['c1CoordX']
                item['c1CoordY'] = self.__c1Code[idx]['c1CoordY']
                item['c1NameKR'] = self.__c1Code[idx]['c1NameKR']
                item['c2Code'] = sub['c2Code']
                item['c2NameKR'] = sub['c2NameKR']

                self.__c2Code.append(item)

        end_time = time.clock()
        self.__elapsedtime_c2 = end_time - start_time
        if self.__DEBUG:
            print("DEBUG: Elapsed time for c2 parsing : %f sec." % self.__elapsedtime_c2)
        IO.writeJSON('c2Code.json', self.__c2Code)

    def __get_c2parsing(self, text, index):
        code_list = []

        if self.__c1Code[index]['c1Code'] == "3600000000":
            item = dict()
            item['c2Code'] = u"3611000000"
            item['c2NameKR'] = self.__c1Code[index]['c1NameKR']
            code_list.append(item)

        else:
            soup = bs4.BeautifulSoup(text, "html.parser")
            arealist = soup.find('div', {'class': 'area scroll'}).findAll('li')

            for subcode in arealist:
                temp = str(subcode.find('a')['class']).replace("[", "").replace("]", "").replace("'", "")

                item = dict()
                item['c2Code'] = temp.split(':')[-1]
                item['c2NameKR'] = subcode.find('a').text
                code_list.append(item)

        return code_list

    @property
    def c3code(self):
        return self.__c3Code

    @c3code.setter
    def c3code(self, fname):
        self.__c3Code = IO.staticLoadJSON(fname)

    def parsing_c3code(self):
        if not self.__c2Code:
            print("Error: c2code is empty.")
            return None

        start_time = time.clock()
        url_list = list()
        for code in self.__c2Code:
            url1 = 'http://land.naver.com/article/divisionInfo.nhn?rletTypeCd='
            url2 = '&tradeTypeCd=&hscpTypeCd=&articleOrderCode=&cortarNo='
            url = url1 + self.__estateCode + url2 + code['c2Code']
            url_list.append(url)

        for idx, url in enumerate(url_list):
            num_attempts = 1
            subc3code = list()

            while num_attempts < self.__RETRIES:
                if self.__DEBUG:
                    print("DEBUG: get_c3code: %s requesting (%d/%d) ..." % (url, idx+1, len(self.__c2Code)), end=" ")

                try:
                    r = requests.get(url, timeout=self.__TIMEOUT)
                except requests.exceptions.RequestException as e:
                    print("Failed")
                    print("Requests Error Msg: %s" % e)
                    print("Retrying to connect ... %d/%d" % (num_attempts+1, self.__RETRIES))
                    num_attempts += 1
                else:
                    subc3code = self.__get_c3parsing(r.text)

                    if self.__DEBUG:
                        print("Done")
                    break

            for sub in subc3code:
                item = dict()
                item['c1Code'] = self.__c2Code[idx]['c1Code']
                item['c1CoordX'] = self.__c2Code[idx]['c1CoordX']
                item['c1CoordY'] = self.__c2Code[idx]['c1CoordY']
                item['c1NameKR'] = self.__c2Code[idx]['c1NameKR']
                item['c2Code'] = self.__c2Code[idx]['c2Code']
                item['c2NameKR'] = self.__c2Code[idx]['c2NameKR']
                item['c3Code'] = sub['c3Code']
                item['c3NameKR'] = sub['c3NameKR']
                item['c3TotalCounts'] = sub['c3TotalCounts']

                self.__c3Code.append(item)

        end_time = time.clock()
        self.__elapsedtime_c3 = end_time - start_time
        if self.__DEBUG:
            print("DEBUG: Elapsed time for c3 parsing : %f sec." % self.__elapsedtime_c3)
        IO.writeJSON('c3Code.json', self.__c3Code)

    @staticmethod
    def __get_c3parsing(text):
        code_list = list()
        soup = bs4.BeautifulSoup(text, "html.parser")
        arealist = soup.find('div', {'id': 'divisionScrollList'}).findAll('li')

        for subcode in arealist:
            c3info = str(subcode.find('a')['class']).replace("[", "").replace("]", "").replace("'", "")
            count = subcode.find('em').text.replace("(", "").replace(")", "")

            item = dict()
            item['c3Code'] = c3info.split(':')[-1]
            item['c3NameKR'] = subcode.find('a').text
            item['c3TotalCounts'] = count

            code_list.append(item)

        return code_list

    @property
    def c4code(self):
        return self.__c4Code

    @c4code.setter
    def c4code(self, fname):
        self.__c4Code = IO.staticLoadJSON(fname)

    def parsing_c4code(self):
        if not self.__c3Code:
            print("Error: c3Code is empty.")
            return None

        start_time = time.clock()
        url_list = list()
        for code in self.__c3Code:
            url1 = 'http://land.naver.com/article/articleList.nhn?rletTypeCd='
            url2 = '&tradeTypeCd=&hscpTypeCd=&cortarNo='
            url = url1 + self.__estateCode + url2 + code['c3Code']
            url_list.append(url)

        for idx, url in enumerate(url_list):
            num_attempts = 1
            subc4code = list()

            while num_attempts < self.__RETRIES:
                if self.__DEBUG:
                    print("DEBUG: get_c4code: %s requesting (%d/%d) ..." % (url, idx+1, len(self.__c3Code)), end=" ")

                try:
                    r = requests.get(url, timeout=self.__TIMEOUT)
                except requests.exceptions.RequestException as e:
                    print("Failed")
                    print("Requests Error Msg: %s" % e)
                    print("Retrying to connect ... %d/%d" % (num_attempts+1, self.__RETRIES))
                    num_attempts += 1
                else:
                    subc4code = self.__get_c4parsing(r.text)

                    if self.__DEBUG:
                        print("Done")
                    break

            for sub in subc4code:
                item = dict()
                item['c1Code'] = self.__c3Code[idx]['c1Code']
                item['c1CoordX'] = self.__c3Code[idx]['c1CoordX']
                item['c1CoordY'] = self.__c3Code[idx]['c1CoordY']
                item['c1NameKR'] = self.__c3Code[idx]['c1NameKR']
                item['c2Code'] = self.__c3Code[idx]['c2Code']
                item['c2NameKR'] = self.__c3Code[idx]['c2NameKR']
                item['c3Code'] = self.__c3Code[idx]['c3Code']
                item['c3NameKR'] = self.__c3Code[idx]['c3NameKR']
                item['c3TotalCounts'] = self.__c3Code[idx]['c3TotalCounts']
                item['c4Code'] = sub['c4Code']
                item['c4NameKR'] = sub['c4NameKR']
                item['c4CoordMapX'] = sub['c4CoordMapX']
                item['c4CoordMapY'] = sub['c4CoordMapY']
                item['c4TradeCounts'] = sub['c4TradeCounts']
                item['c4LeaseCounts'] = sub['c4LeaseCounts']
                item['c4RentCounts'] = sub['c4RentCounts']

                self.__c4Code.append(item)

        end_time = time.clock()
        self.__elapsedtime_c4 = end_time - start_time
        if self.__DEBUG:
            print("DEBUG: Elapsed time for c4 parsing : %f sec." % self.__elapsedtime_c4)
        IO.writeJSON('c4Code.json', self.__c4Code)

    @staticmethod
    def __get_c4parsing(text):
        code_list = []
        soup = bs4.BeautifulSoup(text, "html.parser")
        arealist = soup.find('div', {'class': 'housing_inner'}).findAll('li')

        for sub in arealist:
            item = dict()
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

    @property
    def c4list(self):
        return self.__c4List

    @c4list.setter
    def c4list(self, fname):
        self.__c4List = IO.staticLoadJSON(fname)

    def parsing_c4list(self):
        if not self.__c4Code:
            print("Error: c4code is empty.")
            return None

        start_time = time.clock()
        url_list = list()
        index_list = list()
        specific_idx = 0
        #for idx, code in enumerate(self.__c4Code[specific_idx:(specific_idx+1)]):
        for idx, code in enumerate(self.__c4Code):
            num_totalsales = int(code['c4TradeCounts']) + int(code['c4LeaseCounts']) + int(code['c4RentCounts'])
            if num_totalsales:
                index_list.append(idx + specific_idx)
                url1 = 'http://land.naver.com/article/articleList.nhn?rletTypeCd='
                url2 = '&tradeTypeCd=&hscpTypeCd=&rletNo='

                url = url1 + self.__estateCode + url2 + code['c4Code']
                url_list.append(url)

        for idx, url in enumerate(url_list):
            num_attempts = 1
            index = index_list[idx]
            subc4list = list()

            while num_attempts < self.__RETRIES:
                if self.__DEBUG:
                    print("DEBUG: get_c4list: %s requesting (%d/%d) ..." % (url, idx+1, len(self.__c4Code)), end=" ")

                try:
                    r = requests.get(url, timeout=self.__TIMEOUT)
                except requests.exceptions.RequestException as e:
                    if self.__DEBUG:
                        print("Failed")
                        print("Requests Error Msg: %s" % e)
                        print("Retrying to connect ... %d/%d" % (num_attempts+1, self.__RETRIES))
                    num_attempts += 1
                else:
                    if self.__DEBUG:
                        print("Done")

                    subc4list = self.__get_c4listparsing(r.text, index, url)
                    for sub in subc4list:
                        #index = index_list[idx]
                        item = dict()
                        item['c1Code'] = self.__c4Code[index]['c1Code']
                        item['c1CoordX'] = self.__c4Code[index]['c1CoordX']
                        item['c1CoordY'] = self.__c4Code[index]['c1CoordY']
                        item['c1NameKR'] = self.__c4Code[index]['c1NameKR']
                        item['c2Code'] = self.__c4Code[index]['c2Code']
                        item['c2NameKR'] = self.__c4Code[index]['c2NameKR']
                        item['c3Code'] = self.__c4Code[index]['c3Code']
                        item['c3NameKR'] = self.__c4Code[index]['c3NameKR']
                        item['c3TotalCounts'] = self.__c4Code[index]['c3TotalCounts']
                        item['c4Code'] = self.__c4Code[index]['c4Code']
                        item['c4NameKR'] = self.__c4Code[index]['c4NameKR']
                        item['c4CoordMapX'] = self.__c4Code[index]['c4CoordMapX']
                        item['c4CoordMapY'] = self.__c4Code[index]['c4CoordMapY']
                        item['c4TradeCounts'] = self.__c4Code[index]['c4TradeCounts']
                        item['c4LeaseCounts'] = self.__c4Code[index]['c4LeaseCounts']
                        item['c4RentCounts'] = self.__c4Code[index]['c4RentCounts']

                        self.__c4List.append(item)

                        #print(sub['c4MaemulType'], sub['c4SellingType'], item['c4NameKR'], sub['c4SellingPrice'])

                    break

        end_time = time.clock()
        self.__elapsedtime_c4 = end_time - start_time
        if self.__DEBUG:
            print("DEBUG: Elapsed time for c4 parsing : %f sec." % self.__elapsedtime_c4)
        IO.staticWriteJSON('2016-02-15-c4List.json', self.__c4List)

    def __get_c4listparsing(self, text, index, url):
        soup = bs4.BeautifulSoup(text, "html.parser")
        maemul_name = soup.findAll('caption', {'class': 'blind_caption'})

        check_maemul = soup.find('table', {'class': 'sale_list _tb_site_img NE=a:cpm'})
        agent_maemul = soup.find('table', {'class': 'sale_list NE=a:prm'})

        num_totalsales = int(self.__c4Code[index]['c4TradeCounts']) + int(self.__c4Code[index]['c4LeaseCounts']) + int(self.__c4Code[index]['c4RentCounts'])
        num_pages = num_totalsales // 30 + 1

        sub_lists = list()
        self.__get_c4listparsing_core(check_maemul, sub_lists, u'확인 매물')
        self.__get_c4listparsing_core(agent_maemul, sub_lists, u'공인중개사협회매물')

        for i in range(2, num_pages+1):
            num_attempts = 1
            page_url = url + '&page=' + str(i)
            while num_attempts < self.__RETRIES:
                if self.__DEBUG:
                    print("DEBUG: get_c4list: %s requesting...(%d/%d page)" % (page_url, i, num_pages), end=" ")

                try:
                    r_sub = requests.get(page_url, timeout=self.__TIMEOUT)
                except requests.exceptions.RequestException as e:
                    print(e)
                    print("Retry to connect ... %d/%d" % (num_attempts+1, self.__RETRIES))
                    num_attempts += 1
                else:
                    if self.__DEBUG:
                        print("Done")

                    soup_sub = bs4.BeautifulSoup(r_sub.text, "html.parser")

                    checkmaemul_sub = soup_sub.find('table', {'class': 'sale_list _tb_site_img NE=a:cpm'})
                    agentmaemul_sub = soup_sub.find('table', {'class': 'sale_list NE=a:prm'})
                    self.__get_c4listparsing_core(checkmaemul_sub, sub_lists, u'확인 매물')
                    self.__get_c4listparsing_core(agentmaemul_sub, sub_lists, u'공인중개사협회매물')

                    break

        return sub_lists

    @staticmethod
    def __get_c4listparsing_core(text, sublist, maemul_name):
        try:
            item_list = text.find('tbody').findAll('tr')
        except AttributeError:
            return None
        else:
            num_subitems = len(item_list) // 2
            for i in range(num_subitems):
                item = dict()
                # 8td & 9td
                # check
                # http://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=&rletNo=104598 

                item['c4MaemulType'] = maemul_name
                subitems = item_list[i*2 + 0].findAll('td')
                #td 1
                selling_type = subitems[0].find('div', {'class': 'inner'}).text

                #td 7
                try:
                    selling_price = subitems[6].find('strong')['title']
                except KeyError:
                    selling_price = subitems[6].find('strong').text.strip()
                item['c4SellingType'] = selling_type
                item['c4SellingPrice'] = selling_price

                sublist.append(item)
