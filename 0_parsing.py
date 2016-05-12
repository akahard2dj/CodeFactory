import datatype
import timestamp
import IO
import bs4
import requests
import requests.exceptions

class parsing():

    def __init__(self):
        self.__RETRIES = 10
        self.__TIMEOUT = 1.0
        self.__DEBUG = True
        self.__c1Code = list()


    @property
    def c1code(self):
        return self.__c1Code

    @c1code.setter
    def c1code(self, filename):
        self.__c1Code = IO.c1_load_json(filename)

    def parsing_c1code(self):
        t1 = timestamp.timestamp('c1code')
        t1.start()

        url = 'http://land.naver.com'

        num_attempts = 1
        while num_attempts < self.__RETRIES:
            if self.__DEBUG:
                print("DEBUG: c1code: %s requesting..." % url, end=" ")

            try:
                r = requests.get(url, timeout=self.__TIMEOUT)
            except requests.exceptions.RequestException as e:
                print("Requests Error Msg: %s" % e)
                print("Retrying to connect ... %d/%d" % (num_attempts+1, self.__RETRIES))
                num_attempts += 1
            else:
                self.__get_c1code(r.text)
                if self.__DEBUG:
                    print("Done")
                break
        t1.stop()

        if num_attempts == 5:
            print("Error: There is no parsed data.")
            return 0

        if self.__DEBUG:
            t1.showLog()

    def __get_c1code(self, text):
        soup = bs4.BeautifulSoup(text, "html.parser")
        selectbox = soup.find("select", {"class": "selectbox-source"})
        option_lists = selectbox.findAll("option")

        for option in option_lists:
            c1 = datatype.c1code()
            c1.set_c1code(option)
            self.__c1Code.append(c1)

