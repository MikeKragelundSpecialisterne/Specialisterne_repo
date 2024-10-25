import os
import sys

try:
    file = open("SPEC_Uge3/opg3/source_data (Datamigrering hjælpeværktøj).csv","r")
    content = file.read()
    file.close()
except (IOError, FileNotFoundError) as e:
    if type(e) == IOError:
        sys.exit("Læsningen af filen fejlede")
    else: 
        sys.exit("Filen blev ikke fundet, tjek om filen er i denne mappe")
        

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "destination_file.txt")

#If the file dosnt exists make a new. 
if not os.path.isfile(file_path):
    newfile = open(file_path, "w")
    destinationFile = open(file_path, "w")
    destinationFile.write(content)
    destinationFile.flush()
    destinationFile.close()
else: 
    try:
        file = open(file_path,"w")
        file.write(content)
        file.flush()
        file.close()
    except (PermissionError) as e:
        print("Fejl i skrivning")
        sys.exit("Destinations-filen eksistere allerede og er skrivebeskyttet")
        
