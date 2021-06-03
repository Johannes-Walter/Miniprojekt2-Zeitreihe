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

    del data["Currency"]
    return data


def plot_bar_chart(subplot, data):
    data = data.groupby("orderDaily").sum()
    print(data)
    subplot.bar(data.index, data["orderAmountInCents"])

    subplot.plot(data.index, data["orderAmountInCents"].rolling(7).mean(), color="red")
    subplot.plot(data.index, data["orderAmountInCents"].rolling(30).mean(), color="green")


def plot_overlaid_first_halfes(subplot, data):
    data = data.groupby("orderDaily").sum()
    data1 = data.loc[]

if __name__ == "__main__":
    data = pd.read_csv("salesdata.csv",
                       sep=";",
                       parse_dates=(["orderDate"]),
                       decimal=",")
    data = clean_sales_data(data)
    
    plt.figure(figsize=(20,12), dpi=200)
    # plot_bar_chart(plt.subplot(), data)
    plot_overlaid_first_halfes(plt.subplot(), data)

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
