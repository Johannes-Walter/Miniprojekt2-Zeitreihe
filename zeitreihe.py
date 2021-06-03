import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def clean_sales_data(data):
    # remove unneccesary column
    del data["test"]

    # add daily intervall
    data["orderDaily"] = pd.to_datetime(data["orderDate"]).dt.date

    # translate every currencey to USD
    # These values are hard-coded based on some rough estimation and googeling
    exchange_rates = {"EUR": 1.2,
                      "CHF": 1.05}

    for key, value in exchange_rates.items():
        data.loc[data["Currency"] == key, "orderAmountInCents"] = \
            data.loc[data["Currency"] == key, "orderAmountInCents"] * value

    data["orderAmountInCents"] /= 100

    del data["Currency"]
    return data


def plot_bar_chart(subplot, data):
    data = data.groupby("orderDaily").sum()
    print(data)
    subplot.bar(data.index, data["orderAmountInCents"])

    subplot.plot(data.index, data["orderAmountInCents"].rolling(7).mean(), color="red")
    subplot.plot(data.index, data["orderAmountInCents"].rolling(30).mean(), color="green")


def plot_sold_amount_monthly(subplot, data, offset=0, width=0.4):
    data = data[data["orderState"] == "4"]
    data.index = pd.to_datetime(data["orderDate"])
    data = data.resample("M").sum()

    #data1 = data.loc[(data.index > datetime.datetime(2020, 1, 1))
    #                 & (data.index < datetime.datetime(2021, 1, 1))]
    #data1.index = range(1, len(data1.index)+1)

    #data2 = data.loc[(data.index > datetime.datetime(2021, 1, 1))
    #                  & (data.index < datetime.datetime(2022, 1, 1))]
    # data2.index = range(1, len(data2.index)+1)
    data1  = data
    data1.index = range(1, len(data1.index)+1)
    #width=0.4
    #subplot.bar(data2.index+width/2, data2["orderAmountInCents"], color=(0, 0, 1, 1), width=width)
    subplot.bar(data1.index-offset, data1["orderAmountInCents"], width=width)#, color=(0, 1, 0, 1), width=width)
    subplot.legend(["2021", "2020"])


def plot_total_amount_monthly(subplot, data):
    data.index = pd.to_datetime(data["orderDate"])
    data = data.resample("M").sum()

    # data1 = data.loc[(data.index > datetime.datetime(2020, 1, 1))
    #                  & (data.index < datetime.datetime(2021, 1, 1))]
    # data1.index = range(1, len(data1.index)+1)

    # data2 = data.loc[(data.index > datetime.datetime(2021, 1, 1))
    #                  & (data.index < datetime.datetime(2022, 1, 1))]
    # data2.index = range(1, len(data2.index)+1)

    data1  = data
    data1.index = range(1, len(data1.index)+1)

    width=0.4
    #subplot.bar(data2.index+width/2, data2["orderAmountInCents"], color=(0, 0, 1, 0.5), width=width)
    subplot.bar(data1.index-width/2, data1["orderAmountInCents"], color=(0, 1, 0, 0.5), width=width)
    subplot.legend(["2021", "2020"])

def plot_amount_per_product(subplot, data):
    data = data[data["orderState"] == "4"]
    data = data.groupby("product").sum()
    subplot.bar(data.index, data["orderAmountInCents"])

def plot_relative_failed_sales(subplot, data):
    #df_all = data[data["orderState"] == "4"]
    df_all = data
    df_all.index = pd.to_datetime(df_all["orderDate"])
    df_all = df_all.resample("D").sum()
    #successful.index = range(1, len(successful.index)+1)
    print(df_all)

    failed = data[data["orderState"] == "7"]
    failed.index = pd.to_datetime(failed["orderDate"])
    failed = failed.resample("D").sum()
    #failed.index = range(1, len(failed.index)+1)
    failed.reindex(df_all.index)
    print(failed)
    width=0.4
    subplot.bar(df_all.index, failed["orderAmountInCents"]/df_all["orderAmountInCents"])

def plot_products_monthly(subplot, data):
    offset = 0.8/len(data["product"].unique())
    i = 0
    for product in data["product"].unique():
        plot_sold_amount_monthly(subplot, data[data["product"]==product], i*offset, offset)
        i += 1

if __name__ == "__main__":
    data = pd.read_csv("salesdata.csv",
                       sep=";",
                       parse_dates=(["orderDate"]),
                       decimal=",",
                       dtype={"test": str,
                              "orderId": str,
                              "orderState": str,
                              "customer": str,
                              "product": str,
                              "orderDate": str,
                              "orderAmountInCents": float,
                              "Currency": str})
    data = clean_sales_data(data)

    plt.figure(figsize=(20,12), dpi=200)
    sub = plt.subplot()
    #plot_bar_chart(sub, data)
    #plot_sold_amount_monthly(sub, data)
    #plot_total_amount_monthly(sub, data)
    #plot_amount_per_product(sub, data)
    #plot_relative_failed_sales(sub, data)
    plot_products_monthly(sub, data)