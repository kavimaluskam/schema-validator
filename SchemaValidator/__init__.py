import datetime
import json
import os

from SchemaValidator.schema import define_field_schema
from SchemaValidator.schema import merge_schema
from SchemaValidator.schema import validate_record


def generate_schema_by_records(input_path: str):
    """
    Generate schema from json file
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"File {input_path} is not found.")

    schema = {}

    with open(input_path, 'r') as r:
        for line in r:
            record = json.loads(line)
            temp_schema = {}

            for name, field in record.items():
                temp_schema[name] = define_field_schema(field)

            schema = merge_schema(
                prev_schema=schema,
                new_schema=temp_schema
            )

    return schema


def validate_records(input_path: str, schema: dict):
    """
    Validate json records with existing schema
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"File {input_path} is not found.")

    errors = []
    with open(input_path, 'r') as r:
        for line_number, line in enumerate(r):
            record = json.loads(line)
            line_errors = validate_record(record, schema)

            if line_errors:
                errors.append({
                    "line_number": line_number,
                    "errors": line_errors
                })

    return errors


def generate_summary_report(input_path: str):
    """
    Generate summary report from json file
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"File {input_path} is not found.")

    data = {}
    with open(input_path, 'r') as r:
        for line in r:
            record = json.loads(line)

            timestamp, name = record.get('timestamp'), record.get('event')
            date = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f').date().strftime('%Y-%m-%d')
            key = f"{date}{name}"

            if key in data:
                data[key] += 1
            else:
                data[key] = 1

    return [
        {"name": k[10:], "date": k[:10], "count": v}
        for k, v in data.items()
    ]
