from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import pandas as pd
from matplotlib import pyplot as plt
from regression_prediction import RegressionPrediction


class FullyConnectedNeuralNetwork(RegressionPrediction):
    def __init__(self, input_size: tuple, number_of_neurons=64, optimize_method='adam'):
        self.model = Sequential()
        self.model.add(Dense(number_of_neurons, activation='elu', input_shape=input_size))
        self.model.add(Dense(number_of_neurons/2, activation='relu', input_shape=input_size))
        self.model.add(Dense(4, activation='relu', input_shape=input_size))
        self.model.add(Dense(1))
        self.model.compile(optimizer=optimize_method, loss='mse', metrics=['mae'])

    @staticmethod
    def normalize_data(data):
        scaler = MinMaxScaler()
        data = scaler.fit_transform(data)
        return data
    @staticmethod
    def load_model(model_filename):
        return load_model(model_filename)
    def fit(self, data, target, epochs=100, batch_size=1, verbose=2, save=False, **kwargs):
        history = self.model.fit(data, target, epochs=epochs, batch_size=batch_size, verbose=verbose)
        if save:
            self.model.save(f'model_{round(history.history["mae"][-1])}.h5')

    def predict(self, data):
        predictions = self.model.predict(data)
        return predictions



"""dataframe = pd.read_csv("data/dataframe_toyota_cars.csv")
x = dataframe[["volume", "power", "mileage", "production_year"]]
y = dataframe["price"]
model = FullyConnectedNeuralNetwork(input_size=(x.shape[1],))
x_train, x_test, y_train, y_test = model.train_test_split(x, y, test_size=0.2, random_state=0)
x_train = model.normalize_data(x_train)
x_test = model.normalize_data(x_test)
try:
    model.model = load_model('model_428928.h5')
    print("model has been loaded successfully")
except FileNotFoundError:
    pass
except OSError:
    pass
'''history = model.model.fit(x_train, y_train, epochs=500, batch_size=1)
model.model.save(f'model_{round(history.history["mae"][-1])}.h5')'''
y_pred = model.predict(x_train)
print_error_metrics(y_train, y_pred, barplot=True)
'''for val_test, val_pred in zip(y_test, y_pred):
    print(val_test, val_pred)'''"""


