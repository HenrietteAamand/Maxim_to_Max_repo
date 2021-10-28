import json
from Ippg import *
from Filewriter_txt_JSONformat import *
from hr_manipulator import *

class CreateJSONobj_class:
    def __init__(self, ppgX_class, full_path,filename_max, filename_observations) -> None:
        self.ppg_JSON = ppgX_class
        self.Filewriter_txt_jsonClass = WriteJSON_class(full_path,filename_observations,self.ppg_JSON.getEmptyObjOn_ppg5_format())
        self.hr_manipulator = hr_manipulator_class('', filename_max)
        #print("Succesfully created 'CreateJSONobj_class'")
        self.valuesToSave = self.ppg_JSON.getValuesToSave() #De værdier der skal gemmes fra strenglisten, der kommer ud fra USB-uret
        #print(self.valuesToSave)
        self.hr_counter = 0
        self.rr_counter = 0
        self.limit = 13 #Sættes til 25 ved 1 hz og 12 ved 2 Hz
        self.limitchanger = -1
        
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
        self.json_obj = json.loads(self.ppg_JSON.toJSON())
        self.Filewriter_txt_jsonClass.SaveLineToFile(self.json_obj)
       #  self.calculate_hr_from_rr_maxim()
        self.save_hr_maxim()
    
    def calculate_hr_from_rr_maxim(self):
        if(float(self.json_obj['rr']) != 0.0):
            self.hr_manipulator.Add_rr_value(float(self.json_obj['rr']), self.json_obj['timestmp'])
            self.rr_counter += 1
            if(self.rr_counter == 5):
                self.hr_manipulator.Calculate_hr_from_rr()
                self.rr_counter = 0
                print('Saved hr value')

    def save_hr_maxim(self):
        self.hr_manipulator.Add_hr_value(float(self.json_obj['hr']), self.json_obj['timestmp'])
        if(self.hr_counter == self.limit):
            self.hr_manipulator.Check_for_spike()
            self.limitchanger = self.limitchanger*(-1)
            self.limit += self.limitchanger
            self.hr_counter = 0
        self.hr_counter += 1








