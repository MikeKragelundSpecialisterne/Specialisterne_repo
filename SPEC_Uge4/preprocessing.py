import pandas as pd
import os
import csv
from datetime import datetime
from collections import defaultdict

# Initial loader, using a generator function, to reduce memory consumption. 
# It goes though one row at a time.

# Params: skip_colums (list): index of which column should be skipped.
def loader(skip_columns=None):
    if skip_columns is None:
        skip_columns = []
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "complaints.csv")
        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Get the first row as header

            # Filter header to remove skipped columns
            filtered_header = [col for i, col in enumerate(header) if i not in skip_columns]
            yield filtered_header

            for row in reader:
                # Filter each row to exclude the columns in skip_columns
                filtered_row = [val for i, val in enumerate(row) if i not in skip_columns]
                yield filtered_row
    except IOError as e:
        print("File not found:", e)
#First we init the generator
generator = loader() 

#I want to have a clear view of the data, so i get a sample size of 5
header = next(generator)
print(header)
sample_data = [next(generator) for _ in range(5)]

# Load the sample data into a DataFrame with the filtered header
df = pd.DataFrame(sample_data, columns=header)

# Display the DataFrame

print(df)

#checking for dublicates:
df = pd.DataFrame(columns=header,data=generator)
print(df.duplicated().sum())
#We are getting a 0, so we are good!  


# In the print above we can see that 1. & 3. row is unique values. 
# 1. is a index number, which won't have relevance and the 3. is a custom description.
# While useful in a case-to-case basis, in a huge dataset like this, it's not usefull and i'll filter it away. 
generator = loader(skip_columns=[0,2])
# Get header
header = next(generator)
# Get 5 rows of data
sample_data = [next(generator) for _ in range(5)]
# Making Dataframe
df = pd.DataFrame(sample_data, columns=header)

print(df)

# This is looking much better. 

# Now we got a new issue,"Date received", which is a date, i would like to parse that value into an actual date. 

print("\nFiltered DataFrame (before date parsing):")
print(df["Date received"])
# Pandas got an inbuild function that parses to datetime.
df['Date received'] = pd.to_datetime(df['Date received'], errors='coerce')
# Print sentence to confirm that the date is parsed. 
print("\nFiltered DataFrame (after date parsing):")
print(df["Date received"])

# Now we got it parsed into a datetime, which is easier to work with in python. 
# Normally you would load all the data in and then manipulate with it. 
# Because we are using generators, i will have to make a new generator, which can do the parsing. 

# Next problem is null values. 
# Firstly i want to identify how many null values there is in each column of the dataset.
# Since we removed all ints, and now only have dates and strings we have to do string search. 

generator = loader(skip_columns=[0,2])

header = next(generator)
# I make a defaultdict, because its easier to init and configure than a normal dict. 
empty_counts = defaultdict(int)

# Iterating though the objects, looking for empty values. 
# I include index here, so that we can see in which category the empty value is in
for row in generator:
    for index, value in enumerate(row):
        if value == "":
            empty_counts[header[index]] += 1

# Display the count of empty strings for each column
print("Empty string values per column:")
for column, count in empty_counts.items():
    print(f"{column}: {count}")

# Now we know that we got a lot of null values in "Sub-issue", "Sub-product" and a few in "State"
# There is several approaches to this, the one i prefer is to fill out the values with a custom text. 


# Since we are using generators, i can't manipulate with the data after it's been loaded the first time
# So i will have to edit the loader, to make it filter each row while doing the initial load.

# Params: skip_columns (list): List of column indices to skip.
# fill_values (dict): Dictionary where keys are column names and values are fill values.

def loaderv2(skip_columns=None, fill_values=None):
    #Loading the user defined params
    if skip_columns is None:
        skip_columns = []
    if fill_values is None:
        fill_values = {}
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "complaints.csv")
        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Get the first row as header

            # Filter header to remove skipped columns
            filtered_header = [col for i, col in enumerate(header) if i not in skip_columns]
            yield filtered_header

            # Find indices for columns to fill missing values
            fill_indices = {filtered_header.index(col): fill_value for col, fill_value in fill_values.items() if col in filtered_header}


            total_rows = sum(1 for _ in reader)  # This consumes the reader
            csvfile.seek(0)  # Go back to the start of the file
            next(reader)  # Skip header again
            current_row = 0
            for row in reader:
                # Filter each row to exclude the columns in skip_columns
                filtered_row = [val for i, val in enumerate(row) if i not in skip_columns]

                # Replace empty values in specified columns
                for i, fill_value in fill_indices.items():
                    if i < len(filtered_row) and filtered_row[i] == "":
                        filtered_row[i] = fill_value
                        
                 #Filter string dates to datetime64 - this is a super heavy operation.. 
                for index, column in enumerate(filtered_header):
                    if column == 'Date received' and index < len(filtered_row):
                        filtered_row[index] = pd.to_datetime(filtered_row[index], errors='coerce')
                        
                 # Update progress every 1% of total rows
                 # Note * I put this on because the operation above took approx 20 mins to compute
                 # I was 99% sure that there was a infinite loop somewhere.
                current_row += 1
                if current_row % (total_rows // 100) == 0:
                    percentage = (current_row / total_rows) * 100
                    print(f"Processed {percentage:.2f}% of rows.")
                    
                yield filtered_row
    except IOError as e:
        print("File not found:", e)
fill_values = {
    'Sub-issue': 'No Sub-issue',
    'Sub-product': 'No Sub-product',
    'State': 'State unknown'
}

# Initialize the generator with skipped columns and fill values
generator = loaderv2(skip_columns=[0, 2], fill_values=fill_values)
header = next(generator)

# Confirming the new loader filters correctly.

# Initialize empty counts dictionary
empty_counts = defaultdict(int)

# Iterate through each row to count empty strings and apply fill values
for row in generator:
    for index, value in enumerate(row):
        # Count empty strings before filling
        if value == "":
            empty_counts[header[index]] += 1

# Display the count of empty strings for each column, using value:key pairs from the dict
print("Empty string values per column after filling:")
for column, count in empty_counts.items():
    print(f"{column}: {count}")

# It looks like the function worked!
#---------------------------------------------------------------------------------------------------------------------------------

# Because the loader function is so heavy in operation, i've chosen to save the output in a new csv file.
# This will allow me to use a much more simple/fast generator, in my visualization file. 

# Initialize the generator with skipped columns and fill values
generator = loaderv2(skip_columns=[0], fill_values=fill_values)
header = next(generator) 

# Specify the output file path - getcwd returns the current dir
output_file_path = os.path.join(os.getcwd(), "Fitted_data_With text.csv")

# Open a new CSV file and write the processed data into it
try:
    #I use newline, because its a csv file, if i were not to use it, python would make a \n at every new line. 
    with open(output_file_path, "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header
        writer.writerow(header)
        
        # Write the data rows
        for row in generator:
            writer.writerow(row)

    print(f"Data has been successfully saved to {output_file_path}")
    
except IOError as e:
    print("Error writing to file:", e)