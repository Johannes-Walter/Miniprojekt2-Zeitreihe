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

print(failed_sales_top)