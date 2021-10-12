from json import JSONEncoder
import json

class Max_dataobj_class():
    def UpdateJSON(self, hr, timestamp, flag):
        self.timestamp = timestamp
        self.hr = hr
        self.fixed = flag

    def Get_Empty_Jason(self):
        self.timestamp = 0
        self.hr = 0
        self.fixed = 0
        theObjectAs_PyObj = json.loads(self.toJSON())
        return theObjectAs_PyObj

    def toJSON(self): #Denne metode bruges til at serialisere ppg objektet. Den returnere et json objekt. 
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)