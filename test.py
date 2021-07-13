
def show_menu_table():
    prompt = """
    1. 입력
    2. 출력
    3. 검색
    4. 종료
    """
    print(prompt)


def inputData(records):
    product_name = input('제품명 : ')
    quantity = int(input('수량 : '))
    product_date = input('생산일(예: 1990-01-01) : ')
    item = dict()
    item['product_name'] = product_name
    item['quantity'] = quantity
    item['product_date'] = product_date
    records.append(item)


def outputData(records):
    print('-----------------------------------------')
    print('  제품명         수량         생산일')
    print('-----------------------------------------')
    for record in records:
        print('  {}         {}           {}'.format(
            record['product_name'],
            record['quantity'],
            record['product_date']
        ))


def searchData(records, search_str):
    search_index = list()
    for idx, record in enumerate(records):
        if record['product_name'] == search_str:
            search_index.append(idx)

    print('-----------------------------------------')
    print('  제품명         수량         생산일')
    print('-----------------------------------------')
    for idx in search_index:
        print('  {}         {}           {}'.format(
            records[idx]['product_name'],
            records[idx]['quantity'],
            records[idx]['product_date']
        ))


if __name__ == '__main__':
    records = list()

    while True:
        show_menu_table()
        menu_index = int(input('메뉴를 선택하세요: '))

        if menu_index == 1:
            while True:
                inputData(records)
                flag = input('계속 입력 하시겠습니까(y/n)? ')
                if flag == 'n':
                    break

        if menu_index == 2:
            outputData(records)

        if menu_index == 3:
            search_str = input('검색할 제품명을 입력 하세요.: ')
            searchData(records, search_str)

        if menu_index == 4:
            exit(0)
