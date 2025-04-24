import os
import time
import cv2
import joblib
import numpy as np
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем необходимые директории
os.makedirs("registered", exist_ok=True)
os.makedirs("auth", exist_ok=True)
os.makedirs("debug", exist_ok=True)

# Монтирование статических файлов
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")
app.mount("/static/auth", StaticFiles(directory="auth"), name="auth_photos")
app.mount("/static/registered", StaticFiles(directory="registered"), name="registered_photos")
app.mount("/static/debug", StaticFiles(directory="debug"), name="debug_photos")

# Загрузка модели и артефактов
try:
    model = joblib.load("output/face_recognition_model.pkl")
    print("\n" + "="*50)
    print("Модель успешно загружена")
    
    # Извлекаем компоненты из pipeline
    scaler = model.named_steps['standardscaler']
    pca = model.named_steps['pca']
    svm = model.named_steps['svc']
    
    print(f"Классификатор: {svm.__class__.__name__}")
    print(f"Количество компонент PCA: {pca.n_components_}")
    
except Exception as e:
    print(f"Ошибка загрузки модели: {e}")
    model = scaler = pca = svm = None

# Загрузка label_map
try:
    with open('output/label_map.pkl', 'rb') as f:
        label_map = joblib.load(f)
    print(f"Загружено классов: {len(label_map)}")
    print("Пример label_map:", {k: v for k, v in list(label_map.items())[:3]})
    print("="*50 + "\n")
except Exception as e:
    print(f"Ошибка загрузки label map: {e}")
    label_map = {}

# Загрузка модели детекции лиц
try:
    detector = cv2.dnn.readNetFromCaffe(
        "face_detector/deploy.prototxt",
        "face_detector/res10_300x300_ssd_iter_140000.caffemodel"
    )
    print("Детектор лиц успешно загружен")
except Exception as e:
    print(f"Ошибка загрузки детектора лиц: {e}")
    detector = None

def extract_hog_features(image):
    """Извлечение HOG-признаков"""
    winSize = (100, 100)
    blockSize = (50, 50)
    blockStride = (25, 25)
    cellSize = (25, 25)
    nbins = 9
    
    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    features = hog.compute(image)
    return features.flatten()

def preprocess_face(face_img):
    """Предварительная обработка лица для классификации"""
    try:
        # Конвертация в grayscale и улучшение контраста
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        
        # Изменение размера и извлечение признаков
        resized = cv2.resize(gray, (100, 100))
        hog_features = extract_hog_features(resized)
        pixel_features = resized.flatten()
        combined_features = np.hstack([pixel_features, hog_features])
        
        return combined_features
    except Exception as e:
        print(f"Ошибка предварительной обработки: {e}")
        return None

def detect_face(image, confidence_threshold=0.5):
    """Обнаружение лица на изображении"""
    if detector is None:
        return None
    
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 
        1.0, 
        (300, 300),
        (104.0, 177.0, 123.0)
    )
    
    detector.setInput(blob)
    detections = detector.forward()
    
    best_face = None
    best_confidence = 0
    
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > best_confidence:
            best_confidence = confidence
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            
            # Корректировка границ
            startX, startY = max(0, startX), max(0, startY)
            endX, endY = min(w - 1, endX), min(h - 1, endY)
            
            if endX > startX and endY > startY and confidence > confidence_threshold:
                best_face = image[startY:endY, startX:endX]
    
    return best_face

def capture_face():
    """Захват лица с камеры"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось открыть камеру")
        return None
    
    try:
        time.sleep(0.1)  # Даем камере время на инициализацию
        ret, frame = cap.read()
        if not ret:
            print("Не удалось захватить кадр")
            return None
            
        # Поворот изображения (если камера перевернута)
        # frame = cv2.rotate(frame, cv2.ROTATE_180)
        
        # Обнаружение лица
        face = detect_face(frame)
        return face
    finally:
        cap.release()

@app.get("/")
async def serve_html():
    """Отдача HTML-интерфейса"""
    with open("frontend/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/face")
def handle_face(command: str = Query(...), login: str = Query(None)):
    """Обработка запросов распознавания/регистрации"""
    if command == "auth":
        response = authenticate_user()
        print("Auth response:", response.body.decode())
        return response
    elif command == "register":
        if login is None:
            return JSONResponse({"status": "error", "reason": "Login is required for registration"})
        return register_user(login)
    else:
        return JSONResponse({"status": "error", "reason": "Unknown command"})

def register_user(login: str):
    """Регистрация нового пользователя"""
    face_img = capture_face()
    if face_img is None:
        return JSONResponse({"status": "error", "reason": "Face not detected"})

    user_dir = os.path.join("registered", login)
    os.makedirs(user_dir, exist_ok=True)
    
    timestamp = str(int(time.time()))
    filename = f"{timestamp}.png"
    path = os.path.join(user_dir, filename)
    cv2.imwrite(path, face_img)
    
    return JSONResponse({
        "status": "success",
        "saved_to": path,
        "photo_url": f"/static/registered/{login}/{filename}"
    })

def get_most_similar_face(auth_features, login):
    """Поиск наиболее похожего лица среди зарегистрированных"""
    user_dir = os.path.join("registered", login)
    if not os.path.exists(user_dir):
        return None, 0
    
    max_similarity = 0
    best_match = None
    
    for filename in os.listdir(user_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(user_dir, filename)
            registered_img = cv2.imread(img_path)
            
            if registered_img is not None:
                try:
                    # Извлекаем признаки зарегистрированного лица
                    registered_features = preprocess_face(registered_img)
                    if registered_features is None:
                        continue
                        
                    # Масштабируем и преобразуем признаки
                    registered_scaled = scaler.transform(registered_features.reshape(1, -1))
                    registered_pca = pca.transform(registered_scaled)
                    
                    # Вычисляем косинусное сходство
                    similarity = cosine_similarity(auth_features, registered_pca)[0][0]
                    
                    if similarity > max_similarity:
                        max_similarity = similarity
                        best_match = {
                            "filename": filename,
                            "photo_url": f"/static/registered/{login}/{filename}",
                            "similarity": float(similarity)
                        }
                except Exception as e:
                    print(f"Ошибка обработки {filename}: {e}")
    
    return best_match, max_similarity

def authenticate_user():
    """Аутентификация с проверкой схожести с фото из папки registered"""
    if model is None:
        return JSONResponse({"status": "error", "reason": "Model not loaded"})

    # Захватываем лицо для аутентификации
    auth_face = capture_face()
    if auth_face is None:
        return JSONResponse({"status": "error", "reason": "Face not detected"})

    # Сохраняем фото аутентификации
    auth_timestamp = str(int(time.time()))
    auth_filename = f"auth_{auth_timestamp}.png"
    auth_path = os.path.join("auth", auth_filename)
    cv2.imwrite(auth_path, auth_face)
    auth_photo_url = f"/static/auth/{auth_filename}"

    # Обрабатываем лицо
    auth_features = preprocess_face(auth_face)
    if auth_features is None:
        return JSONResponse({"status": "error", "reason": "Face processing failed"})

    try:
        # Преобразуем признаки аутентифицируемого лица
        auth_scaled = scaler.transform(auth_features.reshape(1, -1))
        auth_pca = pca.transform(auth_scaled)
        
        # Получаем список всех зарегистрированных пользователей
        registered_users = [d for d in os.listdir("registered") 
                          if os.path.isdir(os.path.join("registered", d))]
        
        if not registered_users:
            return JSONResponse({"status": "error", "reason": "No registered users found"})
        
        # Сравниваем с каждым зарегистрированным пользователем
        best_match = None
        best_similarity = 0
        best_user = None
        
        for user in registered_users:
            user_dir = os.path.join("registered", user)
            
            # Ищем самое похожее фото пользователя
            for filename in os.listdir(user_dir):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(user_dir, filename)
                    registered_img = cv2.imread(img_path)
                    
                    if registered_img is not None:
                        try:
                            # Извлекаем признаки зарегистрированного лица
                            registered_features = preprocess_face(registered_img)
                            if registered_features is None:
                                continue
                                
                            # Масштабируем и преобразуем признаки
                            registered_scaled = scaler.transform(registered_features.reshape(1, -1))
                            registered_pca = pca.transform(registered_scaled)
                            
                            # Вычисляем косинусное сходство
                            similarity = cosine_similarity(auth_pca, registered_pca)[0][0]
                            
                            if similarity > best_similarity:
                                best_similarity = similarity
                                best_user = user
                                best_match = {
                                    "filename": filename,
                                    "photo_url": f"/static/registered/{user}/{filename}",
                                    "similarity": float(similarity)
                                }
                        except Exception as e:
                            print(f"Ошибка обработки {filename}: {e}")
        
        if best_user is None:
            return JSONResponse({"status": "error", "reason": "No matching faces found"})
        
        # Формируем ответ
        response = {
            "status": "success",
            "auth_photo": auth_photo_url,
            "matched_user": best_user,
            "similarity": {
                "score": round(float(best_similarity) * 100, 2),
                "best_match": best_match
            }
        }
        
        return JSONResponse(response)
        
    except Exception as e:
        return JSONResponse({"status": "error", "reason": str(e)})

if __name__ == "__main__":
    import uvicorn
    print("\nFace Recognition API готов к работе")
    uvicorn.run(app, host="0.0.0.0", port=8000)