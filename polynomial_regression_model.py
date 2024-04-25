from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from matplotlib import pyplot as plt


dataframe = pd.read_csv("data/dataframe_toyota_cars.csv")

x = dataframe[["volume", "power", "mileage", "production_year"]]
y = dataframe["price"]

def print_error_metrics(y, y_pred):
    mae = 0
    count = 0
    for i, val in enumerate(y.values):
        mae += abs(val - y_pred[i])
        if abs(val - y_pred[i]) / val * 100 < 10:
            count += 1
    mae /= len(y_pred)
    count = count / len(y_pred) * 100
    print(f"absolute error: {mae}")
    print(f"good predictions percent: {round(count)}")

def print_error_metrics2(y, y_pred, barplot=False):
    mae = 0
    count = 0
    accuracies = []
    for i, val in enumerate(y.values):
        mae += abs(val - y_pred[i])
        accuracy_percent = abs(val - y_pred[i]) / val * 100
        accuracies.append(accuracy_percent)
        if accuracy_percent < 10:
            count += 1
    mae /= len(y_pred)
    count = count / len(y_pred) * 100
    print(f"absolute error: {mae}")
    print(f"good predictions percent: {round(count)}")
    if barplot:
        intervals = [i for i in range(0, 100, 10)]
        interval_values = [0] * len(intervals)

        for val in accuracies:
            i = int(val // 10)
            if i < 0 or i > len(intervals)-1:
                continue
            print(i)
            interval_values[i] += 1
        interval_values = [((val*100) // len(accuracies)) for val in interval_values]
        plt.bar([f'{i}-{i + 10}%' for i in intervals], interval_values)
        plt.xlabel('Диапазон относительных погрешностей')
        plt.ylabel('Количество ошибок')
        plt.title('Столбчатая диаграмма распределения относительных погрешностей')
        plt.show()

def polynomial_regression_create(degree=4):
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    x_poly = poly.fit_transform(x)
    x_train, x_test, y_train, y_test = train_test_split(x_poly, y, test_size=0.2, random_state=0)
    scaler = MinMaxScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    model = LinearRegression()
    model.fit(x_train_scaled, y_train)
    y_pred = model.predict(x_test_scaled)
    print_error_metrics2(y_test, y_pred, True)


import time
for i in range(3, 15):
    time_start = time.time()
    polynomial_regression_create(i)
    print(f"iteration {i} time{time.time()-time_start}")
