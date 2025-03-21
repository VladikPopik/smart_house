import asyncio
from aiokafka import AIOKafkaConsumer
from PIL import Image
import base64
from io import BytesIO

# Настройки Kafka
KAFKA_BROKER = "localhost:9092"  # Адрес Kafka брокера
KAFKA_TOPIC = "predicted_images"  # Тема, из которой будем получать изображения

# Функция для обработки изображения из base64
def process_image(base64_str: str):
    try:
        # Декодируем строку base64 в байты
        img_data = base64.b64decode(base64_str)
        # Открываем изображение из байтов
        image = Image.open(BytesIO(img_data))
        # Показать изображение
        image.show()
    except Exception as e:
        print(f"Error processing image: {e}")

# Асинхронный потребитель Kafka
async def consume_images():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
    )

    # Подключаемся к Kafka
    await consumer.start()
    try:
        async for msg in consumer:
            # Сообщение должно содержать base64 строку изображения
            base64_str = msg.value.decode('utf-8')
            print(f"Received message: {base64_str[:50]}...")  # Покажем первые 50 символов
            process_image(base64_str)  # Обрабатываем изображение
    finally:
        await consumer.stop()

# Запускаем потребителя с использованием asyncio.run()
async def main():
    await consume_images()

# Запуск основного процесса
if __name__ == "__main__":
    asyncio.run(main())
