import pickle
import base64
import zlib
import sftpclient
import datetime
sep = b';'
client = "XXX.XXX.XXX.XXX",
    username="pi",
    password="usbpoortvanroger",
    use_known_hosts=False, 
)
f = client.download("rutger/data.txt")
data = f.read()

a = len(data)
print(a)
data = data.split(b"\r\n")
f1 = open("inside_box.csv",'wb')
f2 = open("outside_box.csv",'wb')
f1.write(b'date;time;ppm;temp;humidity;light;ground moisture;unprocessed ground moisture\r\n')
f2.write(b'date;time;ppm;temp;humidity;light;ground moisture;unprocessed ground moisture\r\n')
def parse_arduino(data):
    temp = data['Temperature'].encode().replace(b".",b",")
    humidity = data['Humidity'].encode().replace(b".",b",")
    light = data['Light'].encode().replace(b".",b",")
    ground_moisture = data['Ground humidity'].encode()
    unprocessed_ground_moisture = data['Raw ground humidity'].encode()
    return b''.join([sep,temp,sep,humidity,sep,light,sep,ground_moisture,sep,unprocessed_ground_moisture,b"\r\n"])
for packet in data:
    if packet:
        try:
            packet = base64.b64decode(packet)
            values = pickle.loads(packet)
        except:
            print("error")
            continue
        f1.write(datetime.datetime.fromtimestamp(values[4]).strftime("%D").encode() + sep)
        f2.write(datetime.datetime.fromtimestamp(values[4]).strftime("%D").encode() + sep)
        f1.write(datetime.datetime.fromtimestamp(values[4]).strftime("%T").encode() + sep)
        f2.write(datetime.datetime.fromtimestamp(values[4]).strftime("%T").encode() + sep)
        #print(values)
        co2_1 = values[0]
        if co2_1[0][0] == 0:
            f2.write(str(co2_1[1][0]['ppm']).encode())
        if co2_1[0][0] == 2:
            f1.write(str(co2_1[1][0]['ppm']).encode())
        co2_2 = values[1]
        if co2_2[0][0] == 0:
            f2.write(str(co2_2[1][0]['ppm']).encode())
        if co2_2[0][0] == 2:
            f1.write(str(co2_2[1][0]['ppm']).encode())
        arduino_1 = values[2][0]
        if arduino_1['Arduino'] == 'Arduino 2(outside of closed box)':
            f2.write(parse_arduino(arduino_1))
        else:
            f1.write(parse_arduino(arduino_1))
        arduino_2 = values[3][0]
        if arduino_2['Arduino'] == 'Arduino 2(outside of closed box)':
            f2.write(parse_arduino(arduino_2))
        else:
            f1.write(parse_arduino(arduino_2))
print(len(data))
f1.close()
f2.close()
