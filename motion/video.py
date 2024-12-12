from flask import Flask, jsonify
import cv2
import os
import uuid
import requests

app = Flask(__name__)

# Папка для сохранения фотографий
KNOWN_FACES_DIR = "known_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

UNKNOWN_FACES_DIR = "unknown_faces"
os.makedirs(UNKNOWN_FACES_DIR, exist_ok=True)

@app.route('/capture', methods=['GET'])
def capture_photo():
    try:
        # Открытие веб-камеры
        camera = cv2.VideoCapture(2)
        if not camera.isOpened():
            return jsonify({"error": "Failed to open the webcam."}), 500

        # Захват одного кадра
        ret, frame = camera.read()
        if not ret:
            return jsonify({"error": "Failed to capture an image."}), 500

        # Создание уникального имени файла
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(KNOWN_FACES_DIR, filename)

        # Сохранение изображения
        cv2.imwrite(filepath, frame)

        # Освобождение ресурсов камеры
        camera.release()

        return jsonify({"message": "Photo captured successfully.", "file": filename}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send-photo', methods=['POST'])
def send_photo():
    try:
        # Открытие веб-камеры
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            return jsonify({"error": "Failed to open the webcam."}), 500

        # Захват одного кадра
        ret, frame = camera.read()
        if not ret:
            return jsonify({"error": "Failed to capture an image."}), 500

        # Создание уникального имени файла
        filename = f"unknown.jpg"
        filepath = os.path.join(UNKNOWN_FACES_DIR, filename)

        # Сохранение изображения
        cv2.imwrite(filepath, frame)

        # Освобождение ресурсов камеры
        camera.release()

        # Отправка GET запроса на /process-image
        response = requests.get("http://127.0.0.1:5000/process-image")
        
        if response.status_code == 200:
            return jsonify({"message": "Photo captured and processed successfully.", "file": filename}), 200
        else:
            return jsonify({"error": "Failed to process the image."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5005)