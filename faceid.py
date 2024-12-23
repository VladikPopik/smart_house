from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from joblib import load, dump
import numpy as np
import cv2
import os
import base64
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio

# Параметры
MODEL_PATH = "output/model.joblib"
PCA_PATH = "output/model_pca.joblib"
LABELS_PATH = "output/model_labels.joblib"
PREDICTED_FOLDER = "predicted"
KAFKA_BROKER = "localhost:9092"
INPUT_TOPIC = "input_images"
OUTPUT_TOPIC = "predicted_images"

# Загрузка модели, PCA и LabelEncoder
print("[INFO] Загрузка модели, PCA и LabelEncoder...")
model = load(MODEL_PATH)
pca = load(PCA_PATH)

if os.path.exists(LABELS_PATH):
    le = load(LABELS_PATH)
else:
    print("[WARNING] Файл меток не найден. LabelEncoder будет инициализирован пустым.")
    le = LabelEncoder()

# Загрузка модели обнаружения лиц
prototxtPath = os.path.sep.join(["face_detector", "deploy.prototxt"])
weightsPath = os.path.sep.join(["face_detector", "res10_300x300_ssd_iter_140000.caffemodel"])
net = cv2.dnn.readNet(prototxtPath, weightsPath)

async def process_message(message):
    try:
        # Декодирование изображения из Base64
        image_data = base64.b64decode(message.value)
        image_array = np.frombuffer(image_data, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        h, w = image.shape[:2]

        # Обработка изображения для предсказания
        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        detected_faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                face = image[startY:endY, startX:endX]
                gray_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face_resized = cv2.resize(gray_face, (50, 50)).flatten()
                detected_faces.append((face_resized, (startX, startY, endX, endY)))

        for (face, (startX, startY, endX, endY)) in detected_faces:
            # Преобразование лица и предсказание
            face_pca = pca.transform([face])
            label_idx = model.predict(face_pca)

            # Проверка на обученность LabelEncoder
            if hasattr(le, "classes_"):
                label = le.inverse_transform(label_idx)[0]
            else:
                label = "Unknown"

            color = (0, 255, 0) if label != "Unknown" else (0, 0, 255)

            # Отображение прямоугольника и метки на изображении
            cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
            cv2.putText(image, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # Сохранение предсказанного изображения
        os.makedirs(PREDICTED_FOLDER, exist_ok=True)
        output_path = os.path.join(PREDICTED_FOLDER, f"predicted_{message.offset}.jpg")
        cv2.imwrite(output_path, image)

        # Кодирование результата обратно в Base64
        _, buffer = cv2.imencode('.jpg', image)
        result_base64 = base64.b64encode(buffer).decode('utf-8')

        return result_base64

    except Exception as e:
        print(f"[ERROR] Ошибка обработки сообщения: {e}")
        return None

async def consume_and_process():
    consumer = AIOKafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id="image_processor"
    )
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)

    await consumer.start()
    await producer.start()
    try:
        async for message in consumer:
            print(f"[INFO] Получено сообщение с offset {message.offset}")
            result_base64 = await process_message(message)

            if result_base64:
                await producer.send_and_wait(OUTPUT_TOPIC, result_base64.encode('utf-8'))
                print(f"[INFO] Результат отправлен в топик {OUTPUT_TOPIC}")
            else:
                print("[WARNING] Результат не отправлен из-за ошибки обработки.")
    finally:
        await consumer.stop()
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(consume_and_process())
