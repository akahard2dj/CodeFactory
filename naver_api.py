import requests
import json
import pymysql

class MySQLQeury:
	def __init__(self):
		self.__passwd = 'boradowon$'
		self.__dbname = 'realestate_db'
		self.__dbuser = 'root'
		self.__dbloc = 'localhost'
		self.__conn = pymysql.connect(host=self.__dbloc, port=3306, user=self.__dbuser, passwd=self.__passwd, db=self.__dbname, use_unicode=True, charset='utf8')
		self.__cur = self.__conn.cursor()
		
	def __del__(self):
		self.__cur.close()
		self.__conn.close()
		
	def get_c2code(self, conditions):
		query_msg = "select c2Code from c2 where c2NameKR = '%s' and c1NameKR = '서울시'" % conditions
		self.__cur.execute(query_msg)
		res = None
		for sub in self.__cur:
			res = (sub[0])
			print(res)
			
		return res


def get_json(query):
	url = 'https://openapi.naver.com/v1/map/geocode?clientId=VpXsKYJAWAdIttaJ7bD9&query='+query
	#url = 'https://openapi.naver.com/v1/map/reversegeocode?clientId=VpXsKYJAWAdIttaJ7bD9&query=127.0824312,37.5383578'
	params = {'clientId':'VpXsKYJAWAdIttaJ7bD9', 'query':query}
	headers = {
		'Host': 'openapi.naver.com',
		'User-Agent': 'curl/7.43.0',
		'Accept': '*/*',
		'Content-Type': 'application/json',
		'X-Naver-Client-Id': 'VpXsKYJAWAdIttaJ7bD9',
		'X-Naver-Client-Secret': 'SY8TyTD5hB',
		}
		
	r = requests.get(url, data=json.dumps(params), headers=headers)
	return (json.loads(r.text))
	
def get_json2(query):
	#url = 'https://openapi.naver.com/v1/map/geocode?clientId=VpXsKYJAWAdIttaJ7bD9&query=자양동 777'
	url = 'https://openapi.naver.com/v1/map/reversegeocode?clientId=VpXsKYJAWAdIttaJ7bD9&query=' + query
	params = {'clientId':'VpXsKYJAWAdIttaJ7bD9', 'query':query}
	headers = {
		'Host': 'openapi.naver.com',
		'User-Agent': 'curl/7.43.0',
		'Accept': '*/*',
		'Content-Type': 'application/json',
		'X-Naver-Client-Id': 'VpXsKYJAWAdIttaJ7bD9',
		'X-Naver-Client-Secret': 'SY8TyTD5hB',
		}
		
	r = requests.get(url, data=json.dumps(params), headers=headers)
	return (json.loads(r.text))
	
mysql = MySQLQeury()
with open('seoul_c2.csv') as f:
	content = f.readlines()
	
fid = open('gps_seoul_c2.csv', 'w')
for line in content:
	sub = line.split(',')
	query = '%s %s' % (sub[2], sub[3])
	
	res = get_json(query)
	lat = res['result']['items'][0]['point']['y']
	lng = res['result']['items'][0]['point']['x']
	query = '%s,%s' % (lng,lat)
	res = (get_json2(query))
	c2name = (res['result']['items'][0]['addrdetail']['sigugun'])
	c2code = mysql.get_c2code(c2name)
	write_msg = '%s,%s,%s\n' % (lng, lat, c2code)
	fid.write(write_msg)
	
fid.close()
