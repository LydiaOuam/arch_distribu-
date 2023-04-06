import json
from kafka import KafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "aylien_news"

# Initialize Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# Consume messages from Kafka topic
for message in consumer:
    if message is not None and message.value is not None:
        try:
            data = json.loads(message.value)
            print(data)
        except json.decoder.JSONDecodeError:
            print("Invalid JSON format")
    else:
        print("Received empty message")

    # Do something with the received message

# Fermer le consommateur Kafka
consumer.close()


