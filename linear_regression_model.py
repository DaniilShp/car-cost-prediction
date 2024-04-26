from sklearn.linear_model import LinearRegression
import pandas as pd
from regression_prediction import RegressionPrediction

"""
from matplotlib import pyplot as plt
plt.scatter(x["production_year"], y)
plt.show()
plt.scatter(x["power"], y)
plt.show()
print(x.head(50))
print(y)
"""


def linear_regression_create(x, y):
    x = pd.get_dummies(x, columns=['brand_model', 'gearbox_type'])  # one hot encoding
    x = RegressionPrediction.normalize_data(x.select_dtypes(include=['number']))
    x_train, x_test, y_train, y_test = RegressionPrediction.train_test_split(x, y, test_size=0.2, random_state=0)
    model = LinearRegression()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    RegressionPrediction.print_error_metrics(y_test, predictions, barplot=True, scatterplot=True, title="Линейная регрессия")

