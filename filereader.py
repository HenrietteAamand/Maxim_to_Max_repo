import csv

class filereader_class:
    def GetOpsaetning():
        csv_file_original =  open('Opsaetning.csv', mode='r')
        csv_reader = csv.DictReader(csv_file_original, delimiter = ';')
        csv_reader = list(csv_reader)
        print(csv_reader)

        dict = {}
        dict['Testperson_nummer'] = csv_reader[len(csv_reader)-1]['ï»¿Testperson_nummer']
        dict['Fasenummer'] = csv_reader[len(csv_reader)-1]['Fasenummer']
        dict['Navn_paa_fase'] = csv_reader[len(csv_reader)-1]['Navn_paa_fase']

        csv_file_original.close()
        return dict