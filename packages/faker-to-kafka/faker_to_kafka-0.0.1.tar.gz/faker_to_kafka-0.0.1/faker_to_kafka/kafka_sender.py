from kafka import KafkaProducer
from kafka.errors import kafka_errors
import traceback


class KafkaSender(object):
    def __init__(self, conf: dict):
        self.bootstrap_servers = conf['bootstrap_servers']
        self.topic = conf['topic']
        self.producer = KafkaProducer(bootstrap_servers=conf['bootstrap_servers'])

    def send(self, msg: str, key=None):
        future = self.producer.send(self.topic, value=bytes(msg, 'utf-8'))
        try:
            future.get(timeout=10)  # 监控是否发送成功
        except kafka_errors:  # 发送失败抛出kafka_errors
            traceback.format_exc()

# sender = KafkaProducer({"bootstrap_servers": "kafka.dormi.io:9092", "topic": "topic01"})
# sender.send("hello")
