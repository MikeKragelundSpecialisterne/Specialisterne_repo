import matplotlib.pyplot as plt
import pandas as pd
import os
import csv
import seaborn as sns

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

# Making a dataframe in pandas. 
df = pd.DataFrame(columns=header,data=generator)


# Firstly i want to find out which kind of complaints was genereally made to which company. 
# On the X-axis i want number of complaints and on the Y-axis  the companies.
# Then use seaborn to make a colorcoding, which can show me what kind of complaints. 
# This should give a nice overview of the different companies. 

#Parameters:
num_companies = 20 
num_complains = 5

# Identify the top 20 companies with the highest total complaints
top_companies = df["Company"].value_counts().head(num_companies).index 

# Filter the data for only these top companies
top_company_data = df[df["Company"].isin(top_companies)]

# Group by Company and Product, then count complaints
complaints_by_company_product = top_company_data.groupby(['Company', 'Product']).size().reset_index(name='Complaint_Count')

# Sort by complaint count (highest first), then by company, and take the top products
top_complaints_per_company = complaints_by_company_product.sort_values(['Complaint_Count', 'Company'], 
                                                                       ascending=[False, True]).groupby('Company').head(num_complains)

# Plotting the results
plt.figure(figsize=(12, 8))
sns.barplot(data=top_complaints_per_company, y='Company', x='Complaint_Count', hue='Product', dodge=False)
plt.title("Top Complained-about Products by Top Companies")
plt.xlabel("Number of Complaints")
plt.ylabel("Company")
plt.legend(title="Product")
plt.tight_layout()
plt.show()

#From seeing this graph we can conclude 3 things. 
# 1: The majority of rapports comes from 3 companies. 
# 2: The majority of rapports are "Credit reporting". 
# 3: The data might be a bit biased because of low variety.

# Next up i want to make a statistic about where the complaints were made. 
# So we want Time on the X-axis and number of complaints on the Y-axis. 
# To represent the states i'm using seaborn, to color code them.





#Params: 
num_states = 7
#I capped this at 7, because like the first plot, the majority of complaints comes from a few states.


# For some reason the data is not saved as datetime, so there was a mistake in my loader in preprocessing.py...
# Maybe datetimes can't be stored in csv?..
# Convert 'Date received' to datetime format if not already done
df["Date received"] = pd.to_datetime(df["Date received"], errors='coerce')

# Extract year and month to analyze trends over time
df["YearMonth"] = df["Date received"].dt.to_period("M")

# Group by State and YearMonth, count complaints
state_date_counts = df.groupby(['State', 'YearMonth']).size().reset_index(name='Complaint_Count')

# Calculate the total number of complaints for each state over the entire period
total_complaints_by_state = df.groupby('State')['Date received'].count()

# Select the top states based on the total complaint count
top_states = total_complaints_by_state.nlargest(num_states).index

# Filter the data for only these top states
filtered_state_data = state_date_counts[state_date_counts['State'].isin(top_states)]

# Pivot data to have dates on one axis and states on the other
state_date_pivot = filtered_state_data.pivot(index='YearMonth', columns='State', values='Complaint_Count').fillna(0)

# Convert YearMonth index to datetime format for plotting
state_date_pivot.index = state_date_pivot.index.to_timestamp()

# Plotting
plt.figure(figsize=(14, 8))
for state in top_states:
    plt.plot(state_date_pivot.index, state_date_pivot[state], label=state)

plt.title("Complaint Trends Over Time by State")
plt.xlabel("Date")
plt.ylabel("Number of Complaints")
plt.legend(title="State")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# We can see in this graph, it's actually a pretty even distrubution
# Also there is serveral spikes in the data, it's hard to conclude anything from this data. 
# There is a spike in complaints from Florida from 2021-2022, so let's analyse which complaints was made in that period. 


#First i will plot which complaints were made in 2020-2021


# Filter data for complaints from Florida in 2020-2021
arkansas_spike_data = df[(df['State'] == 'FL') & 
                         (df['Date received'] >= '2020-01-01') & 
                         (df['Date received'] <= '2021-12-31')]

# Group by complaint category to see which ones were most common
complaint_category_counts = arkansas_spike_data['Product'].value_counts()




plt.figure(figsize=(14, 8))  
complaint_category_counts.plot(kind='bar')
plt.yscale("log")
plt.title("Top Complaint Categories in Florida (2020-2021) -  Log Scale")
plt.xlabel("Complaint Category")
plt.ylabel("Number of Complaints (Log Scale)")
plt.xticks(rotation=90)  
plt.tight_layout()  
plt.show()


#Secondly i will plot what happend in 2021-2022, and see if we can find some irregularity


# Filter data for complaints from Florida in 2020-2021
arkansas_spike_data = df[(df['State'] == 'FL') & 
                         (df['Date received'] >= '2021-01-01') & 
                         (df['Date received'] <= '2022-12-31')]

# Group by complaint category to see which ones were most common
complaint_category_counts = arkansas_spike_data['Product'].value_counts()




plt.figure(figsize=(14, 8))  
complaint_category_counts.plot(kind='bar')
plt.yscale("log")
plt.title("Top Complaint Categories in Florida (2020-2021) -  Log Scale")
plt.xlabel("Complaint Category")
plt.ylabel("Number of Complaints (Log Scale)")
plt.xticks(rotation=90)  
plt.tight_layout()  
plt.show()

# Looking at this data we can see that "Mortage" and "Checking and savings account" switched place, from mortage being 5. to 4. 
# However there is a weak correlation, it's not enough to conclude anything. 

# Define the date range for the spike
spike_start = '2021-01-01'
spike_end = '2022-12-31'

# Filter data for complaints from Florida during the spike period
florida_spike_data = df[(df['State'] == 'FL') & 
                        (df['Date received'] >= spike_start) & 
                        (df['Date received'] <= spike_end)]


# Group by company to see which ones had the most complaints during the spike
company_counts = florida_spike_data['Company'].value_counts()

# Plot the top companies during the spike period
plt.figure(figsize=(10, 6))
company_counts.head(10).plot(kind='pie',autopct="%.2f%%")
plt.title("Top Companies in Florida (2020-2021 Spike)")
plt.xlabel("")
plt.ylabel("")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()