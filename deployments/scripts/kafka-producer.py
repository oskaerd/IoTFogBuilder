from kafka import KafkaProducer
import sys

def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=[f'{sys.argv[1]}:{sys.argv[2]}'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

if __name__ == '__main__':
    with open(f'{sys.argv[4]}', 'r') as input_file:
        records_to_send = input_file.readlines()
        kafka_producer = connect_kafka_producer()
        for recipe in records_to_send:
            publish_message(kafka_producer, sys.argv[3], 'raw', recipe.strip())
        if kafka_producer is not None:
            kafka_producer.close()