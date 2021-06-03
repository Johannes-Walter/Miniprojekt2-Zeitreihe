import pandas as pd
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

    data["orderAmountInDollar"] = data["orderAmountInCents"] / 100

    del data["Currency"]
    return data


def plot_sold_amount_monthly(subplot, data, offset=0, width=25):
    data.index = pd.to_datetime(data["orderDate"])
    data = data.resample("M").sum()

    data1 = data
    subplot.bar(data1.index+pd.to_timedelta(offset, unit="D"), data1["orderAmountInDollar"], width=width)
    subplot.axvline(x=pd.to_datetime("1.1.2020"), color=(.5, .5, .5, .5))
    subplot.axvline(x=pd.to_datetime("1.1.2021"), color=(.5, .5, .5, .5))
    plt.suptitle("Monatlich verkaufter Warenwert")


def plot_amount_per_product(subplot, data):
    data = data.groupby("product").sum()
    subplot.bar(data.index, data["orderAmountInDollar"])
    plt.suptitle("Verkaufter Wert pro Produkt")


def plot_relative_failed_sales(subplot, data):
    data.index = pd.to_datetime(data["orderDate"])

    failed = data[data["orderState"] == "7"]
    failed = failed.resample("D").sum()
    data = data.resample("D").sum()
    failed_percentage = (failed["orderAmountInDollar"]
                         / data["orderAmountInDollar"]).median()

    subplot.bar(data.index,
                failed["orderAmountInDollar"]/data["orderAmountInDollar"])
    # 100%-Linie
    subplot.axhline(y=1, linestyle="--", color="black")

    # Durchschnittlicher Fail
    subplot.axhline(y=failed_percentage, linestyle="--", color="black")

    # Jahresmarker
    subplot.axvline(x=pd.to_datetime("1.1.2020"), color=(.5, .5, .5, .5))
    subplot.axvline(x=pd.to_datetime("1.1.2021"), color=(.5, .5, .5, .5))
    plt.suptitle("Anteil fehlgeschlagener Verkäufe pro Tag")
    plt.title(f"Durchschnitt über den Zeitraum: {failed_percentage*100}%")


def plot_products_monthly(subplot, data):
    products = data["product"].unique()
    offset = 25/len(products)
    for iter, product in enumerate(products):
        plot_sold_amount_monthly(subplot,
                                 data[data["product"] == product],
                                 (iter+1) * offset,
                                 offset)
    plt.legend(products)
    plt.suptitle("Monatlicher Umsatz pro Produkt")


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

    sucessful_sales = data[data["orderState"] == "4"]

    plt.figure(figsize=(20, 12), dpi=200)

    sub = plt.subplot()
    plot_sold_amount_monthly(sub, sucessful_sales, offset=0)
    plt.show()

    plt.figure(figsize=(20, 12), dpi=200)
    plot_amount_per_product(plt.subplot(), sucessful_sales)
    plt.show()

    plt.figure(figsize=(20, 12), dpi=200)
    plot_relative_failed_sales(plt.subplot(), data)
    plt.show()

    plt.figure(figsize=(20, 12), dpi=200)
    plot_products_monthly(plt.subplot(), data)
    plt.show()
