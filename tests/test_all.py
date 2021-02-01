import json
import pytest

from SchemaValidator import generate_schema
from SchemaValidator import validate_records
from SchemaValidator import generate_summary_report


def test_generate_schema_correct_case():

    input_path = "tests/data/sample-1.json"
    schema_path = "tests/data/schema-test-1.json"

    schema = {}
    with open(schema_path) as json_file:
        schema = json.load(json_file)

    assert schema == generate_schema(input_path)


def test_generate_schema_incorrect_case():

    input_path = "tests/data/sample-2.json"

    with pytest.raises(Exception):
        generate_schema(input_path)


def test_validate_correct_case():

    input_path = "tests/data/sample-1.json"
    schema_path = "tests/data/schema-test-1.json"

    schema = {}
    with open(schema_path) as json_file:
        schema = json.load(json_file)

    assert [] == validate_records(input_path, schema)


def test_validate_incorrect_case():

    input_path = "tests/data/sample-2.json"
    schema_path = "tests/data/schema-test-1.json"

    schema = {}
    with open(schema_path) as json_file:
        schema = json.load(json_file)

    assert validate_records(input_path, schema) == [
        {
            'line_number': 3,
            'errors': [{'name': 'regEx', 'type': 'Missing Field'}]
        }, {
            'line_number': 4,
            'errors': [
                {'name': 'random float',
                 'schema_type': 'number',
                 'type': 'Unmatched data type',
                 'value': 'ASD'},
                {'name': 'array.element_type',
                 'schema_type': 'string',
                 'type': 'Unmatched data type',
                 'value': 123},
                {'name': 'array.element_type',
                 'schema_type': 'string',
                 'type': 'Unmatched data type',
                 'value': 456},
                {'name': 'array.element_type',
                 'schema_type': 'string',
                 'type': 'Unmatched data type',
                 'value': 0},
                {'name': 'array.element_type',
                 'schema_type': 'string',
                 'type': 'Unmatched data type',
                 'value': 1},
                {'name': 'array.element_type',
                 'schema_type': 'string',
                 'type': 'Unmatched data type',
                 'value': 3},
                {'name': 'array of objects.element_type.index start at 5',
                 'type': 'Missing Field'}
            ]
        }
    ]


def test_report():
    input_path = "tests/data/sample-report.json"
    answer_path = "tests/data/sample-report-answer.json"

    data = generate_summary_report(input_path)

    answer = {}
    with open(answer_path) as json_file:
        answer = json.load(json_file)

    assert data == answer
