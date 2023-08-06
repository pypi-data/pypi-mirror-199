from dataclasses import dataclass
from typing import List
import yaml


@dataclass
class FieldConfig:
    name: str
    provider: str
    args: dict


@dataclass
class GeneratorConfig:
    kafka: dict
    fake: dict
    format: str
    max: int
    sleep_s: float
    fields: List[FieldConfig]


def _parse_field(unparsed_fields):
    fields = []
    for field in unparsed_fields:
        if isinstance(field, str):
            fields.append(FieldConfig(field, field, {}))
        if isinstance(field, dict):
            field_cp = field.copy()
            _name = list(field_cp.keys())[0]
            _provider = list(field_cp.values())[0]
            del field_cp[_name]
            _args = {} if len(field_cp) == 0 else field_cp
            fields.append(FieldConfig(_name, _provider, _args))
    return fields


def gen_config(file_path):
    _file = open(file_path, "r")
    conf = yaml.safe_load(_file)
    return GeneratorConfig(
        conf["kafka"],
        conf["fake"],
        conf["format"],
        conf["max"],
        1.0 / conf["frequency"],
        _parse_field(conf["fields"])
    )


if __name__ == "__main__":
    config: GeneratorConfig = gen_config("config.yml")
    print(config)
