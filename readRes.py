import numpy as np
from collections import namedtuple

def countLines(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
		return i+1
		
def readLines(fname, arrayLines):
	fp = open(fname, "r")
	for line in fp:
		arrayLines.append(line)
		
	fp.close()	

#fname = "C:\\Users\\user\\Desktop\\SPL 141217\\141217A\\1.res"

def readRes(fname):
	numberOfLines = countLines(fname)
	array = []
	targetIdx = []
	results = []
	readLines(fname, array)

	#Results=MTF-Field; Type=Sagittal; EFL=6.38178[mm]; Freq=0[lp/mm]; Defocus=0.000[mm]; Azimuth=0.000[deg]
	ResResults = namedtuple("ResResults", ["Type", "EFL", "Freq"])

	for i in range(0, numberOfLines-1):
		findResult = array[i].find('Results')
		if findResult != -1:
			targetIdx.append(i)
			
	#for i in range(0, len(targetIdx)):
	for i in range(1,len(targetIdx)):
		subSplit = array[targetIdx[i]].split(";")
		nReminders = len(subSplit)
		values = []
		
		# Type
		subString = subSplit[1].strip()
		splitString = subString.split("=")
		values.append(splitString[1])
		
		# EFL
		subString = subSplit[2].strip()
		splitString = subString.split("=")
		values.append(splitString[1])
		
		# Freq
		subString = subSplit[3].strip()
		splitString = subString.split("=")
		values.append(splitString[1])
		
		# Sensor Angle
		subSplit = array[targetIdx[i]+1].split(" ")
		nSkipSensorAngle = 4
		numberOfPositions = len(subSplit)-nSkipSensorAngle-1
		sensorAngle = []
		
		for j in range(0, numberOfPositions):
			sensorAngle.append(float(subSplit[j+nSkipSensorAngle]))
		values.append(sensorAngle)
		
		# Sensor Pos
		subSplit = array[targetIdx[i]+2].split(" ")
		nSkipSensorPos = 1
		numberOfPositions = len(subSplit)-nSkipSensorPos-2
		sensorPos = []
		
		for j in range(0, numberOfPositions):
			sensorPos.append(float(subSplit[j+nSkipSensorPos]))
		values.append(sensorPos)
			
		# MTF Values
		subSplit = array[targetIdx[i]+3].split(" ")
		nSkipValuesMTF = 1
		numberOfValuesMTF = len(subSplit)-nSkipValuesMTF-1
		valuesMTF = []

		for j in range(0, numberOfValuesMTF):
			valuesMTF.append(float(subSplit[j+nSkipValuesMTF]))
		values.append(valuesMTF)

		results.append(values)
	return results
	
from pylab import *

if __name__ == '__main__':
	fname = "C:\\Users\\user\\Desktop\\SPL 141217\\141217A\\1.res"
	results = readRes(fname)
	idx = 7
	print results[idx]
	
	for i in range(0,7):
		plot(results[idx+i][4],results[idx+i][5])		

	show()
