#-*- coding:cp949 -*-
def drill(realList):
    c2List, c3List, c4List, c5List = realList

    c2Code = '1100000000' # seoul
    output_dict = [x for x in c2List if x['c1Code'] == c2Code]
    for c2Sub in output_dict:
        code = c2Sub['c2Code']
        f1_dict = [x for x in c3List if x['c2Code'] == code]
        nItem = 0
        for f1Sub in f1_dict:
            nItem = nItem + int(f1Sub['count'])

        print c2Sub['c2NameKR'], nItem


def drill2(realList):
    c2List, c3List, c4List, c5List = realList

    output_dict = [x for x in c5List if x['c4Code'] == '8928']

    trade_apt = [x for x in output_dict if x['c5AptTradeType'] == u'매매']
    lease_apt = [x for x in output_dict if x['c5AptTradeType'] == u'전세']
    rent_apt = [x for x in output_dict if x['c5AptTradeType'] == u'월세']

    print len(trade_apt), len(lease_apt), len(rent_apt), c4List[0]['c4SaleTotal']
