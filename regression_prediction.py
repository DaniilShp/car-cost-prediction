from abc import abstractmethod
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


class RegressionPrediction:
    @abstractmethod
    def fit(self, data, target, **kwargs):
        pass

    @abstractmethod
    def predict(self, data):
        pass

    @staticmethod
    def normalize_data(data):
        scaler = MinMaxScaler()
        data = scaler.fit_transform(data)
        return data

    @staticmethod
    def train_test_split(x, y, test_size=0.2, random_state=0, **kwargs):
        return train_test_split(x, y, test_size=test_size, random_state=random_state, **kwargs)

    @staticmethod
    def print_error_metrics(y, y_pred, barplot=False, scatterplot=False, title=""):
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
            RegressionPrediction.show_bars_with_accuracies(accuracies, title)
        if scatterplot:
            RegressionPrediction.show_scatterplot_with_accuracies(accuracies, title)

    @staticmethod
    def show_bars_with_accuracies(_accuracies: list[int, float], title):
        intervals = [i for i in range(0, 100, 10)]
        interval_values = [0] * len(intervals)

        for val in _accuracies:
            i = int(val // 10)
            if i < 0 or i > len(intervals) - 1:
                continue
            interval_values[i] += 1
        interval_values = [((val * 100) // len(_accuracies)) for val in interval_values]
        plt.bar([f'{i}-{i + 10}%' for i in intervals], interval_values)
        plt.xlabel('Диапазон относительных погрешностей')
        plt.ylabel('Процент ошибок')
        plt.title(f'{title}\nСтолбчатая диаграмма распределения относительных погрешностей')
        plt.show()

    @staticmethod
    def show_scatterplot_with_accuracies(_accuracies: list[int, float], title):
        plt.scatter(range(len(_accuracies)), _accuracies, c=[el/100 for el in _accuracies], cmap='RdYlGn_r')
        plt.xlabel('индекс предсказания')
        plt.ylabel('относительная погрешность, %')
        plt.title(f'{title}\nраспределение относительных погрешностей')
        plt.colorbar()
        plt.show()
