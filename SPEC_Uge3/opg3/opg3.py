import io
import os

try:
    file = open("SPEC_Uge3/opg3/source_data (Datamigrering hjælpeværktøj).csv","r")
    content = file.read()
    file.close()
except (IOError, FileNotFoundError) as e:
    if type(e) == IOError:
        print("Der er fejl")
    else: 
        print("Der er en anden fejl")
        
    

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "destination_file.txt")

newfile = open(file_path, "w")

destinationFile = open(file_path, "w")

print(content)
destinationFile.write(content)

destinationFile.flush()
destinationFile.close()

#skrivebestyttelse
errorname = "IOError"
