import datatype
import timestamp
import IO
import bs4
import requests
import requests.exceptions

class MyRequests:
    def __init__(self, text):
        self.text = text

    def get_c1code(self):
        soup = bs4.BeautifulSoup(self.text, "html.parser")
        selectbox = soup.find("select", {"class": "selectbox-source"})
        option_lists = selectbox.findAll("option")

        c1lists = list()
        for option in option_lists:
            builder = datatype.C1Code.Builder()
            builder.set_c1code(option['value'])
            builder.set_c1coord(option['xcrdn'], option['ycrdn'])
            builder.set_c1namekr(option.text)

            c1 = builder.build()
            c1lists.append(c1)

        return c1lists

    def get_c2code(self):
        soup = bs4.BeautifulSoup(self.text, "html.parser")
        c1arealist = soup.find('div', {'id': 'loc_view1'}).findAll('option')
        for c1 in c1arealist:
            if c1.has_attr('selected'):
                print(c1)


class Parsing:

    def __init__(self):
        self.__RETRIES = 10
        self.__TIMEOUT = 1.0
        self.__DEBUG = True
        self.estateCode = 'A01'
        self.c1Code = list()
        self.c2Code = list()
        self.url_list = list()

    def request_routine(self, tag, var_name, subfunc_name):


        #url = 'http://land.naver.com'

        for idx, url in enumerate(self.url_list):
            t1 = timestamp.Timestamp(tag)
            t1.start()

            num_attempts = 1
            while num_attempts < self.__RETRIES:
                if self.__DEBUG:
                    print("DEBUG: %s: %s requesting..." % (tag, url), end=" ")

                try:
                    r = requests.get(url, timeout=self.__TIMEOUT)
                except requests.exceptions.RequestException as e:
                    print("Requests Error Msg: %s" % e)
                    print("Retrying to connect ... %d/%d" % (num_attempts+1, self.__RETRIES))
                    num_attempts += 1
                else:
                    my_cls = MyRequests(r.text)
                    method = None
                    try:
                        method = getattr(my_cls, subfunc_name)
                    except AttributeError:
                        raise NotImplementedError("Class `{}` does not implement `{}`".format(my_cls.__class__.__name__, subfunc_name))

                    #self.__c1Code = method(idx)
                    setattr(self, var_name, method())
                    #self.__get_c1code(r.text)
                    if self.__DEBUG:
                        print("Done")
                    break

            t1.stop()

            if num_attempts == 5:
                print("Error: There is no parsed data.")
                return 0

            if self.__DEBUG:
                t1.show_log()

    @property
    def c1code(self):
        return self.c1Code

    @c1code.setter
    def c1code(self, filename):
        self.c1Code = IO.c1_load_json(filename)

    def load_c1code(self, filename):
        self.c1Code = IO.c1_load_json(filename)

    def parsing_c1code_ver2(self):
        url = 'http://land.naver.com'

        if not self.url_list:
            del self.url_list[:]

        self.url_list.append(url)
        self.request_routine('c1code', 'c1Code', 'get_c1code')

    @property
    def c2code(self):
        return self.c2Code

    @c2code.setter
    def c2code(self, filename):
        self.c1Code = IO.c1_load_json(filename)

    def parsing_c2code(self):
        if not self.c1Code:
            return None

        if not self.url_list:
            del self.url_list[:]

        for code in self.c1Code:
            url1 = "http://land.naver.com/article/cityInfo.nhn?rletTypeCd="
            url2 = "&tradeTypeCd=&hscpTypeCd=&cortarNo="
            url = url1 + self.estateCode + url2 + code.c1Code
            self.url_list.append(url)

        self.request_routine('c2code', 'c2Code', 'get_c2code')
