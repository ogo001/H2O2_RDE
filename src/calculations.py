from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calibration_mean(data_selection) -> pd.DataFrame:
    data = data_selection
    data['Concentration'] = pd.to_numeric(data['Concentration'])
    df = data.groupby('Concentration', as_index=False).mean()
    df = df.rename(columns={'Concentration': 'Concentration Mean', 'Time': 'Time Mean', 'Signal': 'Signal Mean'})

    return df


def calibration_regression(data):
    calib_mean = calibration_mean(data_selection=data)

    lr = LinearRegression()
    x = np.array(calib_mean['Concentration Mean']).reshape((-1, 1))
    y = np.array(calib_mean['Signal Mean']).reshape((-1, 1))

    lr.fit(x, y)
    ypred = lr.predict(x)

    plt.scatter(x, y, color='red')
    plt.plot(x, ypred)
    plt.show()
    print(f'Slope:{lr.coef_} and intercept:{lr.intercept_}')

    return lr.coef_, lr.intercept_


def signal_to_concentration(regression_parameters,truncated_data):

    a, b = regression_parameters
    col_names = [col for col in truncated_data.columns]

    h2o2_y = [(i * a + b) for i in truncated_data[col_names[1]]]

    print(np.array(h2o2_y)[0])

    #plt.plot(truncated_data[col_names[0]], h2o2_y)