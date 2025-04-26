import os
import cv2
import numpy as np
import joblib
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import NearestNeighbors
import warnings

# Отключаем предупреждения
warnings.filterwarnings("ignore")

# Пути и параметры
dataset_path = "caltech_faces"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
min_samples_per_class = 5  # Минимальное количество образцов для класса

def extract_hog_features(image):
    """Извлечение признаков HOG"""
    winSize = (100, 100)
    blockSize = (50, 50)
    blockStride = (25, 25)
    cellSize = (25, 25)
    nbins = 9
    
    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    features = hog.compute(image)
    return features.flatten()

def extract_features(image):
    """Извлечение признаков"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    resized = cv2.resize(gray, (100, 100))
    
    # Комбинируем HOG и raw pixels
    hog_features = extract_hog_features(resized)
    pixel_features = resized.flatten()
    return np.concatenate([pixel_features, hog_features])

def load_and_preprocess_data(dataset_path):
    """Загрузка данных с фильтрацией малых классов"""
    faces = []
    labels = []
    label_map = {}
    class_counts = {}
    
    print("[INFO] Загрузка изображений...")
    
    label = 0
    for person_name in sorted(os.listdir(dataset_path)):
        person_dir = os.path.join(dataset_path, person_name)
        if os.path.isdir(person_dir):
            samples = []
            for img_name in os.listdir(person_dir):
                img_path = os.path.join(person_dir, img_name)
                img = cv2.imread(img_path)
                if img is not None:
                    features = extract_features(img)
                    samples.append(features)
            
            # Пропускаем классы с недостаточным количеством образцов
            if len(samples) >= min_samples_per_class:
                faces.extend(samples)
                labels.extend([label] * len(samples))
                label_map[label] = person_name
                class_counts[person_name] = len(samples)
                label += 1
            else:
                print(f"[WARNING] Пропуск класса {person_name} - только {len(samples)} образцов")
    
    print("\n[INFO] Распределение классов:")
    for name, count in class_counts.items():
        print(f"{name}: {count} образцов")
    
    return np.array(faces), np.array(labels), label_map

def balanced_train_test_split(X, y, test_size=0.2):
    """Стратифицированное разделение с защитой от малых классов"""
    unique_classes = np.unique(y)
    X_train, y_train = [], []
    X_test, y_test = [], []
    
    for class_label in unique_classes:
        class_indices = np.where(y == class_label)[0]
        np.random.shuffle(class_indices)
        
        split_idx = max(1, int(len(class_indices) * (1 - test_size)))
        
        # Всегда оставляем хотя бы 1 образец в тестовой выборке
        if len(class_indices) > split_idx + 1:
            X_train.append(X[class_indices[:split_idx]])
            X_test.append(X[class_indices[split_idx:]])
            y_train.append(y[class_indices[:split_idx]])
            y_test.append(y[class_indices[split_idx:]])
        else:
            # Для очень малых классов (меньше 5 образцов)
            # добавляем все в тренировочный набор, а один образец дублируем в тестовый
            X_train.append(X[class_indices])
            y_train.append(y[class_indices])
            
            # Добавляем последний образец в тестовую выборку
            X_test.append(X[class_indices[-1:]])
            y_test.append(y[class_indices[-1:]])
    
    # Проверяем, что тестовая выборка не пустая
    if len(X_test) == 0:
        # Если все классы слишком маленькие, берем случайные образцы
        test_indices = np.random.choice(len(X), size=int(len(X)*test_size), replace=False)
        train_indices = np.setdiff1d(np.arange(len(X)), test_indices)
        return X[train_indices], X[test_indices], y[train_indices], y[test_indices]
    
    return (
        np.concatenate(X_train) if len(X_train) > 0 else np.array([]),
        np.concatenate(X_test) if len(X_test) > 0 else np.array([]),
        np.concatenate(y_train) if len(y_train) > 0 else np.array([]),
        np.concatenate(y_test) if len(y_test) > 0 else np.array([])
    )

def train_model(X, y):
    """Обучение модели с улучшенной обработкой малых классов"""
    print("\n[INFO] Обучение модели...")
    
    # Проверяем количество образцов на класс
    unique_classes, counts = np.unique(y, return_counts=True)
    min_samples = counts.min()
    
    # Упрощаем модель если мало образцов
    if min_samples < 5:
        print("[WARNING] Обнаружены классы с <5 образцами - упрощаем модель")
        pipeline = make_pipeline(
            StandardScaler(),
            PCA(n_components=0.8),  # Еще меньше компонент
            SVC(kernel='linear', C=1, probability=True, random_state=42)
        )
        param_grid = {}
    else:
        pipeline = make_pipeline(
            StandardScaler(),
            PCA(n_components=0.95),
            SVC(kernel='rbf', probability=True, random_state=42)
        )
        param_grid = {
            'svc__C': [0.1, 1, 10],
            'svc__gamma': ['scale', 0.01]
        }
    
    # Разделение данных с учетом малых классов
    X_train, X_test, y_train, y_test = balanced_train_test_split(X, y)
    
    # Проверка на пустые выборки
    if len(X_train) == 0 or len(X_test) == 0:
        raise ValueError("Не удалось создать валидные train/test выборки. Проверьте данные.")
    
    # Обучение
    grid = GridSearchCV(
        pipeline, 
        param_grid, 
        cv=min(3, min_samples), 
        n_jobs=-1, 
        verbose=1,
        error_score='raise'
    )
    
    try:
        grid.fit(X_train, y_train)
    except Exception as e:
        print(f"\n[ERROR] Ошибка при обучении: {str(e)}")
        print("Попробуйте:")
        print("1. Увеличить количество образцов (минимум 5 на класс)")
        print("2. Уменьшить размерность PCA (n_components=0.8)")
        print("3. Использовать более простую модель (kernel='linear')")
        raise
    
    # Оценка
    print("\n[INFO] Отчет по классификации:")
    y_pred = grid.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    return grid.best_estimator_

def save_artifacts(model, label_map):
    """Сохранение модели и метаданных"""
    print("\n[INFO] Сохранение артефактов...")
    joblib.dump(model, os.path.join(output_dir, 'face_recognition_model.pkl'))
    joblib.dump(label_map, os.path.join(output_dir, 'label_map.pkl'))
    print("[SUCCESS] Модель успешно сохранена в папку output")

if __name__ == "__main__":
    try:
        X, y, label_map = load_and_preprocess_data(dataset_path)
        
        if len(np.unique(y)) < 2:
            raise ValueError("Недостаточно классов для обучения (минимум 2)")
        
        model = train_model(X, y)
        save_artifacts(model, label_map)
    except Exception as e:
        print(f"\n[ERROR] Ошибка при обучении модели: {str(e)}")
        print("Проверьте:")
        print("1. Наличие изображений в папке caltech_faces")
        print("2. Каждый класс должен содержать минимум 5 изображений")
        print("3. Изображения должны быть в формате JPG/PNG")