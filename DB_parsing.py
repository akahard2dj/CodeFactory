import json
import DW_parsing
import DW_stat
import IO

kuName = ['kangnam', 'kangdong', 'kangbuk', 'kangseo','kwanak','kwangjin','kuro','kuemchoen','noone','dobong',
            'dongdaemun','dongjak','mapo','seodaemun','seocho','seongdong','seongbuk','songpa','yangcheon',
            'youngdeungpo','yongsan','eunpyong','jongro','jung','jungrang']

dongName = []
dongName.append( ['kaepo','nonhyun','daechi','dogok','samsung','saegok','suseo','shinsa','apgujeong','yeoksam','yulhyun','ilwon','jagok','cheongdam'])
dongName.append( ['kangil','kodeok','gil','dunchon','myungil','sangil','seongnae','amsa','cheonho'])
dongName.append( ['miah','beon','suyou','ui'])
dongName.append( ['kayang','kaehwa','gonghang','gwhahae','naebalsan','deungchon','magok','banghwa','yeomchang','ogok','osoe','oebalsan','hwagok'])
dongName.append( ['namhyun','bongchoen','shinlim'])
dongName.append( ['gwhangjang','kuui','kunja','nueong','jayang','junggok','hwayang'])
dongName.append( ['garibong','gaebong','gocheok','kuro','gung','shindorim','oryu','onsu','choenwang','hang'])
dongName.append( ['gasan','doksan','shiheung'])
dongName.append( ['gongreung','sanggae','wolgae','junggae','hagae'])
dongName.append( ['dobong','banghak','ssangmun','chang'])
dongName.append( ['dapshipri','shinseol','youngdu','yimun','jangan','jeonnong','jaeki','cheonryangri','hoeki','huikyung'])
dongName.append( ['noryangjin','daebang','dongjak','bon','sadang','sangdo1','snagdo','shindaebang','hukseok'])
dongName.append( ['gongdeok','kusu','nogosan','dangin','daeheung','dohwa','dongkyo','mapo','mangwon','sangsu','sangam','seokyo','seongsan','shingongdeok','shinsu','shinjeong','ahyun','yeonnam','yeomri','yongkang','jung','changcheon','tojeong','hajung','hapjeong','hyunseok'])
dongName.append( ['namgajwha','naengcheon','daeshin','daehyun','mikeun','bongwon','bukkwaja','bukahyun','shinchon','yeonhui','youngcheon','okcheon','changcheon','cheonyoun','chungjeongro2ga','chungjeongro3ga','hap','hyunjeo','honguen','hongjae'])
dongName.append( ['naegok','banpo','bangbae','seocho','shinwon','yangjae','yeomgok','umyeon','wonji','jamwon'])
dongName.append( ['keumho1ga','keumho2ga','keumho3ga','keumho4ga','doseon','majang','sakuen','sangwangshipri','seongsu1ga','seongsu2ga','songjeong','oksoo','youngdap','eungbon','hawangshipri','haengdand','hongik'])
dongName.append( ['kileum','donam','dongseon1ga','dongseon2ga','dongseon3ga','dongseon4ga','dongseon5ga','dongsomun1ga','dongsomun2ga','dongsomun3ga','dongsomun4ga','dongsomun5ga','dongsomun6ga','dongsomun7ga','bomun1ga','bomun2ga','bomun3ga','bomun4ga','bomun5ga','bomun6ga','bomun7ga','samseon1ga','samseon2ga','samseon3ga','samseon4ga','samseon5ga','sangwolgok','seokkwan','seongbuk','seongbuk1ga','anam1ga','anam2ga','anam3ga','anam4ga','anam5ga','jangui','jeongreung','jongam','hawolgok'])
dongName.append( ['garak','geoyoe','macheon','munjeong','bangyi','samjeon','seokchon','songpa','shincheon','okeum','jamshil','jangji','pungnap'])
dongName.append( ['mok','shinwol','shinjeong'])
dongName.append( ['dangsan','dangsan1ga','dangsan2ga','dangsan3ga','dangsan4ga','dangsan5ga','dangsan6ga','daerim','dorim','munrae1ga','munrae2ga','munrae3ga','munrae4ga','munrae5ga','munrae6ga','shingil','yangpyoeng','yangpyoeng1ga','yangpyoeng2ga','yangpyoeng3ga','yangpyoeng4ga','yangpyoeng5ga','yangpyoeng6ga','yanghwa','yeouido','youngdeungpo','youngdeungpo1ga','youngdeungpo2ga','youngdeungpo3ga','youngdeungpo4ga','youngdeungpo5ga','youngdeungpo6ga','youngdeungpo7ga','youngdeungpo8ga'])
dongName.append( ['kalwol','namyoung','dowon','dongbinggo','dongja','munbae','bokwhang','sancheon','seoke','seobinggo','shinke','shinchang','yongmun','yongsan1ga','yongsan2ga','yongsan3ga','yongsan4ga','yongsan5ga','yongsan6ga','wonhyoro1ga','wonhyoro2ga','wonhyoro3ga','wonhyoro4ga','yichon','yitaewon','juseong','cheongam','cheongpa1ga','cheongpa2ga','cheongpa3ga','hangangro1ga','hangangro2ga','hangangro3ga','hannam','hyochang','huam'])
dongName.append( ['kalhyun','kusan','nokbeon','daejo','bulkwang','susaek','shinsa','yeokchon','ungam','jungsan','jinkwan'])
dongName.append( ['kahui','kyunji','kyungun','ke','gongpyoeng','kwansu','kwancheol','kwanhun','kyonam','kyobuk','kuki','kungjeong','kwonnong','nakwon','naesoo','naeja','nusang','nuha','dangju','doryum','donui','dongsung','myungrun1ga','myungrun2ga','myungrun3ga','myungrun4ga','myo','muak','bongik','buam','sagan','sajik','samchoeng','seorin','saejong','sokyuk','songwol','songhyun','susong','sungin','shinkyo','shinmuro1ga','shinmuro2ga','shinyoung','ankuk','yeonkeon','yeonji','yeji','okin','waryong','unni','wonnam','wonseo','yihwa','ikseon','insa','inui','jangsa','jae','jeokseon','jongro1ga','jongro2ga','jongro3ga','jongro4ga','jongro5ga','jongro6ga','junghak','changseong','changshin','cheongun','cheongjin','chaebu','chungshin','tongui','tongin','palpan','pyeong','pyeongchang','pilun','haengchon','hyehwa','hongji','hongpa','hwa','hyoja','hyojae','hunjeong'])
dongName.append( ['kwanghui1ga','kwanghui2ga','namdaemunro1ga','namdaemunro2ga','namdaemunro3ga','namdaemunro4ga','namdaemunro5ga','namsan1ga','namsan2ga','namsan3ga','namchang','namhak','da','manri1ga','manri2ga','myung1ga','myung2ga','mukyo','muhak','mukjeong','bangsan','bongrae1ga','bongrae2ga','bukchang','sanrim','samkak','seosomun','sokong','supyo','suha','sunhwa','shindang','ssangrim','yekwan','yejang','ojang','eulji1ga','eulji2ga','eulji3ga','eulji4ga','eulji5ga','eulji6ga','eulji7ga','uiju1ga','uiju2ga','inhyung1ga','inhyung2ga','yipjeong','jangkyo','jangchung1ga','jangchung2ga','jeo1ga','jeo2ga','jeong','jukyo','juja','jungrim','cho','chungmuro1ga','chungmuro2ga','chungmuro3ga','chungmuro4ga','chungmuro5ga','chungjeongro1ga','taepyungro1ga','taepyungro2ga','pil1ga','pil2ga','pil3ga','hwanghak','hoehyun1ga','hoehyun2ga','hoehyun3ga','huengin'])
dongName.append( ['mangu','myeonmok','muk','sangbong','shinnae','junghwa'])

class1_code = ['1100000000','4100000000','2800000000','2600000000','3000000000','2700000000','3100000000','3600000000','2900000000','4200000000','4300000000','4400000000','4700000000','4800000000','4500000000','4600000000','5000000000']
class1_nameEN = ['seoul-si','gyeonggi-do','incheon-si','busan-si','daejeon-si','daegu-si','ulsan-si','saejong-si','gwangju-si','gangwon-do','chungcheongbuk-do','chungcheongnam-do','gyeongsangbuk-do','gyunsangnam-do','jeonrabuk-do','jeongranam-do','jaeju-do']
type_code = ['A01', 'A02', 'B01', 'C03', 'E03', 'C01', 'D02', 'D01', 'E02', 'F01', 'D03']
type_name = ['apt','oft','bun','hos','lnd','onr','shp','ofc','fct','rdv','etc']

#Loading from web site
#c2List = DW_parsing.getc2List(class1_code)
#IO.writeJSON('c2List.json',c2List)

#Loading from json file
#c2List = IO.staticLoadJSON('2015-12-16-c2List.json')
c2List = IO.loadJSON('c2List.json')
#for sub in c2List:
#    print sub['c1Code'], sub['c1NameKR'], sub['c2Code'], sub['c2NameKR']

# indexing example
#output_dict = [x for x in c2List if x['c1Code'] == '1100000000']

#Loading from web site
#for tCode in type_code:
#tCode = 'A01'
#c3List = DW_parsing.getc3List(c2List, tCode)
#fname = 'c3List_' + tCode + '.json'
#IO.writeJSON(fname, c3List)

#Loading from json file
#for tCode in type_code:
#tCode = 'A01'
#fname = 'c3List_' + tCode + '.json'
#c3List = IO.loadJSON(fname)

c3List = IO.staticLoadJSON('2015-12-16-c3List_A01.json')
#output_dict = [x for x in c3List if x['c1Code'] == '1100000000']
#for sub in output_dict:
#    print sub['c1Code'], sub['c1NameKR'], sub['c2Code'], sub['c2NameKR'], sub['c3Code'], sub['c3NameKR'], sub['count']

#DW_stat.drill(c2List, c3List)

#c4List = DW_parsing.getc4List(c3List, 'A01')
#IO.writeJSON('c4List_A01.json', c4List)
c4List = IO.staticLoadJSON('2015-12-16-c4List_A01.json')


#c4List = IO.loadJSON('c4List_A01.json')
#for sub in c4List:
#    print sub['c1Code'], sub['c1NameKR'], sub['c2Code'], sub['c2NameKR'], sub['c3Code'], sub['c3NameKR'],sub['c4Code'], sub['c4NameKR']

#c5List=DW_parsing.getc5List(c4List, 'A01')
#IO.writeJSON('c5List_A01.json', c5List)

c5List = IO.staticLoadJSON('2015-12-16-c5List_A01.json')
#for sub in c5List:
#    print sub['c1Code'], sub['c1NameKR'], sub['c2Code'], sub['c2NameKR'], sub['c3Code'], sub['c3NameKR'],sub['c4Code'], sub['c4NameKR'], sub['c5AptTradeType'], sub['c5AptRegisterDate'], sub['c5AptTradeFlag'], sub['c5AptPrice']

#realList = (c2List, c3List, c4List, c5List)
#DW_stat.drill2(realList)
#DW_stat.drill2(realList)


#for sub in c4List:
#    print sub['c1Code'], sub['c1NameKR'], sub['c2Code'], sub['c2NameKR'], sub['c3Code'], sub['c3NameKR'],sub['c4Code'], sub['c4NameKR']

#output_dict = [x for x in c3List if x['c1Code'] == '1100000000']

#for sub in output_dict:
#    print sub['c1Code'], sub['c1NameKR'], sub['c2Code'], sub['c2NameKR'], sub['c3Code'], sub['c3NameKR']

#print len(output_dict)

realList = (c2List, c3List, c4List, c5List)
DW_stat.drill3(realList)
