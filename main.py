import serial
import time
import json
from Ippg import *
from ppg4 import *
from Filewriter_txt_JSONformat import *
from CreateJSONobj import *
import datetime as dt

# Opretter de klasser der skal bruges til at gemme data
ppgX_JSON = Ppg4_Class()
create_json_Obj = CreateJSONobj_class(ppgX_JSON, '', 'Here_Goes_A_New_Filename.csv')


port = serial.Serial('COM5', baudrate=115200, timeout=3.0)
#port = serial.Serial("/dev/tty.usbmodem01234567891", baudrate=115200, timeout=3.0)
my_string = ""
port.flushInput()
port.flushOutput()
print("setting data type to ascii")
port.write("set_cfg stream ascii\n".encode()) # Setting the returntype to ascii so it can be decoded

port.write("set_cfg report FF\n".encode())
#time.sleep(2)
port.write("get_format ppg 4\n".encode())
i = 0
while i < 100:
    response = port.readline()
    print(response)
    my_string = response.decode('ascii')
    if my_string.isalpha():
        print(my_string)
        i +=1
    if response == b'' or response =='' or i == 200:
        break

print("getting ppg data")
port.write("read ppg 4\n".encode())
i = 0
print("Start")
while 1>=0:
    my_bytes = port.readline()
    timestamp = dt.datetime.now().time()
    my_string = my_bytes.decode('ascii')
    if my_string[0:1].isnumeric():
        create_json_Obj.CreateAndSave(my_string, timestamp)
        i+= 1
        
    if my_bytes == b'' or my_bytes =='' or i == 100: #vi måler lige nu i 4500 samples svarende til 2 minutter og 10 sekunder
        print("we are breaking out")
        break

port.write("stop\n".encode())

print("done")
port.close()
