from AccelInterface import AccelInterface as Accel
import time
import csv

Ac = Accel()
secs = 0;
# with open('test9.csv', mode='w') as dataFile:
dataFile = open('test10.csv', mode='w')
dataWriter = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) 
while(secs < 10):
	#print(Ac.getXRotation())
	#print(Ac.getYRotation())
	dataWriter.writerow([Ac.getAccelXScaled(),Ac.getAccelYScaled(),Ac.getAccelZScaled()])
	print("x",Ac.getAccelXScaled())
	print("y",Ac.getAccelYScaled())
	print("z",Ac.getAccelZScaled())
	print(secs)
	secs += 1
	time.sleep(1)
