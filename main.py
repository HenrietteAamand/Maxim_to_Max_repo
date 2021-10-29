import serial
import time
import json
from Ippg import *
from ppg4 import *
from Filewriter_txt_JSONformat import *
from CreateJSONobj import *
import datetime as dt
from filereader import *

tid_minutter = 0.5
#Opsætning:
opætnings_parametre = filereader_class.GetOpsaetning()
Testperson_nummer = opætnings_parametre['Testperson_nummer']
Fasenummer = opætnings_parametre['Fasenummer']
Navn_på_fase = opætnings_parametre['Navn_paa_fase']

print('Getting data for fase {0} where intervention is {1}', Fasenummer, Navn_på_fase)

# Opretter de klasser der skal bruges til at gemme data
ppgX_JSON = Ppg4_Class()
filename_full_observations = 'Testperson_' + Testperson_nummer + "_Fase_" + Fasenummer + "_" + Navn_på_fase + "_observationer" #Testperson_1_Fase_1_stilhed_observationer
filename_maxdata = 'Testperson_' + Testperson_nummer + "_Fase_" + Fasenummer + "_" + Navn_på_fase + "_maxdata" #Testperson_1_Fase_1_stilhed_maxdata 
full_path_full_observations = '/Users/sisselraahede/Documents/Au_Digital_design/Kandidat/Praktik/Isobel/Lydindhold/Max/Soundscape komposition/GenerativeCompositionAbleton/Observationer/RaaObservationer'
full_path_maxdata = '/Users/sisselraahede/Documents/Au_Digital_design/Kandidat/Praktik/Isobel/Lydindhold/Max/Soundscape komposition/GenerativeCompositionAbleton'

create_json_Obj = CreateJSONobj_class(ppgX_JSON, full_path_maxdata, filename_maxdata, full_path_full_observations, filename_full_observations)



create_json_Obj = CreateJSONobj_class(ppgX_JSON, full_path_full_observations, filename_maxdata, filename_full_observations)

#port = serial.Serial('COM5', baudrate=115200, timeout=3.0)
port = serial.Serial("/dev/tty.usbmodem01234567891", baudrate=115200, timeout=3.0)
my_string = ""
port.flushInput()
port.flushOutput()
print("setting data type to ascii")
port.write("set_cfg stream ascii\n".encode()) # Setting the returntype to ascii so it can be decoded

print("getting ppg data")
port.write("read ppg 4\n".encode())
i = 0
print("Start")
while True:
    my_bytes = port.readline()
    timestamp = dt.datetime.now().time()
    my_string = my_bytes.decode('ascii')
    if my_string[0:1].isnumeric():
        create_json_Obj.CreateAndSave(my_string, timestamp)
        i+= 1
        
    if my_bytes == b'' or my_bytes =='' or i == tid_minutter*25*60: #vi måler lige nu i 4500 samples svarende til 2 minutter og 10 sekunder
        #print("we are breaking out")
        break

port.write("stop\n".encode())

print("done getting data for fase {0} where intervention is {1}", Fasenummer, Navn_på_fase)
port.close()
