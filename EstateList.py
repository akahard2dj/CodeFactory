import bs4
import requests
import requests.exceptions
import time
import IO


class EstateList:

    def __init__(self):
        self.__c1Code = list()
        self.__c2Code = list()
        self.__estateCode = 'A01'
        self.__RETRIES = 5
        self.__TIMEOUT = 0.001
        self.__DEBUG = False
        self.__elapsedtime_c1 = 0.0
        self.__elaspedtime_c2 = 0.0

    def set_debug(self, flag):
        self.__DEBUG = flag

    def set_estatecode(self, estatecode):
        self.__estateCode = estatecode

    def get_c1code(self):
        return self.__c1Code

    def set_c1code(self, fname, flag):
        if flag:
            self.__c1Code = IO.loadJSON(fname)
        else:
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

    def get_c2code(self):
        return self.__c2Code

    def set_c2code(self, fname, flag):
        if flag:
            self.__c2Code = IO.loadJSON(fname)
        else:
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
                    print("DEBUG: get_c2code: %s requesting..." % url, end=" ")

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
        self.__elaspedtime_c2 = end_time - start_time
        if self.__DEBUG:
            print("DEBUG: Elapsed time for c2 parsing : %f sec." % self.__elaspedtime_c2)
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
