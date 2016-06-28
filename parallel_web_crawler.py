from bs4 import BeautifulSoup
from datatype import C1Code, C2Code, C3Code, C4Code, C4List, C4ComplexInfo
from request_manager import RequestManager
import json_utils
import url_info
from timestamp import Timestamp

from mpi4py import MPI
import pymysql
import time

class ParallelWebCrawler:
	def __init__(self):
		self.code = list()
		self.ts = Timestamp()
		self.rm = RequestManager()
		self.estate_code = 'A01'
		self.comm = MPI.COMM_WORLD
		self.size = self.comm.Get_size()
		self.rank = self.comm.Get_rank()
		self.root_rank = 0
		
		self.parse_timestamp = time.strftime("%Y-%m-%d", time.localtime())
		self.conn = None
		self.cur = None
		self.passwd = ''
		self.dbname = ''
		self.dbuser = ''
		self.dbloc = 'localhost'
		
	def request(self):
		raise NotImplementedError()
		
	def parse(self, text, index, url):
		raise NotImplementedError()
		
	def callback(self, data):
		raise NotImplementedError()
		
	def result(self):
		return self.code
		
class C1(ParallelWebCrawler):
	def request(self):
		if self.rank == self.root_rank:
			self.conn = pymysql.connect(host=self.dbloc, user=self.dbuser, passwd=self.passwd, db=self.dbname, 
										use_unicode=True, charset='utf8')
			self.cur = self.conn.cursor()
										
			self.ts.start('request_c1')
			self.rm.request('c1', url_info.C1_URL, self.callback)
			json_utils.write_class("c1CodeClass.json", self.code)
			self.ts.stop()
			self.ts.show_log()
			
			self.cur.close()
			self.conn.commit()
			self.conn.close()
		
	def callback(self, data):
		self.code = self.parse(data.get_html())
		
	def parse(self, text, index=0, url=''):
		soup = BeautifulSoup(text, "html.parser")
		select_box = soup.find("select", {"class": "selectbox-source"})
		option_lists = select_box.findAll("option")
		code_list = list()

		for option in option_lists:
			builder = C1Code.Builder()
			builder.set_c1code(option['value']) \
				.set_c1coord(option['xcrdn'], option['ycrdn']) \
				.set_c1namekr(option.text)
			code_list.append(builder.build())
			query_msg = "insert into c1 (timestamp, c1Code, c1CoordX, c1CoordY, c1NameKR) " \
						"values('%s', '%s', '%s','%s','%s')" % \
						(self.parse_timestamp, option['value'], option['xcrdn'], option['ycrdn'], option.text)
			self.cur.execute(query_msg)

		return code_list
		
class C2(ParallelWebCrawler):
	def __init__(self):
		ParallelWebCrawler.__init__(self)
		#self.__c1Code = c1_code
		self.__c1Code = json_utils.load_c1class('json_data\\2016-06-28\\c1CodeClass.json')
		
	def request(self):
		if not self.__c1Code:
			print('Error: c1code is empty')
			return None
			
		self.conn = pymysql.connect(host=self.dbloc, user=self.dbuser, passwd=self.passwd, db=self.dbname, 
										use_unicode=True, charset='utf8')
		self.cur = self.conn.cursor()
			
		if self.rank == self.root_rank:
			self.ts.start('request_c2')
		
		if self.rank == self.root_rank:
			url_list = list()
			for code in self.__c1Code:
				url = url_info.C2_URL1 + self.estate_code + url_info.C2_URL2 + code.c1Code
				url_list.append(url)
			chunks = [[] for _ in range(self.size)]
			for idx, chunk in enumerate(url_list):
				chunks[idx%self.size].append(chunk)
		
		else:
			url_list = None
			chunks = None
			
		url_list = self.comm.scatter(chunks, root=self.root_rank)
		
		for idx, url in enumerate(url_list):
			self.rm.request('c2', url, self.callback, idx)
		
		gather_code = self.comm.gather(self.code, root=self.root_rank)
		if self.rank == self.root_rank:
			write_code = list()
			for list_code in gather_code:
				for code in list_code:
					write_code.append(code)
			json_utils.write_class('c2CodeClass.json', write_code)
		
		if self.rank == self.root_rank:
			self.ts.stop()
			self.ts.show_log()
			
		self.cur.close()
		for i in range(self.size):
			if self.rank == i:
				self.conn.commit()
		self.conn.close()
			
	def callback(self, data):
		html = data.get_html()
		index = data.get_index()
		idx = index * self.size + self.rank
		for sub in self.parse(html, index):
			builder = C2Code.Builder()
			builder.set_c1code(self.__c1Code[idx]) \
				.set_c2code(sub['c2Code']) \
				.set_c2namekr(sub['c2NameKR'])
			self.code.append(builder.build())
			query_msg = "insert into c2 (timestamp, c1Code, c1CoordX, c1CoordY, c1NameKR, c2Code, c2NameKR) " \
						"values('%s', '%s', '%s','%s','%s', '%s', '%s')" % \
						(self.parse_timestamp,
						 self.__c1Code[idx].c1Code, self.__c1Code[idx].c1CoordX, self.__c1Code[idx].c1CoordY,
						 self.__c1Code[idx].c1NameKR,
						 sub['c2Code'], sub['c2NameKR'])
			self.cur.execute(query_msg)
		
	def parse(self, text, index, url=''):
		code_list = list()
		idx = index * self.size + self.rank
		if self.__c1Code[idx].c1Code == "3600000000":
			item = dict()
			item['c2Code'] = "3611000000"
			item['c2NameKR'] = self.__c1Code[idx].c1NameKR
			code_list.append(item)

		else:
			soup = BeautifulSoup(text, "html.parser")
			area_list = soup.find('div', {'class': 'area scroll'}).findAll('li')

			for sub_code in area_list:
				temp = str(sub_code.find('a')['class']).replace("[", "").replace("]", "").replace("'", "")

				item = dict()
				item['c2Code'] = temp.split(':')[-1]
				item['c2NameKR'] = sub_code.find('a').text
				code_list.append(item)
		
		return code_list
		
class C3(ParallelWebCrawler):
	def __init__(self):
		ParallelWebCrawler.__init__(self)
		self.__c2Code = json_utils.load_c2class('json_data\\2016-06-28\\c2CodeClass.json')
		
	def request(self):
		if not self.__c2Code:
			print('Error: c2code is empty')
			return None
			
		if self.rank == self.root_rank:
			self.ts.start('request_c3')
			
		if self.rank == self.root_rank:
			url_list = list()
			for code in self.__c2Code:
				url = url_info.C3_URL1 + self.estate_code + url_info.C3_URL2 + code.c2Code
				url_list.append(url)
			chunks = [[] for _ in range(self.size)]
			for idx, chunk in enumerate(url_list):
				chunks[idx%self.size].append(chunk)
				
		else:
			url_list = None
			chunks = None
			
		url_list = self.comm.scatter(chunks, root=self.root_rank)
		
		for idx, url in enumerate(url_list):
			self.rm.request('c3', url, self.callback, idx)
			
		gather_code = self.comm.gather(self.code, root=self.root_rank)
		if self.rank == self.root_rank:
			write_code = list()
			for list_code in gather_code:
				for code in list_code:
					write_code.append(code)

			json_utils.write_class('c3CodeClass.json', write_code)

			self.ts.stop()
			self.ts.show_log()
			
	def parse(self, text, index=0, url=''):
		code_list = list()
		soup = BeautifulSoup(text, "html.parser")
		area_list = soup.find('div', {'id': 'divisionScrollList'}).findAll('li')

		for sub_code in area_list:
			c3info = str(sub_code.find('a')['class']).replace("[", "").replace("]", "").replace("'", "")
			count = sub_code.find('em').text.replace("(", "").replace(")", "")

			item = dict()
			item['c3Code'] = c3info.split(':')[-1]
			item['c3NameKR'] = sub_code.find('a').text
			item['c3TotalCounts'] = count

			code_list.append(item)

		return code_list

			
	def callback(self, data):
		html = data.get_html()
		index = data.get_index()
		sub_c3 = self.parse(html)

		for sub in sub_c3:
			builder = C3Code.Builder()
			idx = index * self.size + self.rank
			builder.set_c2code(self.__c2Code[idx]) \
				.set_c3code(sub['c3Code']) \
				.set_c3namekr(sub['c3NameKR']) \
				.set_c3totalcounts(sub['c3TotalCounts'])
			self.code.append(builder.build())

class C4(ParallelWebCrawler):
	def __init__(self):
		ParallelWebCrawler.__init__(self)
		self.__c3Code = json_utils.load_c3class('json_data\\2016-06-28\\c3CodeClass.json')
		self.failed_url_list = list()
		
	def request(self):
		if not self.__c3Code:
			print("Error: c3Code is empty.")
			return None
			
		if self.rank == self.root_rank:
			self.ts.start('request_c4')
			
		if self.rank == self.root_rank:
			url_list = list()
			for code in self.__c3Code:
				url = url_info.C4_URL1 + self.estate_code + url_info.C4_URL2 + code.c3Code
				url_list.append(url)
			chunks = [[] for _ in range(self.size)]
			for idx, chunk in enumerate(url_list):
				chunks[idx%self.size].append(chunk)
		else:
			url_list = None
			chunks = None
			
		url_list = self.comm.scatter(chunks, root=self.root_rank)
		
		for idx, url in enumerate(url_list):
			self.rm.request('c4', url, self.callback, idx)
			
		while len(self.failed_url_list) != 0:
			failed_url = self.failed_url_list.pop()
			self.rm.request('c4', failed_url, self.callback, 0)
			
		gather_code = self.comm.gather(self.code, root=self.root_rank)
		if self.rank == self.root_rank:
			write_code = list()
			for list_code in gather_code:
				for code in list_code:
					write_code.append(code)

			json_utils.write_class('c4CodeClass.json', write_code)

			self.ts.stop()
			self.ts.show_log()
			
	def callback(self, data):
		html = data.get_html()
		index = data.get_index()
		url = data.get_url()

		subc4code = self.parse(html)
		if subc4code is not None:
			for sub in subc4code:
				builder = C4Code.Builder()
				idx = index * self.size + self.rank
				builder.set_c3code(self.__c3Code[idx]) \
					.set_c4code(sub['c4Code']) \
					.set_c4namekr(sub['c4NameKR']) \
					.set_c4coord(sub['c4CoordMapX'], sub['c4CoordMapY']) \
					.set_c4counts(sub['c4TradeCounts'], sub['c4LeaseCounts'], sub['c4RentCounts'])
				self.code.append(builder.build())
		else:
			print("This %s url is seems to be broken." % idx)
			self.failed_url_list.append(url)

	def parse(self, text, index=0, url=''):
		code_list = list()
		soup = BeautifulSoup(text, "html.parser")

		webpage_msg = soup.find('div', {'class': 'housing_inner'})
		if webpage_msg is None:
			return None

		else:
			area_list = soup.find('div', {'class': 'housing_inner'}).findAll('li')

			for sub in area_list:
				item = dict()
				tmp = sub.find('a')
				count = sub.find('em').text.replace("(", "").replace(")", "").split('/')

				item['c4Code'] = tmp['hscp_no']
				item['c4NameKR'] = tmp.text.strip()
				item['c4CoordMapX'] = tmp['mapx']
				item['c4CoordMapY'] = tmp['mapy']
				item['c4TradeCounts'] = count[0]
				item['c4LeaseCounts'] = count[1]
				item['c4RentCounts'] = count[2][:-1]
				item['c4TotalSalesCounts'] = int(count[0]) + int(count[1]) + int(count[2][:-1])
				code_list.append(item)

			return code_list
			
class C4ComplexInfoData(ParallelWebCrawler):
	def __init__(self):	
		ParallelWebCrawler.__init__(self)
		self.__c4Code = json_utils.load_c4class('json_data\\2016-06-28\\c4CodeClass.json')
		self.failed_url_list = list()
		self.failed_index_list = list()

	def request(self):
		if not self.__c4Code:
			print('Error: c4lists is empty')
			return None
			
		if self.rank == self.root_rank:
			self.ts.start('request_c4_complex_info')
			
		if self.rank == self.root_rank:
			url_list = list()
			for code in self.__c4Code:
				url = url_info.C4_LIST_URL1 + url_info.C4_LIST_URL_TAB[2] + url_info.C4_LIST_URL2 + \
					self.estate_code + url_info.C4_LIST_URL3 + code.c4Code
				url_list.append(url)
			chunks = [[] for _ in range(self.size)]
			for idx, chunk in enumerate(url_list):
				chunks[idx%self.size].append(chunk)
		else:
			url_list = None
			chunks = None
			
		url_list = self.comm.scatter(chunks, root=self.root_rank)

		for idx, url in enumerate(url_list):
			self.rm.request('c4_complex_info', url, self.callback, idx)

		while len(self.failed_url_list) != 0:
			failed_url = self.failed_url_list.pop()
			failed_index = self.failed_index_list.pop()
			self.rm.request('c4_complex_info', failed_url, self.callback, failed_index)

		gather_code = self.comm.gather(self.code, root=self.root_rank)
		if self.rank == self.root_rank:
			write_code = list()
			for list_code in gather_code:
				for code in list_code:
					write_code.append(code)

			json_utils.write_class('c4ComplexInfo.json', write_code)

			self.ts.stop()
			self.ts.show_log()

	def callback(self, data):
		html = data.get_html()
		index = data.get_index()
		url = data.get_url()

		self.parse(html, index, url)

	@staticmethod
	def __get_c4complexinfo_A(text):
		item = dict()

		soup = BeautifulSoup(text, "html.parser")
		housing_info = soup.find('table', {'class': 'housing_info'}).find('tbody')

		info_tables = housing_info.findAll('tr')
		num_tables = len(info_tables)

		n_houses = info_tables[0].find('strong').text
		n_building = info_tables[0].find('td', {'tabindex': '0'}).text

		built_date = info_tables[1].findAll('td')[0].text
		construction_company = info_tables[1].findAll('td')[1].text

		total_parkinglots = info_tables[2].findAll('td')[0].text
		parkinglot_per_house = info_tables[2].findAll('td')[1].text

		heating_type = info_tables[3].findAll('td')[0].text
		fuel_for_heating = info_tables[3].findAll('td')[1].text

		floor_area_ratio = info_tables[4].findAll('td')[0].text
		coverage_ratio = info_tables[4].findAll('td')[1].text

		highest_floor = info_tables[5].findAll('td')[0].text
		lowest_floor = info_tables[5].findAll('td')[1].text

		area_type_int = list()
		area_type_float = list()
		area_type = info_tables[6].findAll('span')

		for area in area_type:
			area_type_int.append(area['title'].split()[1])
			area_type_float.append(area.text)

		admin_office_tel = 'None'
		if num_tables == 8:
			admin_office_tel = info_tables[7].find('span')['title']

		add_base = soup.find('li', {'class': 'info info_v2'})
		address1 = add_base.text.split('도로명')[0].replace('\n', '').strip()

		try:
			road_add_raw = add_base.find('a', {'href': 'javascript:showRoadAddrLayer()'})
			address2 = road_add_raw.find('span', {'class': 'ly_tx'}).find('em').text.strip()
		except AttributeError:
			address2 = 'None'

		item['n_tot_houses'] = n_houses
		item['n_building'] = n_building
		item['n_houses'] = n_houses
		item['n_longterm_rent'] = 0
		item['built_date'] = built_date
		item['construction_company'] = construction_company
		item['total_parkinglots'] = total_parkinglots
		item['parkinglot_per_house'] = parkinglot_per_house
		item['heating_type'] = heating_type
		item['fuel_for_heating'] = fuel_for_heating
		item['floor_area_ratio'] = floor_area_ratio
		item['coverage_ratio'] = coverage_ratio
		item['highest_floor'] = highest_floor
		item['lowest_floor'] = lowest_floor
		item['area_type_int'] = area_type_int
		item['area_type_float'] = area_type_float
		item['admin_office_tel'] = admin_office_tel
		item['address1'] = address1
		item['address2'] = address2

		return item

	@staticmethod
	def __get_c4complexinfo_B(text):
		item = dict()

		soup = BeautifulSoup(text, "html.parser")
		housing_info = soup.find('table', {'class': 'housing_info'}).find('tbody')

		info_tables = housing_info.findAll('tr')
		num_tables = len(info_tables)

		tot_house = info_tables[0].findAll('strong')
		n_tot_house = tot_house[1].text

		str_n_house = info_tables[1].find('br').text.replace('\t', '').replace('\r', '').replace('\n', '').split()
		n_houses = str_n_house[1]
		n_longterm_rent = str_n_house[4]

		n_building = info_tables[2].findAll('td')[0].text
		built_date = info_tables[2].findAll('td')[1].text

		construction_company = info_tables[3].findAll('td')[0].text
		total_parkinglots = info_tables[3].findAll('td')[1].text

		parkinglot_per_house = info_tables[4].findAll('td')[0].text
		heating_type = info_tables[4].findAll('td')[1].text

		fuel_for_heating = info_tables[5].findAll('td')[0].text
		floor_area_ratio = info_tables[5].findAll('td')[1].text

		coverage_ratio = info_tables[6].findAll('td')[0].text
		highest_floor = info_tables[6].findAll('td')[1].text

		lowest_floor = info_tables[7].findAll('td')[0].text

		area_type_int = list()
		area_type_float = list()
		area_type = info_tables[7].findAll('span')

		for area in area_type:
			area_type_int.append(area['title'].split()[1])
			area_type_float.append(area.text)

		admin_office_tel = 'None'
		if num_tables == 9:
			admin_office_tel = info_tables[8].find('span')['title']

		add_base = soup.find('li', {'class': 'info info_v2'})
		address1 = add_base.text.split('도로명')[0].replace('\n', '').strip()

		try:
			road_add_raw = add_base.find('a', {'href': 'javascript:showRoadAddrLayer()'})
			address2 = road_add_raw.find('span', {'class': 'ly_tx'}).find('em').text.strip()
		except AttributeError:
			address2 = 'None'

		item['n_tot_houses'] = n_tot_house
		item['n_building'] = n_building
		item['n_houses'] = n_houses
		item['n_longterm_rent'] = n_longterm_rent
		item['built_date'] = built_date
		item['construction_company'] = construction_company
		item['total_parkinglots'] = total_parkinglots
		item['parkinglot_per_house'] = parkinglot_per_house
		item['heating_type'] = heating_type
		item['fuel_for_heating'] = fuel_for_heating
		item['floor_area_ratio'] = floor_area_ratio
		item['coverage_ratio'] = coverage_ratio
		item['highest_floor'] = highest_floor
		item['lowest_floor'] = lowest_floor
		item['area_type_int'] = area_type_int
		item['area_type_float'] = area_type_float
		item['admin_office_tel'] = admin_office_tel
		item['address1'] = address1
		item['address2'] = address2

		return item

	def parse(self, text, index, url):
		soup = BeautifulSoup(text, "html.parser")

		webpage_msg = soup.find('table', {'class': 'housing_info'})
		if webpage_msg is None:
			self.failed_url_list.append(url)
			self.failed_index_list.append(index)

		else:
			try:
				housing_info = soup.find('table', {'class': 'housing_info'}).find('tbody')
				_ = housing_info.find('strong', {'class': 'bu'}).text
			except AttributeError:
				item = self.__get_c4complexinfo_A(text)
			else:
				item = self.__get_c4complexinfo_B(text)

			builder = C4ComplexInfo.Builder()
			builder.set_c4complex_row1(
				item['n_tot_houses'], item['n_building'], item['n_houses'], item['n_longterm_rent']) \
				.set_c4complex_row2(item['built_date'], item['construction_company']) \
				.set_c4complex_row3(item['total_parkinglots'], item['parkinglot_per_house']) \
				.set_c4complex_row4(item['heating_type'], item['fuel_for_heating']) \
				.set_c4complex_row5(item['floor_area_ratio'], item['coverage_ratio']) \
				.set_c4complex_row6(item['highest_floor'], item['lowest_floor']) \
				.set_c4complex_row7(item['area_type_float'], item['area_type_int']) \
				.set_c4complex_row8(item['admin_office_tel']) \
				.set_c4complex_address(item['address1'], item['address2'])
			self.code.append(builder.build())

class C4Lists(ParallelWebCrawler):
	def __init__(self):
		ParallelWebCrawler.__init__(self)
		self.__c4Code = json_utils.load_c4class('json_data\\2016-06-28\\c4CodeClass.json')

	def request(self):
		if not self.__c4Code:
			print("Error: c4code is empty.")
			return None
			
		if self.rank == self.root_rank:
			self.ts.start('request_c4list')
			
		if self.rank == self.root_rank:
			url_list = list()
			for code in self.__c4Code:
				url = url_info.C4_LIST_URL1 + url_info.C4_LIST_URL_TAB[0] + url_info.C4_LIST_URL2 + \
				self.estate_code + url_info.C4_LIST_URL3 + code.c4Code
				url_list.append(url)
			chunks = [[] for _ in range(self.size)]
			for idx, chunk in enumerate(url_list):
				chunks[idx%self.size].append(chunk)
		else:
			url_list = None
			chunks = None
			
		url_list = self.comm.scatter(chunks, root=self.root_rank)

		for idx, url in enumerate(url_list):
			self.rm.request('c4_complex_info', url, self.callback, idx)

		if self.rank == self.root_rank:
			self.ts.stop()
			self.ts.show_log()

	def callback(self, data):
		index = data.get_index()
		html = data.get_html()
		url = data.get_url()
		subc4list = self.parse(html, index, url)

		c4code_list = list()
		idx = index * self.size + self.rank
		for sub in subc4list:
			builder = C4List.Builder()
			builder.set_c4code(self.__c4Code[idx]) \
				.set_c4sellinginfo(sub['c4MaemulType'], sub['c4SellingType'], sub['c4SellingDate'],
								   sub['c4SellingStatus'], sub['c4SellingStatusCaption'],
								   sub['c4SellingDetailLink']) \
				.set_c4selling_buildinginfo(sub['c4SellingAreaType'], sub['c4SellingSupplyArea'],
											sub['c4SellingNetArea'], sub['c4SellingComplex'], sub['c4SellingFloor'],
											sub['c4SellingTotalFloor'], sub['c4SellingPrice']) \
				.set_c4selling_agentinfo(sub['c4SellingAgentName'], sub['c4SellingAgentTel'], sub['c4SellingAgentCode'],
										 sub['c4SellingAgentComment'], sub['c4SellingSource'],
										 sub['c4SellingSourceLink'], sub['c4SellingClass'])
			c4code_list.append(builder.build())
			
		json_utils.write_c4list_class(self.__c4Code[idx].c4Code, c4code_list)

	def parse(self, text, index, url):
		soup = BeautifulSoup(text, "html.parser")
		maemul_name = soup.findAll('caption', {'class': 'blind_caption'})

		check_maemul = soup.find('table', {'class': 'sale_list _tb_site_img NE=a:cpm'})
		agent_maemul = soup.find('table', {'class': 'sale_list NE=a:prm'})
		num_totalsales = \
			int(self.__c4Code[index].c4TradeCounts) + \
			int(self.__c4Code[index].c4LeaseCounts) + \
			int(self.__c4Code[index].c4RentCounts)
		num_pages = num_totalsales // 30 + 1

		sub_lists = list()
		self.__get_c4list_parsing_core(check_maemul, sub_lists, '확인 매물')
		self.__get_c4list_parsing_core(agent_maemul, sub_lists, '공인중개사협회매물')

		for i in range(2, num_pages + 1):
			page_url = url + '&page=' + str(i)
			RequestManager().request('c4_list_parse', page_url, self.c4_list_parsing_callback, i, sub_lists)

		return sub_lists

	@staticmethod
	def __get_c4list_parsing_core(text, sublist, maemul_name):
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
				subitems = item_list[i * 2 + 0].findAll('td')
				subitems2 = item_list[i * 2 + 1].findAll('td')
				num_tdcounts = len(subitems)

				if maemul_name == '공인중개사협회매물':
					# td 1 - selling type
					selling_type = subitems[0].find('div', {'class': 'inner'}).text

					# td 2 - selling date
					selling_date = subitems[1].text

					# td 4 - area
					arealist = subitems[3].find('div', {'class': 'inner'}).text.strip().split()
					selling_areatype = arealist[0]
					selling_supplyarea = arealist[2]
					selling_netarea = arealist[4]

					# td 5 - complex
					selling_complex = subitems[4].find('div').text

					# td 6 - floor
					floorlist = subitems[5].find('div').text.split('/')
					selling_floor = floorlist[0]
					selling_totalfloor = floorlist[1]

					# td 7 - price

					selling_price = subitems[6].find('strong').text

					# td 8 - contact
					agent_name = subitems[7].findAll('span')[0]['title']
					agent_tel = subitems[7].findAll('span')[1].text
					try:
						tmp = subitems[7].find('a')['href']
						agent_code = tmp.split('(', 1)[1].split(')')[0].split("'", 1)[1].split("'")[0]
					except TypeError:
						agent_code = 'NoCode'

					# td 1 - comment & agent
					agent_comment = subitems2[0].findAll('span')[0]['title'].replace('\n', '').replace('\r', '').strip()

					#selling_source = subitems2[0].findAll('span')[1].text.strip()
					selling_source = ''

					item['c4SellingType'] = selling_type
					item['c4SellingDate'] = selling_date
					item['c4SellingStatus'] = ""
					item['c4SellingStatusCaption'] = ""
					item['c4SellingDetailLink'] = ""
					item['c4SellingAreaType'] = selling_areatype
					item['c4SellingSupplyArea'] = selling_supplyarea
					item['c4SellingNetArea'] = selling_netarea
					item['c4SellingComplex'] = selling_complex
					item['c4SellingFloor'] = selling_floor
					item['c4SellingTotalFloor'] = selling_totalfloor
					item['c4SellingPrice'] = selling_price
					item['c4SellingAgentName'] = agent_name
					item['c4SellingAgentTel'] = agent_tel
					item['c4SellingAgentCode'] = agent_code
					item['c4SellingAgentComment'] = agent_comment
					item['c4SellingSource'] = selling_source
					item['c4SellingSourceLink'] = ""
					item['c4SellingClass'] = maemul_name

				if maemul_name == '확인 매물' and num_tdcounts == 8:
					# td 1 - selling type
					selling_type = subitems[0].find('div', {'class': 'inner'}).text

					# td 2 - selling price
					selling_date = subitems[1].find('span').text
					selling_check = subitems[1].find('span')['class'][0]
					try:
						selling_checkcaption = subitems[1].find('span')['title']
					except KeyError:
						selling_checkcaption = subitems[1].find('img')['alt']

					# td 3 - detail link
					selling_detail_link = subitems[2].findAll('a')[1]['href']

					# td 4 - area
					arealist = subitems[3].find('div', {'class': 'inner'}).text.strip().split()
					selling_areatype = arealist[0]
					selling_supplyarea = arealist[2]
					selling_netarea = arealist[4]

					# td 5 - complex
					selling_complex = subitems[4].find('div').text

					# td 6 - floor
					floorlist = subitems[5].find('div').text.split('/')
					selling_floor = floorlist[0]
					selling_totalfloor = floorlist[1]

					# td 7 - price
					try:
						selling_price = subitems[6].find('strong')['title']
					except KeyError:
						selling_price = subitems[6].find('strong').text.strip()

					# td 8 - contact
					agent_name = subitems[7].findAll('span')[0]['title']
					agent_tel = subitems[7].findAll('span')[1].text
					try:
						tmp = subitems[7].find('a')['href']
						agent_code = tmp.split('(', 1)[1].split(')')[0].split("'", 1)[1].split("'")[0]
					except TypeError:
						agent_code = 'NoCode'
					# td 1 - comment & agent
					agent_comment = subitems2[0].find('span')['title'].replace('\n', '').replace('\r', '').strip()

					selling_source = subitems2[0].find('a').text
					selling_sourcelink = subitems2[0].find('a')['href']

					item['c4SellingType'] = selling_type
					item['c4SellingDate'] = selling_date
					item['c4SellingStatus'] = selling_check
					item['c4SellingStatusCaption'] = selling_checkcaption
					item['c4SellingDetailLink'] = selling_detail_link
					item['c4SellingAreaType'] = selling_areatype
					item['c4SellingSupplyArea'] = selling_supplyarea
					item['c4SellingNetArea'] = selling_netarea
					item['c4SellingComplex'] = selling_complex
					item['c4SellingFloor'] = selling_floor
					item['c4SellingTotalFloor'] = selling_totalfloor
					item['c4SellingPrice'] = selling_price
					item['c4SellingAgentName'] = agent_name
					item['c4SellingAgentTel'] = agent_tel
					item['c4SellingAgentCode'] = agent_code
					item['c4SellingAgentComment'] = agent_comment
					item['c4SellingSource'] = selling_source
					item['c4SellingSourceLink'] = selling_sourcelink
					item['c4SellingClass'] = maemul_name

				if maemul_name == '확인 매물' and num_tdcounts == 9:
					# td 1
					selling_type = subitems[0].find('div', {'class': 'inner'}).text

					# td 2 - selling price
					selling_date = subitems[1].find('span').text
					selling_check = subitems[1].find('span')['class'][0]
					try:
						selling_checkcaption = subitems[1].find('span')['title']
					except KeyError:
						selling_checkcaption = ""

					# td 3 - detail link
					selling_detail_link = subitems[3].findAll('a')[1]['href']

					# td 4 - area
					arealist = subitems[4].find('div', {'class': 'inner'}).text.strip().split()
					selling_areatype = arealist[0]
					selling_supplyarea = arealist[2]
					selling_netarea = arealist[4]

					# td 5 - complex
					selling_complex = subitems[5].find('div').text

					# td 6 - floor
					floorlist = subitems[6].find('div').text.split('/')
					selling_floor = floorlist[0]
					selling_totalfloor = floorlist[1]

					# td 7 - price
					try:
						selling_price = subitems[7].find('strong')['title']
					except KeyError:
						selling_price = subitems[7].find('strong').text.strip()

					# td 8 - contact
					agent_name = subitems[8].findAll('span')[0]['title']
					agent_tel = subitems[8].findAll('span')[1].text
					try:
						tmp = subitems[8].find('a')['href']
						agent_code = tmp.split('(', 1)[1].split(')')[0].split("'", 1)[1].split("'")[0]
					except TypeError:
						agent_code = 'NoCode'
					# td 1 - comment & agent
					agent_comment = subitems2[0].find('span')['title'].strip()

					selling_source = subitems2[0].find('a').text
					selling_sourcelink = subitems2[0].find('a')['href']

					item['c4SellingType'] = selling_type
					item['c4SellingDate'] = selling_date
					item['c4SellingStatus'] = selling_check
					item['c4SellingStatusCaption'] = selling_checkcaption
					item['c4SellingDetailLink'] = selling_detail_link
					item['c4SellingAreaType'] = selling_areatype
					item['c4SellingSupplyArea'] = selling_supplyarea
					item['c4SellingNetArea'] = selling_netarea
					item['c4SellingComplex'] = selling_complex
					item['c4SellingFloor'] = selling_floor
					item['c4SellingTotalFloor'] = selling_totalfloor
					item['c4SellingPrice'] = selling_price
					item['c4SellingAgentName'] = agent_name
					item['c4SellingAgentTel'] = agent_tel
					item['c4SellingAgentCode'] = agent_code
					item['c4SellingAgentComment'] = agent_comment
					item['c4SellingSource'] = selling_source
					item['c4SellingSourceLink'] = selling_sourcelink
					item['c4SellingClass'] = maemul_name

				sublist.append(item)

	def c4_list_parsing_callback(self, data):
		soup_sub = BeautifulSoup(data.get_html(), "html.parser")
		check_maemul_sub = soup_sub.find('table', {'class': 'sale_list _tb_site_img NE=a:cpm'})
		agent_maemul_sub = soup_sub.find('table', {'class': 'sale_list NE=a:prm'})
		self.__get_c4list_parsing_core(check_maemul_sub, data.get_sub_list(), '확인 매물')
		self.__get_c4list_parsing_core(agent_maemul_sub, data.get_sub_list(), '공인중개사협회매물')
