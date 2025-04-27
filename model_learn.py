import numpy as np
import pickle
from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import datetime

# # Настройки
# input_len = 60
# output_len = 15
# model_path = "svr_temperature_model.pkl"

# # Синтетические данные: синусоида + шум
# np.random.seed(42)
# data = np.sin(np.linspace(0, 30, 1000)) + np.random.normal(0, 0.1, 1000)

# # Формирование обучающих примеров
# X, y = [], []
# for i in range(len(data) - input_len - output_len):
#     X.append(data[i:i + input_len])
#     y.append(data[i + input_len:i + input_len + output_len])

# X = np.array(X)
# y = np.array(y)

# # Обучение модели
# base_model = make_pipeline(StandardScaler(), SVR(kernel='rbf', C=1.0, epsilon=0.1))
# model = MultiOutputRegressor(base_model)
# model.fit(X, y)

# # Сохранение модели в файл
# with open(model_path, 'wb') as f:
#     pickle.dump(model, f)

# print(f"Модель успешно обучена и сохранена в файл: {model_path}")

# input_len = 60      # длина входного окна (60 минут)
# output_len = 15     # длина выходного окна (предсказываемые минуты)
# model_path = "svr_humidity_model.pkl"  # путь сохранения модели

# # Генерируем синтетический ряд влажности: аналогично температуре,
# # используем периодическую функцию (синусоиду) с добавлением шума
# np.random.seed(42)
# humidity_data = np.sin(np.linspace(0, 30, 1000)) * 30 + 50 + np.random.normal(0, 2, 1000)

# # Формируем обучающие данные
# X, y = [], []
# for i in range(len(humidity_data) - input_len - output_len):
#     X.append(humidity_data[i:i+input_len])  # предыдущие 60 минут влажности
#     y.append(humidity_data[i+input_len:i+input_len+output_len])  # следующие 15 минут влажности

# X = np.array(X)
# y = np.array(y)

# # Строим модель регрессии на основе SVM
# base_model = make_pipeline(StandardScaler(), SVR(kernel='rbf', C=1.0, epsilon=0.1))
# model = MultiOutputRegressor(base_model)

# # Обучаем модель
# model.fit(X, y)

# # Сохраняем модель в файл
# with open(model_path, 'wb') as f:
#     pickle.dump(model, f)

# print(f"Модель успешно обучена и сохранена в файл: {model_path}")

time = 1745710451.211097
print(datetime.datetime.fromtimestamp(time).replace(microsecond=0))
