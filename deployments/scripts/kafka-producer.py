from kafka import KafkaProducer


def publish_message(producer_instance, topic_name, key, value):
    try:
        print("b")
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        print("c")
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        print("d")
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['192.168.0.100:19092'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

if __name__ == '__main__':
    all_recipes = ["aaaaa", "bbbbbb", "ccccccc", "dexi", "eeeeeeee"]
    kafka_producer = connect_kafka_producer()
    for recipe in all_recipes:
        print("A")
        publish_message(kafka_producer, 'books', 'raw', recipe.strip())
    if kafka_producer is not None:
        kafka_producer.close()