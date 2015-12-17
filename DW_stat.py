#-*- coding:cp949 -*-
import IO
import csv
import bs4

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


def extTradeCountList(realList):
    c2List, c3List, c4List, c5List = realList

    tradeList = []
    for aa in c4List:
        sub = {}
        output_dict = [x for x in c5List if x['c4Code'] == aa['c4Code']]

        trade_apt = [x for x in output_dict if (x['c5AptTradeType'] == u'매매' and x['c5AptTradeFlag'] == 'mark4')]
        lease_apt = [x for x in output_dict if (x['c5AptTradeType'] == u'전세' and x['c5AptTradeFlag'] == 'mark4')]
        rent_apt = [x for x in output_dict if (x['c5AptTradeType'] == u'월세' and x['c5AptTradeFlag'] == 'mark4')]

        sub['c1Code'] = aa['c1Code']
        sub['c2Code'] = aa['c2Code']
        sub['c3Code'] = aa['c3Code']
        sub['c4Code'] = aa['c4Code']

        sub['nTrade'] = len(trade_apt)
        sub['nLease'] = len(lease_apt)
        sub['nRent'] = len(rent_apt)
        tradeList.append(sub)
        print len(output_dict), aa['c1Code'],aa['c2Code'],aa['c3NameKR'], aa['c4NameKR'], len(trade_apt), len(lease_apt), len(rent_apt)

    IO.staticWriteJSON('c5Stat.json', tradeList)

def saveMap(csvfname, svgfname):
    reader = csv.reader(open(csvfname, 'r'), delimiter=',')

    svg = open('Seoul_districts.svg', 'r').read()

    item_count = {}
    count_only = []
    min_value = 100
    max_value = 0
    past_header = True
    for row in reader:
        if not past_header:
            past_header = True
            continue

        try:
            unique = row[0]
            count = float(row[1].strip())
            item_count[unique] = count
            print unique, count
            count_only.append(count)
        except:
            pass

    soup = bs4.BeautifulSoup(svg, "html.parser")

    paths = soup.findAll('path')
    colors = ["#CCE0FF", "#99C2FF", "#66A3FF", "#3385FF", "#0066FF", "#0052CC", "#003D99"]
    g_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

    count_span = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    ratio = (max(count_only) - min(count_only)) / float(len(count_span)-2)
    count_span = [x*ratio for x in count_span]
    print count_span
    for p in paths:
        try:
            count = item_count[p['id']]
            print p['id'], item_count[p['id']]
        except:
            continue

        if count > count_span[10]:
            color_class = 5
        elif count > count_span[7]:
            color_class = 4
        elif count > count_span[5]:
            color_class = 3
        elif count > count_span[3]:
            color_class = 2
        elif count > count_span[1]:
            color_class = 1
        else:
            color_class = 0

        color = colors[color_class]
        p['style'] = g_style + color


    f = open(svgfname, 'w')
    f.write(soup.prettify())
    f.close()

def drill3(realList):
    c2List, c3List, c4List, c5List = realList
    #extTradeCountList(realList)
    statList = IO.staticLoadJSON('c5Stat.json')


    output_dict = [x for x in c2List if x['c1Code'] == '1100000000']

    nTrade = []
    nLease = []
    nRent = []
    for aa in output_dict:
        sub = [x for x in statList if x['c2Code'] == aa['c2Code']]
        subSumTrade = []
        subSumLease = []
        subSumRent = []
        for bb in sub:
            subSumTrade.append(bb['nTrade'])
            subSumLease.append(bb['nLease'])
            subSumRent.append(bb['nRent'])
        nTrade.append(sum(subSumTrade))
        nLease.append(sum(subSumLease))
        nRent.append(sum(subSumRent))

    guName = ['Gangnam', 'Gangdong', 'Gangbuk', 'Gangseo','Gwanak','Gwangjin','Guro','Geumcheon','Nowon','Dobong',
            'Dongdaemun','Dongjak','Mapo','Seodaemun','Seocho','Seongdong','Seongbuk','Songpa','Yangcheon',
            'Yeongdeungpo','Yongsan','Eunpyeong','Jongno','Jung','Jungnang']

    tradeList = []
    leaseList = []
    rentList = []
    csvTrade = open('seoul_trade.csv','wb')
    csvLease = open('seoul_lease.csv','wb')
    csvRent = open('seoul_rent.csv','wb')
    csvLeaseRatio = open('seoul_leaseRatio.csv','wb')
    wriTrade = csv.writer(csvTrade)
    wriLease = csv.writer(csvLease)
    wriLeaseRatio = csv.writer(csvLeaseRatio)
    wriRent = csv.writer(csvRent)
    for i in range(len(nTrade)):
        trade = (guName[i]+'-gu', nTrade[i])
        print trade
        lease = (guName[i]+'-gu', nLease[i])
        rent = (guName[i]+'-gu', nRent[i])
        leaseRatio = (guName[i]+'-gu', float(nLease[i]) / float(nTrade[i]+nLease[i]+nRent[i]))
        wriTrade.writerow(trade)
        wriLease.writerow(lease)
        wriRent.writerow(rent)
        wriLeaseRatio.writerow(leaseRatio)

    csvTrade.close()
    csvLease.close()
    csvRent.close()
    csvLeaseRatio.close()

    saveMap('seoul_trade.csv','seoul_trade.svg')
    saveMap('seoul_lease.csv','seoul_lease.svg')
    saveMap('seoul_rent.csv','seoul_rent.svg')
    saveMap('seoul_leaseRatio.csv','seoul_leaseRatio.svg')
