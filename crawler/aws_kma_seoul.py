import requests
import json


class GeoInfoWeatherObservationWGS(object):
    def __init__(self, key=''):
        self._key = key
        self.__base_url = 'http://openAPI.seoul.go.kr:8088/{}/json/GeoInfoWeatherObservationWGS/1/100'.format(key)




'''
url='http://openAPI.seoul.go.kr:8088/{}/json/GeoInfoWeatherObservationWGS/1/100'.format(key)
res = requests.get(url)
json_data = json.loads(res.text)

f = open('observatory_seoul.csv', 'w')
for obs_item in json_data["GeoInfoWeatherObservationWGS"]["row"]:
    msg = "{},{},{},{},{},{},{},\n".format(
        obs_item['OBJECTID'], obs_item["AWS_CDE"], obs_item["NAM"], obs_item["AWS_GBN"], obs_item["LNG"],
        obs_item["LAT"], obs_item["ADDRESS"]
    )
    f.write(msg)
f.close()

'''
'''
url = 'http://openAPI.seoul.go.kr:8088/{}/json/RealtimeWeatherStation/1/100/ '.format(key)
res = requests.get(url)
json_data = json.loads(res.text)


for weather_item in json_data["RealtimeWeatherStation"]["row"]:
    print(weather_item)

print(json.dumps(json_data, indent=4))
'''

'''
from selenium import webdriver

driver = webdriver.Chrome('d:\\Workspaces\\Server\\SeoulWind\\chromedriver')
driver.implicitly_wait(3)

driver.get('http://aws.seoul.go.kr/RealTime/RealTimeWeatherUser.asp?TITLE=%C0%FC%20%C1%F6%C1%A1%20%C7%F6%C8%B2')


print(driver.page_source)
'''

import requests
from bs4 import BeautifulSoup

url = 'http://aws.seoul.go.kr/RealTime/RealTimeWeatherUser.asp?TITLE=%C0%FC%20%C1%F6%C1%A1%20%C7%F6%C8%B2'
res = requests.get(url)
res.encoding = 'EUC-KR'

soup = BeautifulSoup(res.text, "html.parser")
current_time_html = soup.find('td', {'class': 'explain'}).text.rstrip().strip()
tmp = current_time_html.split(' ')

current_time_str = ''
for time_item in tmp[:-1]:
    current_time_str += str(time_item[:-1])
    
current_time_str += tmp[-1][:2]
print(current_time_str)


data_boxes = soup.find_all('td', {'valign': 'top'})
aws_seoul_items = data_boxes[0].find_all('tr', {'valign': 'top'})
for aws_seoul in aws_seoul_items[1:]:
    spot_data = aws_seoul.find_all('td')

    name = spot_data[1].text.strip()
    wind_dir_value = spot_data[2].text.strip()
    wind_dir_str = spot_data[3].text.strip()
    wind_speed = spot_data[4].text.strip()
    temp = spot_data[5].text.strip()
    preci = spot_data[6].text.strip()
    rain = spot_data[7].text.strip()
    hum = spot_data[8].text.strip()
    sol_rad = spot_data[9].text.strip()
    sunshine = spot_data[10].text.strip()
    print(name, wind_dir_str, wind_speed, temp, preci, rain, hum, sol_rad, sunshine)

aws_kma_items = data_boxes[1].find_all('tr', {'valign': 'top'})
for aws_kma in aws_kma_items[1:]:
    spot_data = aws_kma.find_all('td')

    name = spot_data[1].text.strip()
    wind_dir_value = spot_data[2].text.strip()
    wind_dir_str = spot_data[3].text.strip()
    wind_speed = spot_data[4].text.strip()
    temp = spot_data[5].text.strip()
    preci = spot_data[6].text.strip()
    rain = spot_data[7].text.strip()
    hum = spot_data[8].text.strip()
    #sol_rad = spot_data[9].text.strip()
    #sunshine = spot_data[10].text.strip()
    print(name, wind_dir_str, wind_speed, temp, preci, rain, hum, sol_rad, sunshine)
