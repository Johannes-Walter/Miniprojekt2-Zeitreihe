import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("salesdata.csv", sep=";", error_bad_lines=False)
data["orderDate"] = pd.to_datetime(data["orderDate"])
data["orderDaily"] = pd.to_datetime(data["orderDate"]).dt.date


customer_terminated = data[data["orderState"] == 2]
system_error = data[data["orderState"] == 7]
successful_sales = data[data['orderState'] == 4]

''' Aufgabe 1 a) '''

percentage_failed_sales = len(customer_terminated) / len(data)
print(f"Anteil abgebrochener Verkäufe: {percentage_failed_sales}%")


''' Aufgabe 1 b) '''


data_grouped = data[data["orderState"] == 4].groupby("orderDaily")
failed_sales_grouped = system_error.groupby("orderDaily")

failed_sales_stat = failed_sales_grouped.count()

#failed_sales_stat["orderState"].plot()
failed_sales_top = failed_sales_stat[failed_sales_stat["orderState"] > 15]["orderDate"]

# print(failed_sales_top)

print(successful_sales)

''' Aufgabe 2 '''

successful_sales['orderAmountInCents']=successful_sales['orderAmountInCents'].apply(lambda x: x.replace(',','.')).astype(float)
daily_successful_sales = successful_sales.groupby(["orderDaily"])["orderAmountInCents"].sum()
# successful_sales['moving_average']=successful_sales['orderAmountInCents'].rolling(50).mean()
# successful_sales['moving_average'].plot()

daily_successful_sales.plot(kind='')

# daily_successful_sales.rolling(2).mean().plot(kind='line')
daily_successful_sales.rolling(10).mean().plot(kind='line')


''' Aufgabe 3 '''

# daily_successful_sales.