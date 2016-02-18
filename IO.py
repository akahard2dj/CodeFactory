import json
import time
import os

def writeJSON(fname, listItem):
    timestampStr = time.strftime("%Y-%m-%d-", time.localtime())
    fnameTimestamp = timestampStr + fname
    j = json.dumps(listItem)
    with open(fnameTimestamp, 'w') as f:
        f.write(j)
    f.close()


def write_c4list_json(c4code_value, list_items):
    dir_name = time.strftime("%Y-%m-%d", time.localtime())

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    fname = dir_name + '\\' + str(c4code_value) + '_c4List.json'
    j = json.dumps(list_items)
    with open(fname, 'w') as f:
        f.write(j)
    f.close()

def staticWriteJSON(fname, listItem):
    j = json.dumps(listItem)
    with open(fname, 'w') as f:
        f.write(j)
    f.close()

def loadJSON(fname):
    timestampStr = time.strftime("%Y-%m-%d-", time.localtime())
    fnameTimestamp = timestampStr + fname

    with open(fnameTimestamp, 'r') as f:
        listItem = json.load(f)

    return listItem

def staticLoadJSON(fname):
    with open(fname, 'r') as f:
        listItem = json.load(f)

    return listItem

def timestamp_json(fname):
    timestampStr = time.strftime("%Y-%m-%d-", time.localtime())
    fnameTimestamp = timestampStr + fname

    return fnameTimestamp
