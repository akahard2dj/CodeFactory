def drill(c2List, c3List):
    c2Code = '1100000000'
    output_dict = [x for x in c2List if x['c1Code'] == c2Code]
    for c2Sub in output_dict:
        code = c2Sub['c2Code']
        f1_dict = [x for x in c3List if x['c2Code'] == code]
        sum = 0
        for f1Sub in f1_dict:
            sum = sum + int(f1Sub['count'])

        print c2Sub['c2NameKR'], sum
