from confluent_kafka import Consumer, KafkaException
import os

# Конфигурация consumer
conf = {
    'bootstrap.servers': 'localhost:45697',  # Адрес Kafka-сервера
    'group.id': 'photo-consumer-group',     # Группа consumer-ов
    'auto.offset.reset': 'earliest'         # Начать с первого сообщения, если нет смещения
}

# Создание экземпляра consumer
consumer = Consumer(conf)

# Подписка на топик "photo"
topic = 'photo'
consumer.subscribe([topic])

# Папка для сохранения изображений
output_dir = 'web'
os.makedirs(output_dir, exist_ok=True)

print(f"Подписан на топик '{topic}'. Ожидание сообщений...")

try:
    while True:
        # Получение сообщения из топика
        msg = consumer.poll(1.0)  # Таймаут 1 секунда

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                print("Достигнут конец партиции.")
            else:
                print(f"Ошибка: {msg.error()}")
            continue

        # Обработка сообщения
        print(f"Получено сообщение с ключом: {msg.key()}")
        file_name = f"{output_dir}/received_image.jpg"

        # Сохранение сообщения в файл
        with open(file_name, 'wb') as f:
            f.write(msg.value())
        
        print(f"Файл сохранён как {file_name}")
        break  # Останавливаем после первого сообщения (для примера)

except KeyboardInterrupt:
    print("\nConsumer остановлен.")

finally:
    # Закрытие consumer
    consumer.close()