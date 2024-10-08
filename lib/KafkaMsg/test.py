import kafka as kf


producer = kf.KafkaProducer(bootstrap_servers="kafka:9092")
def test_producer():
    for i in range(100):
        producer.send("test", b"1")


consumer = kf.KafkaConsumer("test", bootstrap_servers="kafka:9092")
def test_consumer():
    for msg in consumer:
        print(msg)

