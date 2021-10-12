from typing import List
from Ippg import IPpg_Class
from json import JSONEncoder
import json

class Ppg4_Class(IPpg_Class,JSONEncoder):
    def __init__(self):
        print("PPG4 class: Created Ppg4 object")

    def UpdateJSON(self, ListOfValues, timestamp):
        self.timestmp = str(timestamp)
        self.smpleCnt = ListOfValues[0]
        self.grnCnt = ListOfValues[1]
        self.led2 = ListOfValues[2]
        self.led3 = ListOfValues[3]
        self.grn2Cnt = ListOfValues[4]
        self.irCnt = ListOfValues[5]
        self.redCnt = ListOfValues[6]
        self.accelX = ListOfValues[7]
        self.accelY = ListOfValues[8]
        self.accelZ = ListOfValues[9]
        self.hr = ListOfValues[10]
        self.rr = ListOfValues[11]
        self.rrsecure = ListOfValues[12]
        self.spo2 = ListOfValues[13]
    
    def toJSON(self): #Denne metode bruges til at serialisere ppg objektet. Den returnere et json objekt som string. 
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)

    #Provides an empty JSON object with the right headers i accordance to ppg5
    def getEmptyObjOn_ppg5_format(self):
        self.timestmp = 0
        self.smpleCnt = 0
        self.grnCnt = 0
        self.led2 = 0
        self.led3 = 0
        self.grn2Cnt = 0
        self.irCnt = 0
        self.redCnt = 0
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.hr = 0
        self.rr = 0
        self.rrsecure = 0
        self.spo2 = 0
        #self.ibi = 0
        theObjectAs_PyObj = json.loads(self.toJSON())
        return theObjectAs_PyObj

    def getValuesToSave(self): #Denne fnktion skal returnere de værdier man ønsker at få ud fra ppg5 formatet
        return [0,1,2,3,4,5,6,7,8,9,11,13,14,18,26] 

    
