import pymysql
import requests
import requests.adapters
import json
import os

def get_addr2latlng(query, client_id, client_secret):
    url = 'https://openapi.naver.com/v1/map/geocode?clientId=%s&query=%s' % (client_id, query)
    #url = 'https://openapi.naver.com/v1/map/geocode?clientId=VpXsKYJAWAdIttaJ7bD9&query=' + query

    params = {'clientId': client_id, 'query': query}
    headers = {
        'Host': 'openapi.naver.com',
        'User-Agent': 'curl/7.43.0',
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret,
    }
    requests.adapters.DEFAULT_RETRIES = 5
    r = requests.get(url, data=json.dumps(params), headers=headers, timeout=5)
    return json.loads(r.text)

class MySQLQeury:
    def __init__(self, dbname, passwd, dbuser, dbloc):
        self.__passwd = passwd
        self.__dbname = dbname
        self.__dbuser = dbuser
        self.__dbloc = dbloc
        self.conn = pymysql.connect(host=self.__dbloc, port=3306, user=self.__dbuser, passwd=self.__passwd,
                                    db=self.__dbname, use_unicode=True, charset='utf8')
        self.cur = self.conn.cursor()

        self.c1_data = list()
        self.c2_data = list()
        self.c3_data = list()
        self.c4_data = list()

    def __del__(self):
        self.conn.close()

    @staticmethod
    def search_in_dictlist(data, key, value):
        idx = next(index for (index, d) in enumerate(data) if d[key] == value)
        return idx

    def set_c1data(self):
        query = "select * from c1"
        self.cur.execute(query)
        for sub in self.cur:
            c1_index = sub[0]
            c1_code = sub[2]
            c1_name = sub[5]
            sub_dict = {'index': c1_index, 'code': c1_code, 'name': c1_name}
            self.c1_data.append(sub_dict)

    def get_c1data(self):
        self.set_c1data()
        return self.c1_data

    def set_c2data(self):
        if not self.c1_data:
            self.set_c1data()

        query = "select * from c2"
        self.cur.execute(query)
        for idx, sub in enumerate(self.cur):
            c1_index = sub[0]
            c2_index = sub[1]
            c2_code = sub[2]
            c2_name = sub[3]
            c1_key = self.search_in_dictlist(self.c1_data, 'index', c1_index)
            sub_dict = {'index': c2_index, 'code': c2_code, 'name': c2_name, 'c1key': c1_key}
            self.c2_data.append(sub_dict)

    def get_c2data(self):
        self.set_c2data()
        return self.c2_data

    def is_table(self, table_name):
        len_check = 0
        result = False
        self.cur.execute("show tables like '%s'" % table_name)
        for sub in self.cur:
            len_check = len(sub)

        if len_check is not 0:
            result = True

        return result


    def rename_table(self, ori_table, rename_table):
        if self.is_table(ori_table) is not True:
            print('%s does not exist. Please check an original table.' % ori_table)
            return False
        else:
            if self.is_table(rename_table) is True:
                print('%s exists. Please check a renamed table.' % rename_table)
                return False
            else:
                self.cur.execute('rename table %s to %s' % (ori_table, rename_table))
                return True

    def copy_table(self, ori_table, target_table):
        if self.is_table(ori_table) is not True:
            print('%s does not exist. Please check an original table.' % ori_table)
            return False
        else:
            if self.is_table(target_table) is True:
                print('%s exists. Please check a renamed table.' % target_table)
                return False
            else:
                self.cur.execute('create table %s select * from %s' % (target_table, ori_table))
                return True

    def make_table(self, sql_name):
        result = True
        f = open(os.path.join('mysql', 'c4list.sql'), 'r')
        lines = f.readlines()
        query = str()
        for line in lines:
            query += line
        try:
            self.cur.execute(query)

        except:
            print('%s is already exists. Please check the table.' % sql_name)
            result = False

        return result

    def delete_table(self, table):
        if self.is_table(table) is True:
            print('%s does not exist. Please check an original table.' % table)
            return False
        else:
            self.cur.execute('drop table %s' % table)
            return True


mysql = MySQLQeury('test_estatedb', 'boradowon$', 'root', 'localhost')
#mysql.copy_table('c1', 'c1_copy2')
print(mysql.delete_table('c4list'))
#c1_data = mysql.get_c1data()
#c2_data = mysql.get_c2data()
#print(c1_data[c2_data[0]['c1key']]['name'], c2_data[0]['name'])

