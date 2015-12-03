import bs4
import time

def getTick():
    return time.clock()

def getCortarNoC2(str):
    # target parsing context
    cortarNo_list = []
    soup = bs4.BeautifulSoup(str, "html.parser")

    #checking class2?
    address_list = soup.find('div', {"class" : "address_list  NE=a:lcl"})
    flagNumberStr = address_list.find('h3', {"class" : "area_tit"})
    span = flagNumberStr.find('span')
    if span == None:
        table = soup.find('div', {"class" : "area scroll"})
        list = table.findAll('li')

        for i in range(len(list)):
            cortarNo = {}
            tmp = list[i].find('a')["onclick"]
            code = tmp.split('(',1)[1].split(')')[0].split("'",1)[1].split("'")[0]
            cortarNo["name"] = list[i].text
            cortarNo["code"] = code
            cortarNo_list.append(cortarNo)

    else:
        selectBox = soup.find('div', {"class" : "selectbox-list"})
        table = selectBox.findAll('li')
        list = table.find('li', {"class" : "selectbox-item selectbox-item-selected selectbox-item-over"})
        print list.text
        cortarNo = {}
        cortarNo_list.append(cortarNo)

    return cortarNo_list
