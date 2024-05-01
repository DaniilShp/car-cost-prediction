from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.metrics import r2_score, mean_absolute_error
import pandas as pd
from regression_prediction import RegressionPrediction


def random_forest_regression_create(x, y, forest_n=100):
    x = pd.get_dummies(x)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    model = RandomForestRegressor(n_estimators=forest_n, random_state=0)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    metrics = "max_error", "r2", "neg_mean_absolute_percentage_error", "neg_mean_absolute_error"
    cross_validation_result = cross_validate(model, x, y, scoring=metrics, cv=3)
    print("коэффициент детерминации {0}".format(r2_score(y_test, y_pred)))
    RegressionPrediction.print_error_metrics(y_test, y_pred, barplot=True, scatterplot=True, title="RandomForest")
    return cross_validation_result


if __name__ == '__main__':
    dataframe = pd.read_csv("data/dataframe_audi_cars.csv")
    x, y = (dataframe[["volume", "power", "mileage", "production_year", "gearbox_type", "brand_model"]],
            dataframe["price"])
    cross_validation_result = random_forest_regression_create(x, y)
    print(cross_validation_result)
