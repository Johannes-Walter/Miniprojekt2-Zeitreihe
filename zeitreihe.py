import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


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

    del data["Currency"]
    return data


def plot_bar_chart(subplot, data):
    data = data.groupby("orderDaily").sum()
    print(data)
    subplot.bar(data.index, data["orderAmountInCents"])

    subplot.plot(data.index, data["orderAmountInCents"].rolling(7).mean(), color="red")
    subplot.plot(data.index, data["orderAmountInCents"].rolling(30).mean(), color="green")


def plot_overlaid_first_halfes(subplot, data):
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
    width=0.4
    #subplot.bar(data2.index+width/2, data2["orderAmountInCents"], color=(0, 0, 1, 1), width=width)
    subplot.bar(data1.index-width/2, data1["orderAmountInCents"], color=(0, 1, 0, 1), width=width)
    subplot.legend(["2021", "2020"])


def plot_overlaid_first_halfes_all(subplot, data):
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

def plot_amount_per_customer(subplot, data):
    data = data[data["orderState"] == "4"]
    data = data.groupby("customer").sum()
    data = data.sort_values("orderAmountInCents")
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
    subplot.plot(df_all.index, failed["orderAmountInCents"]/df_all["orderAmountInCents"])

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
    plot_overlaid_first_halfes(sub, data)
    plot_overlaid_first_halfes_all(sub, data)
    #plot_amount_per_product(sub, data)
    #plot_amount_per_customer(sub, data)
    #plot_relative_failed_sales(sub, data)
    import sys
    sys.exit()

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
    failed_sales_top = \
        failed_sales_stat[failed_sales_stat["orderState"] > 15]["orderDate"]

    # print(failed_sales_top)

    print(successful_sales)

    ''' Aufgabe 2 '''

    daily_successful_sales = \
        successful_sales.groupby(["orderDaily"])["orderAmountInCents"].sum()
    # successful_sales['moving_average']=successful_sales['orderAmountInCents'].rolling(50).mean()
    # successful_sales['moving_average'].plot()

    daily_successful_sales.plot(kind='area')

    # daily_successful_sales.rolling(2).mean().plot(kind='line')
    daily_successful_sales.rolling(50).mean().plot(kind='line', figsize=(10, 5))


    ''' Aufgabe 3 '''

    # daily_successful_sales.
