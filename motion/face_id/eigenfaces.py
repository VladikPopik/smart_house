import os
import cv2
import numpy as np
import argparse
from imutils import paths
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump, load

def load_dataset_from_directory(base_path, net, min_confidence):
    faces = []
    labels = []
    image_paths = []  # Добавляем список путей изображений для отслеживания изменений

    for person_name in os.listdir(base_path):
        person_path = os.path.join(base_path, person_name)
        if not os.path.isdir(person_path):
            continue

        for image_path in paths.list_images(person_path):
            image_paths.append(image_path)  # Добавляем путь изображения в список
            image = cv2.imread(image_path)
            h, w = image.shape[:2]

            blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
            net.setInput(blob)
            detections = net.forward()

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > min_confidence:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    face = image[startY:endY, startX:endX]

                    if face.shape[0] > 0 and face.shape[1] > 0:
                        gray_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                        resized_face = cv2.resize(gray_face, (50, 50))
                        faces.append(resized_face.flatten())
                        labels.append(person_name)

    return np.array(faces), labels, image_paths


# Парсер аргументов
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="caltech_faces",
                help="Путь к директории с обучающими изображениями (подпапки = имена людей)")
ap.add_argument("-f", "--face", type=str, default="face_detector",
                help="Путь к модели детектора лиц")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="Минимальная вероятность для фильтрации слабых детекций")
ap.add_argument("-n", "--num-components", type=int, default=150,
                help="Количество главных компонент PCA")
ap.add_argument("-m", "--model", type=str, default="output/model.joblib",
                help="Путь для сохранения/загрузки модели и PCA")
ap.add_argument("-d", "--detected", type=str, default="detected",
                help="Путь к директории с изображениями для предсказания")
args = vars(ap.parse_args())

pca_path = args["model"].replace(".joblib", "_pca.joblib")
labels_path = args["model"].replace(".joblib", "_labels.joblib")
model_path = args["model"]

# Загружаем модель детектора лиц
print("[INFO] Загрузка модели детектора лиц...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"], "res10_300x300_ssd_iter_140000.caffemodel"])
net = cv2.dnn.readNet(prototxtPath, weightsPath)

# Проверяем, существует ли модель, PCA и LabelEncoder
if os.path.exists(model_path) and os.path.exists(pca_path) and os.path.exists(labels_path):
    print("[INFO] Загрузка обученной модели, PCA и LabelEncoder...")
    model = load(model_path)
    pca = load(pca_path)
    le = load(labels_path)
    print("[INFO] Проверка новых данных...")
    
    # Загружаем старые данные и метки
    (old_faces, old_labels, old_image_paths) = load_dataset_from_directory(args["input"], net, min_confidence=args["confidence"])
    old_labels_encoded = le.transform(old_labels)
    
    # Загружаем новые данные (если есть)
    new_faces, new_labels, new_image_paths = load_dataset_from_directory(args["input"], net, min_confidence=args["confidence"])
    new_labels_encoded = le.transform(new_labels)  # Преобразуем метки для новых данных

    # Проверка на удаление файлов
    deleted_files = list(set(old_image_paths) - set(new_image_paths))
    if deleted_files:
        print(f"[INFO] Обнаружены удаленные файлы: {len(deleted_files)}")
    else:
        print("[INFO] Удаленных данных не найдено.")

    # Смотрим, если есть новые изображения, добавляем их
    if len(new_faces) > len(old_faces):
        print(f"[INFO] Обнаружено {len(new_faces) - len(old_faces)} новых изображений.")

        # Сливаем старые и новые данные
        all_faces = np.concatenate((old_faces, new_faces), axis=0)
        all_labels_encoded = np.concatenate((old_labels_encoded, new_labels_encoded), axis=0)

        # Обновляем PCA
        print("[INFO] Обучение PCA на новых данных...")
        pca = PCA(n_components=args["num_components"], whiten=True, svd_solver="randomized")
        all_faces_pca = pca.fit_transform(all_faces)

        # Обновляем модель SVM
        print("[INFO] Обучение SVM на новых данных...")
        model = SVC(kernel="rbf", C=10.0, gamma=0.001, random_state=42)
        model.fit(all_faces_pca, all_labels_encoded)

        # Сохраняем обновленную модель, PCA и LabelEncoder
        print("[INFO] Сохранение обновленных модели, PCA и LabelEncoder...")
        dump(model, model_path)
        dump(pca, pca_path)
        dump(le, labels_path)
    else:
        print("[INFO] Новых данных не найдено.")

else:
    print("[INFO] Обучение новой модели...")
    (faces, labels, image_paths) = load_dataset_from_directory(args["input"], net, min_confidence=args["confidence"])

    if len(faces) == 0 or len(labels) == 0:
        raise ValueError("[ERROR] Не удалось загрузить данные. Проверьте путь и содержимое папки.")

    print(f"[INFO] {len(faces)} изображений загружено.")
    le = LabelEncoder()
    labels_encoded = le.fit_transform(labels)

    trainX, testX, trainY, testY = train_test_split(faces, labels_encoded, test_size=0.25, stratify=labels_encoded, random_state=42)
    print("[INFO] Обучение PCA...")
    # Проверяем, чтобы n_components не превышало ограничения
    n_components = min(args["num_components"], trainX.shape[0], trainX.shape[1])
    print(f"[INFO] Установлено n_components={n_components} для PCA.")

    # Инициализация PCA с обновленным количеством компонентов
    pca = PCA(n_components=n_components, whiten=True, svd_solver="randomized")
    trainX_pca = pca.fit_transform(trainX)

    print("[INFO] Обучение SVM...")
    model = SVC(kernel="rbf", C=10.0, gamma=0.001, random_state=42)
    model.fit(trainX_pca, trainY)

    print("[INFO] Сохранение модели, PCA и LabelEncoder...")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    dump(model, model_path)
    dump(pca, pca_path)
    dump(le, labels_path)

# Оценка модели
print("[INFO] Оценка модели...")
if 'testX' not in locals():  # Проверяем, определены ли переменные для тестирования
    print("[INFO] Разделение данных на обучающую и тестовую выборки...")
    (faces, labels, _) = load_dataset_from_directory(args["input"], net, min_confidence=args["confidence"])
    labels_encoded = le.fit_transform(labels)
    trainX, testX, trainY, testY = train_test_split(faces, labels_encoded, test_size=0.25, stratify=labels_encoded, random_state=42)

testX_pca = pca.transform(testX)  # Здесь уже используется testX
predictions = model.predict(testX_pca)
print(classification_report(testY, predictions, target_names=le.classes_))

# Обработка изображений для предсказания
print("[INFO] Обработка изображений для предсказания...")
detected_faces = []
original_images = []
for imagePath in paths.list_images(args["detected"]):
    image = cv2.imread(imagePath)
    h, w = image.shape[:2]
    original_images.append(image.copy())

    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > args["confidence"]:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            face = image[startY:endY, startX:endX]

            gray_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            face_resized = cv2.resize(gray_face, (50, 50)).flatten()
            detected_faces.append((face_resized, (startX, startY, endX, endY)))

for (face, (startX, startY, endX, endY)), image in zip(detected_faces, original_images):
    # Преобразуем лицо и выполняем предсказание
    face_pca = pca.transform([face])
    label_idx = model.predict(face_pca)

    # Если предсказание неудачное или не соответствует базе данных, то помечаем как "Unknown"
    if label_idx.size == 0:
        label = "Unknown"
        color = (0, 0, 255)  # Красный цвет для "Unknown"
    else:
        label = le.inverse_transform(label_idx)[0]
        color = (0, 255, 0)  # Зеленый цвет для распознанного лица

    # Отображаем прямоугольник вокруг лица и подпись
    cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
    cv2.putText(image, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Сохраняем и показываем изображение
    cv2.imshow("Prediction", image)
    output_path = os.path.join('predicted', f'predicted_face_{startX}_{startY}.jpg')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, image)
    cv2.waitKey(0)

cv2.destroyAllWindows()
