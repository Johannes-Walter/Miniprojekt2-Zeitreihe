import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
import datetime as dt
from itertools import cycle

data = pd.read_csv("salesdata.csv", sep=";", error_bad_lines=False)
data["orderDate"] = pd.to_datetime(data["orderDate"])
data["orderDaily"] = pd.to_datetime(data["orderDate"]).dt.date
data["orderDaily"] = pd.to_datetime(data["orderDaily"])



customer_terminated = data[data["orderState"] == 2]
system_error = data[data["orderState"] == 7]
successful_sales = data[data['orderState'] == 4]



''' Aufgabe 3 '''

''' DATA PREPARATION '''

successful_sales['orderAmountInCents']=successful_sales['orderAmountInCents'].apply(lambda x: x.replace(',','.')).astype(float)
daily_successful_sales = pd.DataFrame(successful_sales.groupby("orderDaily")["orderAmountInCents"].sum())

weekly = daily_successful_sales.resample('W') # aggregate data weekly
weekly_mean = weekly.mean()
weekly_mean.fillna(0, inplace=True) # remove nan values with 0


''' SEASONAL DECOMPOSITION '''
seas_decomp = seasonal_decompose(weekly_mean, period = 26) # decompose data in a trend, seasonal and residual series


''' FURTHER PROCESSING '''

def combine_seasonal_cols(input_df, seasonal_model_results): # add decomposed data to existing dataframe
    input_df['observed'] = seasonal_model_results.observed
    input_df['residual'] = seasonal_model_results.resid
    input_df['seasonal'] = seasonal_model_results.seasonal
    input_df['trend'] = seasonal_model_results.trend


def linReg(series):
    X = series.index.map(dt.datetime.toordinal).to_series().values.reshape(-1, 1) # values converts it into a numpy array
    Y = series.values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions
    plt.scatter(X, Y)
    plt.plot(X, Y_pred, color='red')
    plt.show()
    return linear_regressor.coef_[0][0], linear_regressor.intercept_[0] # unpack list in list to get int values for further use


combine_seasonal_cols(weekly_mean, seas_decomp)
weekly_mean.drop(['observed'], axis=1, inplace=True)
print(weekly_mean)
weekly_mean.plot(xlabel="Weeks", ylabel="Order Amount in Cents")

plt.show()


''' ISOLATE DECOMPOSED DATA '''

trend = weekly_mean['trend']
seasonality = weekly_mean['seasonal']
residual = weekly_mean['residual']
trend_clean = trend.dropna()


''' PERFORM LINEAR REGRESSION AND SAVE GRADIENT AND Y-OFFSET '''

gradient, y_offset = linReg(trend_clean) # linear regression using the trend from the seasonal decomposition



def createModelData():
    pred_time_range = pd.date_range("2019-11-24", periods=162, freq="W") # create dataframe for 162 weeks
    pred_time_range_ordinal = pred_time_range.map(dt.datetime.toordinal) # use ordinal time to simplify data addition
    predicted_sales = pd.DataFrame(columns=["linReg", 'seasonality', 'residual', 'model'], index = pred_time_range_ordinal)

    for x in pred_time_range_ordinal:  # linear regression over the whole 162 weeks
        pred_y = x * gradient + y_offset
        predicted_sales.loc[x]['linReg'] = pred_y

    predicted_sales.set_index(pred_time_range, inplace=True) # use non ordinal time as index

    ''' REPEATEDLY ADD SEASONALITY AND RESIDUAL VALUES TO MODEL DATAFRAME '''
    seasonality_slice_list = list(seasonality[:26].values) # one period of the seasonality
    residual_slice_list = list(residual[13:67].values) # all residual values

    seasonality_cycle = cycle(seasonality_slice_list) # cycle for multiple insert into dataframe
    residual_cycle = cycle(residual_slice_list)

    predicted_sales['seasonality'] = [next(seasonality_cycle) for count in range(predicted_sales.shape[0])]
    predicted_sales['residual'] = [next(residual_cycle) for count in range(predicted_sales.shape[0])]

    # sum of linear regression of trend, seasonality and residual values to yield a forecast
    predicted_sales['model'] = predicted_sales['linReg'] + predicted_sales['seasonality'] + predicted_sales['residual']  
    return predicted_sales



# model_df contains linear regression data, seasonality, residual values from the decomposition and the sum of all values
# for the time of 2019-11-24 to 2022-12-25
model_df = createModelData()
model_df[82:].plot() # plotting the second half of 2021 and all of 2022


''' ANALYZE DATA '''

def comparisons(dataModel, weekly_mean_original):

    second_half_2021 = dataModel['2021-06-01': '2021-12-31']['model'].sum()
    second_half_2020 = weekly_mean_original['2020-06-01': '2020-12-31']['orderAmountInCents'].sum()
    first_half_2021 = weekly_mean_original['2021-01-01': '2021-05-31']['orderAmountInCents'].sum()

    year_2022 = dataModel['2022-01-01' : '2022-12-31']['model'].sum()
    year_2021 = weekly_mean_original['2021-01-01':]['orderAmountInCents'].sum() + dataModel['2021-06-01':'2021-12-31']['model'].sum()
    year_2020 = weekly_mean_original['2020-01-01': '2020-12-31']['orderAmountInCents'].sum()

    half_year_growth_2021 = ((( second_half_2021 / first_half_2021 )) *100).round(2)
    second_halves_percent = ((( second_half_2021 / second_half_2020 )) *100).round(2)
    growth_2020_2021 = ((( year_2021 / year_2020 )) *100).round(2)
    growth_2021_2022 = ((( year_2022 / year_2021 )) *100).round(2)

    print(f'\nExpected growth in sale second half of 2021 compared to second half of past year: {second_halves_percent} %')
    print(f'\nExpected growth in sale for the second half of 2021 vs first half 2021: {half_year_growth_2021} %')
    print(f'\nExpected growth in sale for 2020 vs 2021: {growth_2020_2021} %')
    print(f'\nExpected growth in sale for 2021 vs 2022: {growth_2021_2022} %')

    
comparisons(model_df, weekly_mean)

plt.show()