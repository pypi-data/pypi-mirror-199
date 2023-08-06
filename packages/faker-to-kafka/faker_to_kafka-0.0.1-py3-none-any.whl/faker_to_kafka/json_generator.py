import json
from typing import List
from faker import Faker
from .config_parse import FieldConfig


class JsonGenerator:
    def __init__(self, faker: Faker, fields: List[FieldConfig]):
        self.fields = fields
        self.faker = faker

    def once(self):
        result = {}
        for f in self.fields:
            method = self.faker.__getattr__(f.provider)
            value = method(**f.args)
            value = str(value)
            result[f.name] = value
        return json.dumps(result, ensure_ascii=False)
