import csv 
import json

class WriteJSON_class:
    def __init__(self, path, filename,empty_JSON_obj_with_Header):
        self.path = path
        self.filename = filename
        if(len(path) == 0):
            self.full_path = str(filename)
        else:    
            self.full_path = str(path) + "/" + str(filename)
        self.JSON_obj = empty_JSON_obj_with_Header

        #Åbner filen, tømmer den og skriver ny header
        data_file = open(self.full_path, 'w+', newline='') #w+ fordi så laves filen hvis ikke den allerede eksisterer
        csv_writer = csv.writer(data_file, delimiter=',')
        header = self.JSON_obj.keys()
        csv_writer.writerow(header)
        data_file.close()

    def SaveLineToFile(self, JSON_obj):
        #print("Printing JSON til file with path: " + str(self.full_path))
        #print("")
        data_file = open(self.full_path, 'a', newline='')
        csv_writer = csv.writer(data_file, delimiter=',')
        
        # Writing data of CSV file
        csv_writer.writerow(JSON_obj.values())
        data_file.close()
       