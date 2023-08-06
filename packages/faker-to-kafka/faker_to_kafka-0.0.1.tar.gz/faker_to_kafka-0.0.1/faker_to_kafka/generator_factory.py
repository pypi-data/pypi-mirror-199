from .csv_generator import CsvGenerator
from .json_generator import JsonGenerator


class GeneratorFactory:

    @staticmethod
    def create(_format: str, faker, fields_conf):
        if _format == "csv":
            return CsvGenerator(faker, fields_conf)
        if _format == "json":
            return JsonGenerator(faker, fields_conf)
        raise f"unsupported format {_format}"
