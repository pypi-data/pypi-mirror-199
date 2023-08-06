from typing import List
from faker import Faker
from .config_parse import FieldConfig


class CsvGenerator:
    SEPERATOR = ","

    def __init__(self, faker: Faker, fields: List[FieldConfig]):
        self.fields = fields
        self.faker = faker

    def once(self):
        result = ""
        for f in self.fields:
            method = self.faker.__getattr__(f.provider)
            value = method(**f.args)
            value = str(value)
            result = result + value + ","
        return result[:-1]
