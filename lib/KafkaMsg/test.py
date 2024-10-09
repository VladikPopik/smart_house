import kafka as kf

try: 
    producer = kf.KafkaProducer(bootstrap_servers='kafka:9092')
    consumer = kf.KafkaConsumer('test', bootstrap_servers='kafka:9092')
    def test_producer():
        for i in range(100):
            producer.send('test', b'1')


    def test_consumer():
        for msg in consumer:
            print(f"received {msg}")


except Exception as e:
    def test_producer():
        print("No connection")

    def test_consumer():
        print("No connection")

    
