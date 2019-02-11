from AccelInterface import AccelInterface as Accel
import time

Ac = Accel()
secs = 0;
while(True):
	#print(Ac.getXRotation())
	#print(Ac.getYRotation())
	print("x",Ac.getAccelXScaled())
	print("y",Ac.getAccelYScaled())
	print("z",Ac.getAccelZScaled())
	print(secs)
	secs += 1
	time.sleep(1)
