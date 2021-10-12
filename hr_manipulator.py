from Filewriter_txt_JSONformat import *
from max_dataobj import *

class hr_manipulator_class:
    def __init__(self, path, filename):
        #opret alle de lister der skal addes til og trækkes fra. 
        self.hr_list = []
        self.rr_list = []
        self.timestamp_list = []
        self.oldhr = 60
        self.first_time = True

        self.max_dataobj = Max_dataobj_class()
        self.filewriter = WriteJSON_class(path, filename, self.max_dataobj.Get_Empty_Jason())
        
    def Add_rr_value(self, rr_value,timestamp):
        # tilføj rr-værdi til liste
        if(len(self.rr_list)>0):
            if rr_value <= 1.4*self.rr_list[len(self.rr_list)-1] and rr_value > 0.85*self.rr_list[len(self.rr_list)-1]:
                self.rr_list.append(rr_value)
                self.timestamp_list.append(timestamp)
                print('Added rr-value: ' + str(rr_value))
            else:
                print("rr value not added")
                #lige nu gemmer vi bare ikke værdien hvis den er for høj eller for lav
                pass
        else:
            self.rr_list.append(rr_value)
            self.timestamp_list.append(timestamp)

    def Calculate_hr_from_rr(self):
        #Beregn hr ud fra foregående 10 rr-værdier, fjern derefter de 5 ældste rr-værdier, så vi beregner ca hvert 5. sekund, men over 10 sekunders data
        # returner en hr
        # husk også her at korrigere for procentlige stigninger der er for høje, og absolutte værdier der er helt hen i hegnet
        print(len(self.rr_list))
        if(len(self.rr_list) >= 4):
            hr = float("{:.1f}".format(60000/(sum(self.rr_list)/len(self.rr_list))))
            self.UseFilewriter(hr,self.timestamp_list[len(self.timestamp_list)-1], 0)

            #gemmer de sidste 10 værdier
            n = -10
            self.rr_list = self.rr_list[n:]
            self.timestamp_list = self.timestamp_list[n:]
        else:
            hr = self.oldhr
        return hr

    def Add_hr_value(self, hr_value, timestamp):
        # tilføj en hr værdi til en hr_listen. 
        self.hr_list.append(hr_value)
        self.timestamp_list.append(timestamp)
         
    def Check_for_spike(self):
        if(self.first_time):
            self.oldhr = sum(self.hr_list)/len(self.hr_list)
        
        noSpike = False
        n = len(self.hr_list)-1
        while(noSpike == False):
            #Hvis den senest beregnede hr afviger med mindre end 4 bpm, så accepteres den, og denne returneres
            if(abs(self.hr_list[n]-self.oldhr) < 2):
                self.oldhr = self.hr_list[n]
                self.UseFilewriter(self.oldhr,self.timestamp_list[n], 0)
                noSpike = True
                print("match found at n = " + str(n) + " with hr " + str(self.oldhr))
            
            # hvis der kun detekteres spikes i denne hr liste så accepteres at der er sket en ændring og der returneres et gennemsnit af de 10 hr værder
            if(n == len(self.hr_list)-6):  
                self.oldhr = float("{:.1f}".format(sum(self.hr_list)/len(self.hr_list)))
                self.UseFilewriter(self.oldhr,self.timestamp_list[n], 1)
                noSpike = True #dette er ikke helt sandt, men det er den måde vi kommer ud af whileloopet
                print("NO match found, hr is " + str(self.oldhr))
            n -= 1
        self.hr_list.clear()
        self.timestamp_list.clear()

    def UseFilewriter(self, hr, timestamp, flag):
        self.max_dataobj.UpdateJSON(hr, timestamp,flag)
        self.filewriter.SaveLineToFile(json.loads(self.max_dataobj.toJSON()))

