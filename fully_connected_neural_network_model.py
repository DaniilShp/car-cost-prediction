from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from regression_prediction import RegressionPrediction


class FullyConnectedNeuralNetwork(RegressionPrediction):
    def __init__(self, input_size: tuple, number_of_neurons=64, optimize_method='adam'):
        self._model = Sequential()
        self._model.add(Dense(number_of_neurons, activation='elu', input_shape=input_size))
        self._model.add(Dense(number_of_neurons / 2, activation='relu', input_shape=input_size))
        self._model.add(Dense(4, activation='relu', input_shape=input_size))
        self._model.add(Dense(1))
        self._model.compile(optimizer=optimize_method, loss='mse', metrics=['mae'])

    def load_model(self, model_filename):
        self._model = load_model(model_filename)
    def fit(self, data, target, epochs=100, batch_size=1, verbose=2, save=False, **kwargs):
        history = self._model.fit(data, target, epochs=epochs, batch_size=batch_size, verbose=verbose)
        if save:
            self._model.save(f'model_{round(history.history["mae"][-1])}.h5')

    def predict(self, data):
        predictions = self._model.predict(data)
        return predictions
