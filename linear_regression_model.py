from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sql_data_load import SQLDataLoader
import json

db_table = "toyota_cars"
with open('dbconfig.json') as f:
    dbconfig = json.load(f)

data_loader = SQLDataLoader()
local_path = data_loader.create_dataframe(dbconfig, f"select * from {db_table}", db_table)
dataframe = pd.read_csv(local_path)

dataframe = dataframe.drop(columns=["href", "car_id"], axis=1)

x = dataframe[["production_year", "volume", "power", "mileage", "brand_model", "gearbox_type"]]
y = dataframe["price"]

"""
from matplotlib import pyplot as plt
plt.scatter(x["production_year"], y)
plt.show()
plt.scatter(x["power"], y)
plt.show()
print(x.head(50))
print(y)
"""
x = pd.get_dummies(x, columns=['brand_model', 'gearbox_type'])  # one hot encoding
scaler = MinMaxScaler()
x = scaler.fit_transform(x.select_dtypes(include=['number']))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

model = LinearRegression()
model.fit(x_train, y_train)

predictions = model.predict(x_test)

mae = np.mean(abs(predictions - y_test))
print("Mean Abcolute Error:", mae)

mae = 0
count = 0
for i, val in enumerate(y_test.values):
    accuracy_percent = abs(val - predictions[i]) / val * 100
    if accuracy_percent < 10:
        count += 1
    print(val, predictions[i], round(accuracy_percent))

count = round(count / len(y_test) * 100)
print(f"good predictions percent: {count}")





