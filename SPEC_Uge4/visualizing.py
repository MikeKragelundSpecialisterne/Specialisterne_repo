import matplotlib.pyplot as plt
import pandas as pd
import os
import csv
import seaborn as sns
import numpy as np

def loader(Get_header):  
    try: 
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "Fitted_data.csv")
        with open(file_path, "r", encoding="utf-8") as csvfile:
                        reader = csv.reader(csvfile)
                        header = next(reader)  # Get the first row as header
                        if Get_header:
                            yield header
                        else:
                            for  row in reader:
                                yield row
    except IOError as e:
        print("File not found:",e)
# Get header
generator = loader(True)
header =""
for line in generator:
    header = line

# Reinit without header
generator = loader(False)

# Creating the dataframe with generator. 
# At this stage we are consuming a bit more RAM, because we are going away from generators
df = pd.DataFrame(columns=header,data=generator)

#Plotting the products in a piechart. 
df["product_5"].value_counts().head(10).plot(kind="pie", autopct="%.2f%%", figsize=(12, 6))
plt.title("Distribution of complaints over products")
plt.ylabel("")
plt.show()


# Ensure that the "Date received" column is in datetime format
df["Date received"] = pd.to_datetime(df["Date received"], errors='coerce')

# Group by month and count occurrences
monthly_counts = df["Date received"].dt.to_period("M").value_counts().sort_index()

# Plot the data
monthly_counts.plot(kind="bar", figsize=(12, 6))

ax = monthly_counts.plot(kind="bar", figsize=(12, 6))
plt.xlabel("Month received")
plt.title("Occurrences by Month")
plt.ylabel("")
# Set x-axis ticks to display every 6th label
ax.set_xticks(range(0, len(monthly_counts), 6))
ax.set_xticklabels(monthly_counts.index[::6], rotation=45)

plt.tight_layout()
plt.show()



df["Issue"].value_counts().head(10).plot(kind="pie", autopct="%.2f%%",figsize=(12, 6))
plt.title("issue in each narrative")
plt.ylabel("")

plt.show()


df["Company"].value_counts().head(10).plot(kind="pie", autopct="%.2f%%",figsize=(12, 6))
plt.ylabel("")
plt.title("name of company that is complaint about")
plt.show()



df["State"].value_counts().head(10).plot(kind="pie", autopct="%.2f%%",figsize=(12, 6))
plt.title("the state location of the complaint")
plt.ylabel("")
plt.show()


df["Timely response?"].value_counts().head(2).plot(kind="pie", autopct="%.2f%%",figsize=(12, 6))
plt.title("Was the response timely?")
plt.ylabel("")
plt.show()


