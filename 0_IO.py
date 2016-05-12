from json import JSONEncoder
import json
import datatype

class MyEncode(JSONEncoder):
    def default(self, o):
        return o.__dict__

def write_json(filename, lists):
    j = json.dumps(MyEncode().encode(lists))
    with open(filename, 'w') as f:
        f.write(j)

    f.close()

def c1_load_json(filename):
    with open(filename, 'r') as f:
        j = json.load(f)

    f.close()
    lists = json.loads(j)

    c1lists = list()
    for idx in range(len(lists)):
        c1 = datatype.c1code()
        for key, value in json.loads(j)[idx].items():
            setattr(c1, key, value)
            #print(key, value)

        c1lists.append(c1)

    return c1lists
