import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Forbindelse til databasen.
con = mysql.connector.connect(user="HansChristian", password="Kodeord", host="127.0.0.1", database="northwind")

cursor = con.cursor()

#Analyse for salg. Først kigger vi på hvor meget hvert land har købt for. 
cursor.execute("SELECT c.Country, SUM(od.UnitPrice * od.Quantity) AS TotalSales FROM orders o JOIN customers c ON o.CustomerID = c.CustomerID JOIN     orderdetails od ON o.OrderID = od.OrderID GROUP BY c.Country ORDER BY TotalSales DESC")
rowsOrders = cursor.fetchall()

columns = ['Country', 'TotalSales']
df = pd.DataFrame(rowsOrders, columns=columns)

#Typekonvertering
df['TotalSales'] = pd.to_numeric(df['TotalSales'], errors='coerce')
#Null håndtering. 
df['TotalSales'].fillna(0, inplace=True)


df.plot(x='Country', y='TotalSales', kind='bar', figsize=(10, 6), title="Purchase per country")

plt.gcf().tight_layout()
plt.show()

cursor.reset()

#SQL sætning der finder hvilket land der har købt mest af hvilke vare. 

query = """
    SELECT 
        c.Country, 
        p.ProductName, 
        SUM(od.Quantity) AS TotalQuantity
    FROM 
        orders o
    JOIN 
        customers c ON o.CustomerID = c.CustomerID
    JOIN 
        orderdetails od ON o.OrderID = od.OrderID
    JOIN 
        products p ON od.ProductID = p.ProductID
    GROUP BY 
        c.Country, p.ProductName
    ORDER BY 
        c.Country, TotalQuantity DESC;
"""

cursor.execute(query)
rows = cursor.fetchall()
columns = ['Country', 'ProductName', 'TotalQuantity']
df = pd.DataFrame(rows, columns=columns)

#Typekonvertering
df['TotalQuantity'] = pd.to_numeric(df['TotalQuantity'], errors='coerce')
#Null håndtering. 
df['TotalQuantity'].fillna(0, inplace=True)

#Hvilke produkter USA køber mest af. 
#Da jeg har 3 variabler - produkt, mængde og land, er jeg tvunget til at udskifte landet, da jeg umiddelbart ikke kan vise alle på en gang. 
country = "USA"
df_usa = df[df['Country'] == f'{country}']
df_usa.plot(x='ProductName', y='TotalQuantity', kind='bar', figsize=(10, 6), title=f"Most purchased product by {country}")
plt.gcf().tight_layout()
plt.show()


cursor.reset()

#Jeg kigger her på hvilke kunder i hvilket land der har købt mest. 

query = """
    SELECT 
    c.Country, 
    c.CustomerID, 
    SUM(od.Quantity * od.UnitPrice) AS TotalSales
FROM 
    orders o
JOIN 
    customers c ON o.CustomerID = c.CustomerID
JOIN 
    orderdetails od ON o.OrderID = od.OrderID
GROUP BY 
    c.Country, c.CustomerID;
"""

cursor.execute(query)

rows = cursor.fetchall()

columns = ['Country', 'CustomerID', 'TotalSales']
df = pd.DataFrame(rows, columns=columns)

df['TotalSales'] = pd.to_numeric(df['TotalSales'], errors='coerce')
df = df.dropna(subset=['TotalSales'])


df_country_avg = df.groupby('Country')['TotalSales'].mean().reset_index()
df_country_avg.plot(x='Country', y='TotalSales', kind='bar', figsize=(10, 6), title='Average Customer Lifetime Value by Country')


plt.gcf().tight_layout()
plt.ylabel('Average Total Sales per Customer')
plt.show()


#2. plot analysere top 5 kunder pr land.

#Bruger seaborn her til at få farvekodet landene.
sns.set_theme(style="whitegrid")
g = sns.catplot(
    data=df.groupby('Country').apply(lambda x: x.nlargest(5, 'TotalSales')).reset_index(drop=True),
    x="CustomerID", y="TotalSales", hue="Country", kind="bar", height=6, aspect=2, palette="Set3"
)

g.set_xticklabels(rotation=90)
g.set_axis_labels("Customer ID", "Total Sales")
g.figure.suptitle("Top 5 Customers per Country", y=1.02)

plt.tight_layout()
plt.show()


cursor.close()
con.close()