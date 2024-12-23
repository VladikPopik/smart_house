import os
import base64
import asyncio
from aiokafka import AIOKafkaProducer

async def send_images_to_kafka(folder_path, topic, kafka_bootstrap_servers):
    # Создаем экземпляр Kafka Producer
    producer = AIOKafkaProducer(bootstrap_servers=kafka_bootstrap_servers)
    await producer.start()
    try:
        # Перебираем файлы в указанной папке
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Проверяем, что это файл изображения
            if os.path.isfile(file_path) and filename.lower().endswith((".jpg", ".jpeg", ".png")):
                print(f"[INFO] Отправка файла {filename} в Kafka...")

                # Читаем и кодируем файл в Base64
                with open(file_path, "rb") as image_file:
                    image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

                # Отправляем сообщение в Kafka
                await producer.send_and_wait(topic, image_base64.encode("utf-8"))

                print(f"[INFO] Файл {filename} успешно отправлен в топик {topic}.")
    finally:
        await producer.stop()

if __name__ == "__main__":
    # Параметры Kafka и папки с изображениями
    folder_path = "detected"
    topic = "input_images"
    kafka_bootstrap_servers = "localhost:9092"  # Замените на ваш адрес Kafka

    # Запускаем отправку изображений
    asyncio.run(send_images_to_kafka(folder_path, topic, kafka_bootstrap_servers))
