from bs4 import BeautifulSoup
from datatype import C1Code, C2Code, C3Code, C4Code
from request_manager import RequestManager
import json_utils
import url_info
from timestamp import Timestamp

from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

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
			self.ts.start('request_c1')
			self.rm.request('c1', url_info.C1_URL, self.callback)
			json_utils.write_class("c1CodeClass.json", self.code)
			self.ts.stop()
			self.ts.show_log()
		
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
			
		url_list = comm.scatter(chunks, root=self.root_rank)
		
		for idx, url in enumerate(url_list):
			self.rm.request('c2', url, self.callback, idx)
		
		gather_code = comm.gather(self.code, root=self.root_rank)
		if self.rank == self.root_rank:
			write_code = list()
			for list_code in gather_code:
				for code in list_code:
					write_code.append(code)
			json_utils.write_class('c2CodeClass.json', write_code)
		
		if self.rank == self.root_rank:
			self.ts.stop()
			self.ts.show_log()
			
	def callback(self, data):
		html = data.get_html()
		index = data.get_index()
		for sub in self.parse(html, index):
			builder = C2Code.Builder()
			idx = index * self.size + self.rank
			builder.set_c1code(self.__c1Code[idx]) \
				.set_c2code(sub['c2Code']) \
				.set_c2namekr(sub['c2NameKR'])
			self.code.append(builder.build())		
		
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
			
		url_list = comm.scatter(chunks, root=self.root_rank)
		
		for idx, url in enumerate(url_list):
			self.rm.request('c3', url, self.callback, idx)
			
		gather_code = comm.gather(self.code, root=self.root_rank)
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
			
		url_list = comm.scatter(chunks, root=self.root_rank)
		
		for idx, url in enumerate(url_list):
			self.rm.request('c4', url, self.callback, idx)
			
		while len(self.failed_url_list) != 0:
			failed_url = self.failed_url_list.pop()
			self.rm.request('c4', failed_url, self.callback, 0)
			
		gather_code = comm.gather(self.code, root=self.root_rank)
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
