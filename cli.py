import click
import json

from SchemaValidator import generate_schema_by_records
from SchemaValidator import validate_records
from SchemaValidator import generate_summary_report


@click.group()
def cli():
    """A simple schema validation tool"""
    pass  # Entry Point


@cli.command()
@click.option('--input_path',
              required=True,
              help='Path to your input json to define schema')
def generate_schema(input_path):
    """Define schema based on existing json"""
    schema = generate_schema_by_records(input_path)
    print(json.dumps(schema))


@cli.command()
@click.option('--input_path',
              required=True,
              help='Path to your input json to be validate')
@click.option('--schema_path',
              required=True,
              help='Path to your schema json')
def validate(input_path, schema_path):
    """Validate json records with existing schema"""
    schema = {}

    with open(schema_path) as json_file:
        schema = json.load(json_file)

    errors = validate_records(input_path, schema)
    if errors:
        print(json.dumps(errors))


@cli.command()
@click.option('--input_path',
              required=True,
              help='Path to your input json to be validate')
def summary(input_path):
    """Generate summary report"""
    data = generate_summary_report(input_path)
    print(json.dumps(data))


if __name__ == '__main__':
    cli()
