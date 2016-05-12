import time

class timestamp:
    def __init__(self, tag):
        self.__isUse = False
        self.__tag = tag
        self.__start_time = 0
        self.__end_time = 0
        self.__elapsed_time = 0

    def start(self):
        if self.__isUse is True:
            self.__start_time = 0
            self.__end_time = 0
            self.__elapsed_time = 0
            self.__isUse = False

        self.__isUse = True
        self.__start_time = time.clock()

    def stop(self):
        self.__isUse = False
        self.__end_time = time.clock()

    def showLog(self):
        self.__elapsed_time = self.__end_time - self.__start_time
        print("%s: Elapsed time = %f sec." % (self.__tag,  self.__elapsed_time))
