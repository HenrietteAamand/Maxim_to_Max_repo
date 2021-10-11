import json
from Ippg import *
from Filewriter_txt_JSONformat import *

class CreateJSONobj_class:
    def __init__(self, ppgX_class, full_path,filename_csv) -> None:
        self.ppg_JSON = ppgX_class
        self.Filewriter_txt_jsonClass = WriteJSON_class(full_path,filename_csv,self.ppg_JSON.getEmptyObjOn_ppg5_format())
        print("Succesfully created 'CreateJSONobj_class'")
        self.valuesToSave = self.ppg_JSON.getValuesToSave() #De værdier der skal gemmes fra strenglisten, der kommer ud fra USB-uret
        print(self.valuesToSave)
        

    def CreateAndSave(self, inputFromWatch, timestamp):
        n = 0
        i = 0
        ListOfValues = []
        input = inputFromWatch
        input_in_list_format = input.split(',')
        for value in input_in_list_format:
            if i == self.valuesToSave[n]:
                ListOfValues.append(value)
                n+=1
                if n == len(self.valuesToSave):
                    break
            i += 1
        self.ppg_JSON.UpdateJSON(ListOfValues, timestamp)
        self.Filewriter_txt_jsonClass.SaveLineToFile(json.loads(self.ppg_JSON.toJSON()))






