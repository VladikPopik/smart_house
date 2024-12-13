from confluent_kafka import Producer
import os

# Функция обратного вызова для проверки успешности отправки сообщения
def delivery_report(err, msg):
    if err is not None:
        print(f"Ошибка при отправке сообщения: {err}")
    else:
        print(f"Сообщение отправлено в {msg.topic()} с оффсетом {msg.offset()}")

# Конфигурация продюсера
conf = {
    'bootstrap.servers': 'localhost:45697',  # Адрес вашего Kafka сервера
    'client.id': 'photo-producer'
}

# Создание экземпляра продюсера
producer = Producer(conf)

# Путь к вашему файлу .jpg
file_path = "./detected/processed_image.jpg"

# Чтение файла и отправка его как байтов
with open(file_path, 'rb') as file:
    image_data = file.read()

# Отправка сообщения в топик 'photo' с изображением
producer.produce('photo', key='image_key', value=image_data, callback=delivery_report)

# Принудительная отправка всех сообщений
producer.flush()

print("Изображение отправлено в Kafka.")