import pymysql
import difflib
import operator
import re

def delete_substring(string):
	return re.sub('\([^)]*\)', '', string)

conn = pymysql.connect(user='root', passwd='', db='test_estate_db', use_unicode=True, charset='utf8')
cur = conn.cursor()

cur.execute("select * from c4 where c3namekr='개포동'")
c4 = list()
for row in cur:
	c4.append(row)
	
cur.execute("select * from pricehistory where c3namekr='개포동'")
price_hist = list()
for row in cur:
	price_hist.append(row)

c4_address_num = list()
c4_address_name = list()
c4_address_ext_name = list()
for cc in c4:
	c4_address_num.append(cc[-2].split(" ")[-1])
	c4_address_name.append(cc[11])
	c4_address_ext_name.append(delete_substring(cc[11]))
	print(cc[11], cc[-2].split(" ")[-1])
	
print(price_hist[0])
for price in price_hist:
	add_num = price[-3]
	filtered = [x for x in c4_address_num if add_num in x and len(add_num) is len(x)]
	#print(price[4],difflib.get_close_matches(price[4], c4_address_name))
	if len(filtered) == 1:
		index = c4_address_num.index(add_num)
		query = "update pricehistory set c4code='%s' where id='%s'" % (c4[index][10], price[0])
		cur.execute(query)
		#print(c4[index][10],c4[index][11],price[0])
	else:
		#print(price[4],difflib.get_close_matches( price[4], c4_address_ext_name))
		match_result = difflib.get_close_matches( price[4], c4_address_name)
		#print(price[4], match_result)
		if len(match_result) == 1:
			index = c4_address_name.index(match_result[0])
			query = "update pricehistory set c4code='%s' where id='%s'" % (c4[index][10], price[0])
			cur.execute(query)
			
		if len(match_result) == 0:
			ratio_list = list()
			for c4_sub in c4_address_ext_name:
				c4_1 = c4_sub.replace("단지","")
				price_4_1 = price[4].replace("단지","")
				ratio_list.append(difflib.SequenceMatcher(None, c4_1, delete_substring(price_4_1)).ratio())
			
			max_index, max_value = max(enumerate(ratio_list), key=operator.itemgetter(1))
			if max_value >= 0.6:
				print(price[4], c4_address_name[max_index], max_value)
				query = "update pricehistory set c4code='%s' where id='%s'" % (c4[max_index][10], price[0])
				cur.execute(query)
		
		
conn.commit()
		
