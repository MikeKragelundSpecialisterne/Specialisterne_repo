import os

warningString = "WARNING"
errorString = "ERROR"


file = open("SPEC_Uge3/opg2/app_log (logfil analyse) 1.txt","r")

allLines = file.readlines()
numSentences =len(allLines)

errors = []
warnings = []

for sentence in allLines:
    if errorString in sentence:
        errors.append(sentence)
    if warningString in sentence:
        warnings.append(sentence)

#To make it in this folder
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "Errors&Warnings.txt")

newfile = open(file_path, "w")

newfile.write(errorString + '\n')
newfile.write("Count =" + str(len(errors)) + '\n')
newfile.writelines(error + '\n' for error in errors)
newfile.write(warningString + '\n')
newfile.write("Count = " + str(len(warnings)) + '\n')
newfile.writelines(warning + '\n' for warning in warnings)

newfile.flush()
newfile.close()

file.close()