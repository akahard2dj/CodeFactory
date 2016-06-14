import pymysql

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
for cc in c4:
	c4_address_num.append(cc[-2].split(" ")[-1])
	print(cc[11], cc[-2].split(" ")[-1])
	
print(price_hist[0])
for price in price_hist:
	add_num = price[-3]
	filtered = [x for x in c4_address_num if add_num in x and len(add_num) is len(x)]
	
	if len(filtered) == 1:
		index = c4_address_num.index(add_num)
		query = "update pricehistory set c4code='%s' where id='%s'" % (c4[index][10], price[0])
		cur.execute(query)
		print(c4[index][10],c4[index][11],price[0])
conn.commit()
		
