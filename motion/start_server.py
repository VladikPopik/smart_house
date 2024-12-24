import os
import asyncio
from kafka_functions import produce_result, consume_message
from logging import getLogger, basicConfig, INFO
import httpx
import datetime


from sklearn.preprocessing import LabelEncoder
from joblib import load
import numpy as np
import cv2


basicConfig(filename="motion.log", level=INFO)
log = getLogger(__name__)

MODEL_PATH = "face_id/output/model.joblib"
PCA_PATH = "face_id/output/model_pca.joblib"
LABELS_PATH = "face_id/output/model_labels.joblib"
PREDICTED_FOLDER = "face_id/predicted"
KAFKA_BROKER = "kafka:9092"

async def process_message(message):
    try:
        # Декодирование изображения из Base64
        # image_data = base64.b64decode(message.value)
        # image_array = np.frombuffer(image_data, dtype=np.uint8)
        message_key = next(iter(message))
        message = message[message_key]
        image_array = np.array(message, dtype=np.uint8)
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

        return {"image": image.tolist()}

    except Exception as e:
        print(f"[ERROR] Ошибка обработки сообщения: {e}")
        return None


async def get_cam(timeout: int=5000) -> httpx.Response:
    try:
        async with httpx.AsyncClient(timeout=5000) as client:
            response = await client.get(
                "http://backend:8001/settings/device/type/cam",
                params={"device_type": "cam"}
            )
        if response and response.is_success:
            return response
    except Exception as e:
        log.exception(e)
        await asyncio.sleep(5)
        await get_cam(timeout)

async def main(time_to_cycle=5):
    start = datetime.datetime.now().timestamp()
    to_consume = False
    try:
        response = await get_cam(time_to_cycle)

        if response.is_success and response.json():
            r = response.json()
            if r and r["on"]:
                producer_topic = f"{r['device_name']}-{r['device_type']}"
                consumer_topic = producer_topic + "-rasp"
                log.info(f"{producer_topic}, {consumer_topic}")
                to_consume = True
            else:
                log.info(f"{r}")
    except Exception as e:
        log.error(e)
        raise httpx.NetworkError(f"{e}")

    try:
        if to_consume:
            data = await consume_message(consumer_topic)
            predicted = await process_message(data)
            log.info("Predicted is ok")
            if predicted:
                await produce_result(producer_topic, predicted, compression_type="gzip")
    except Exception as e:
        log.error(e)

    end = datetime.datetime.now().timestamp()
    if end - start <= time_to_cycle:
        await asyncio.sleep(time_to_cycle - (end - start))

    log.info(f"Cycle elapsed after: {end - start} sec.")


    asyncio.get_running_loop().create_task(main(time_to_cycle))

if __name__=="__main__":
    _loop = asyncio.new_event_loop()

    log.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@START UP@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    model = load(MODEL_PATH)
    pca = load(PCA_PATH)

    if os.path.exists(LABELS_PATH):
        le = load(LABELS_PATH)
    else:
        print("[WARNING] Файл меток не найден. LabelEncoder будет инициализирован пустым.")
        le = LabelEncoder()

    prototxtPath = os.path.sep.join(["face_id", "face_detector", "deploy.prototxt"])
    weightsPath = os.path.sep.join(["face_id", "face_detector", "res10_300x300_ssd_iter_140000.caffemodel"])
    net = cv2.dnn.readNet(prototxtPath, weightsPath)

    time_to_cycle = 10

    _loop.create_task(main(time_to_cycle))

    _loop.run_forever()
