import json
import time
import codecs

def dumpPageSource(fname, str):
    file = codecs.open(fname, "w", "utf-8")
    file.write(str)
    file.close()

def loadPageSource(fname):
    file = codecs.open(fname, "r", "utf-8")
    str = file.read()

    return str

def writeJSON(fname, listItem):
    timestampStr = time.strftime("%Y-%m-%d-", time.localtime())
    fnameTimestamp = timestampStr + fname
    j = json.dumps(listItem)
    with open(fnameTimestamp,'w') as f:
        f.write(j)
    f.close()

def staticWriteJSON(fname, listItem):
    j = json.dumps(listItem)
    with open(fname,'w') as f:
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
