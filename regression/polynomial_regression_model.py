from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from regression.regression_prediction import RegressionPrediction


def polynomial_regression_create(x, y, degree=3):
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    x_poly = poly.fit_transform(x)
    x_train, x_test, y_train, y_test = RegressionPrediction.train_test_split(x_poly, y, test_size=0.2, random_state=0)
    scaler = MinMaxScaler()
    x_train_scaled, x_test_scaled = scaler.fit_transform(x_train), scaler.transform(x_test)
    model = LinearRegression()
    model.fit(x_train_scaled, y_train)
    y_pred = model.predict(x_test_scaled)
    RegressionPrediction.print_error_metrics(y_test, y_pred, True, True, title="Полиномиальная регрессия")
