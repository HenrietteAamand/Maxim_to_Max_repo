import json
from Ippg import *
from Filewriter_txt_JSONformat import *
from hr_manipulator import *

class CreateJSONobj_class:
    def __init__(self, ppgX_class, full_path_max, full_path_observations,filename_max, filename_observations) -> None:
        self.ppg_JSON = ppgX_class
        self.Filewriter_txt_jsonClass = WriteJSON_class(full_path_observations,filename_observations,self.ppg_JSON.getEmptyObjOn_ppg5_format())
        self.hr_manipulator = hr_manipulator_class(full_path_max, filename_max) #skal bruge en filsti til at gemme hr værdier til maxim
        #print("Succesfully created 'CreateJSONobj_class'")
        self.valuesToSave = self.ppg_JSON.getValuesToSave() #De værdier der skal gemmes fra strenglisten, der kommer ud fra USB-uret
        #print(self.valuesToSave)
        self.hr_counter = 0
        self.rr_counter = 0
        self.limit = 13 #Sættes til 25 ved 1 hz og 12 ved 2 Hz
        self.limitchanger = -1
        self.first_observations = 1500 #Denne parameter styre hvornår vi gerne vil have gemt data til maxim scriptet. 60*25*tid_i_minutter
        self.counter = 0
        self.oneMinute = 1
        
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
        if(self.counter >= self.first_observations): # Dette styrer hvornår vi gemmer til MAX filen
            self.save_hr_maxim()
            if self.counter % 25 == 0:
                self.oneMinute += 1
                print(str(self.json_obj['hr']))

        else:
            if self.counter % 25 == 0:
                print(self.oneMinute)
                self.oneMinute += 1
        self.counter += 1
    
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
            self.hr_manipulator.Check_for_spike() # Her tjekkes for spike, og der gemmes ti maximfilen
            self.limitchanger = self.limitchanger*(-1)
            self.limit += self.limitchanger
            self.hr_counter = 0
        self.hr_counter += 1








