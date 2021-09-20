import sensor_rutger
import serial
import time
import pickle
serials = []
data = []
out = {}
for i in range(0,33):
	try:
		global b
		b = serial.Serial("/dev/ttyUSB" + str(i),115200,timeout=0.01)
		b.close()
	except:
		pass
	else:
		print("found device at /dev/ttyUSB" + str(i))
		serials.append("/dev/ttyUSB" + str(i))
for i in range(0,33):
	try:
		global a
		a = serial.Serial("/dev/ttyACM" + str(i),115200,timeout=0.01)
		a.close()
	except:
		pass
	else:
		print("found device at /dev/ttyACM" + str(i))
		serials.append("/dev/ttyACM" + str(i))
def handle_arduino(ser):
	ser.write(b"\xff")
	global data
	global out
	data = []
	data += ser.readline().decode(errors='ignore').strip().split(";")
	out = {}
	print(data)
	if len(data) < 12 or len(data) > 12:
		print("did not get enough data",data)
		return handle_arduino(ser)
	for i in range(0,len(data),2):
		print(data[i],data[i+1])
		out.update({data[i]:data[i+1]})
	return out,data
sensor_rutger.setup(serials[0],serials[1],serials[2],serials[3])
sensor_rutger.set_ard_handle(handle_arduino)
if __name__ == '__main__':
	sensor_rutger.loop()
