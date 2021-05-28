import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("salesdata.csv", sep=";", error_bad_lines=False)
data["orderDate"] = pd.to_datetime(data["orderDate"])
data["orderDaily"] = pd.to_datetime(data["orderDate"]).dt.date


failed_sales = data[data["orderState"] == 2]

percentage_failed_sales = len(failed_sales) / len(data)

print(f"Anteil abgebrochener Verkäufe: {percentage_failed_sales}%")

failed_sales = data[data["orderState"] == 7]


data_grouped = data[data["orderState"] == 4].groupby("orderDaily")
failed_sales_grouped = failed_sales.groupby("orderDaily")

t = data_grouped.count()
ü = failed_sales_grouped.count()

#ü["orderState"].plot()
top = ü[ü["orderState"] > 10]["orderDate"]


t["orderDate"].plot()
