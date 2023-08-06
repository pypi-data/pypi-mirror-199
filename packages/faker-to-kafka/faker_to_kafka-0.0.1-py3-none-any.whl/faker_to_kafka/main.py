import time

from datetime import datetime

from faker import Faker

from .generator_factory import GeneratorFactory
from .kafka_sender import KafkaSender
from .config_parse import GeneratorConfig, gen_config


class FakeDataKafkaSender:
    def __init__(self, config_path):
        self.config_path = config_path
        conf: GeneratorConfig = gen_config(config_path)
        self.conf = conf
        self.sender = KafkaSender(conf.kafka)
        self.faker = Faker(conf.fake["locale"])
        self.generator = GeneratorFactory.create(conf.format, self.faker, conf.fields)
        #
        self.count = 0
        self.state = "INIT"
        self.t_begin = 0
        self.t_end = 0
        #
        self.start()

    def fire_once(self):
        msg = self.generator.once()
        print(msg)
        self.sender.send(msg)

    def _not_reach_max(self):
        if self.conf.max <= 0:
            return True
        return self.conf.max > self.count

    def start(self):
        if self.state == "RUNNING":
            return
        self.state = "RUNNING"
        self.t_begin = datetime.now()

        while self._not_reach_max():
            self.fire_once()
            time.sleep(self.conf.sleep_s)
            self.count = self.count + 1

        self.t_end = datetime.now()
        print(f"count={self.count}, time_cost={self.t_end - self.t_begin}")
