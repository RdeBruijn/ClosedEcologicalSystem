import serial
import time
import pickle
import base64
import zlib
sen1 = 0
sen2 = 0
sen3 = 0
sen4 = 0
def setup(port1,port2,port3,port4):
	global sen1
	global sen2
	global sen3
	global sen4
	sen1 = serial.Serial(port1,timeout=1)
	sen2 = serial.Serial(port2,timeout=1)
	sen3 = serial.Serial(port3,timeout=1)
	sen4 = serial.Serial(port4,timeout=1)
command_read_filmware_version = b"\x11\x01\x1E\xD0\x0D\x0A" # read filmware version
command_read_co2 = b"\x11\x01\x01\xED\x0D\x0A" # read co2
command_read_serial_number = b"\x11\x01\x1F\xCF\x0D\x0A" # read serial number
def check_status(status):
    if status == 0:
        return "senor nominal"
    if (status >> 0) & 1:
        return "preheat not done"
    if (status >> 1) & 1:
        return "general sensor error"
    if (status >> 2) & 1:
        return "ppm too high"
    if (status >> 3) & 1:
        return "ppm too low"
    if (status >> 4) & 1:
        return "not calibrated"
    if (status >> 5) & 1:
        return "sensor drift"
def process(a, data):
    a.write(data)
    header = a.read(2)
    if header:
        if header[0] == 0x16:
            pass
            #print("header seems intact")
        else:
            print("header seems corrupt")
        command = a.read(header[1])
        if command[0] == data[2]:
            pass
            #print("command matches")
        else:
            print("command seems off")
        cksum = a.read(1)
        calc = 0
        for i in header+command:
            calc += i
        calc = calc % 256
        calc = 256 - calc
        if calc == cksum[0]:
            pass
            #print("packet intact")
        else:
            print("invalid packet")
        if data == command_read_co2:
            ppm = command[1] * 256 + command[2] # decode ppm
            status = command[3] # get status byte
            status = check_status(status)
            ppm = {'ppm':ppm}
            #print(header,command,cksum,calc,cksum[0],ppm) # print ppm
            return ppm,status
        if data == command_read_filmware_version:
            name = command[1:17] # decode name
            #print(header,command,cksum,calc,cksum[0],name.decode()) # print name
            return name.decode(errors='ignore')
        if data == command_read_serial_number:
            #print(command[-2:-1])
            return command[-2:-1]
    else:
        print("DID NOT GET ANY DATA")
        b = open("errors.txt",'a')
        b.write("GOT NO DATA AT TIME: " + str(time.time())+ "\n")
        b.close()
        return process(a,data)
handle_arduino = 0
def set_ard_handle(func):
	global handle_arduino
	handle_arduino = func
def loop():
    while True:
        results = []
        results.append([process(sen1,command_read_serial_number),process(sen1,command_read_co2)])
        results.append([process(sen2,command_read_serial_number),process(sen2,command_read_co2)])
        results.append(handle_arduino(sen3))
        results.append(handle_arduino(sen4))
        results.append(time.time())
        #print(results)
        f = open('data.txt','ab')
        f.write(base64.b64encode(pickle.dumps(results))+ b"\r\n")
        f.close()
        time.sleep(7200)  #17280 delay needed for 5 times a day
