import json
import time

def writeJSON(fname, list):
    timestampStr = time.strftime("%Y-%m-%d-", time.localtime())
    fnameTimestamp = timestampStr + fname
    j = json.dumps(list)
    with open(fnameTimestamp,'w') as f:
        f.write(j)
    f.close()

def loadJSON(fname):
    with open(fname, 'r') as f:
        list = json.load(f)

    return list
