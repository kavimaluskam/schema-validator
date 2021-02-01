def define_field_schema(field: object):
    """
    Define schema for individual fields
    """
    if type(field) is dict:
        return {
            'type': 'object',
            'required': True,
            'fields': {
                k: define_field_schema(v)
                for k, v in field.items()
            }
        }

    elif type(field) is list:
        return {
            'type': 'array',
            'required': True,
            'element_type': define_field_schema(field[0])
        }

    elif type(field) is str:
        return {'type': 'string', 'required': True}

    elif type(field) is bool:
        return {'type': 'boolean', 'required': True}

    elif type(field) is int or type(field) is float:
        return {'type': 'number', 'required': True}

    elif field is None:
        return {'type': 'None', 'required': False}

    raise Exception(
        "Invalid record is found when defining schema:\n" +
        f"value={field}"
    )


def merge_schema(prev_schema: dict, new_schema: dict):
    """
    Merge schema of two versions
    """
    if not prev_schema:
        return new_schema

    for field_name in list(new_schema):
        if field_name not in list(prev_schema):
            new_schema[field_name]['required'] = False
            prev_schema[field_name] = new_schema[field_name]

    for field_name in list(prev_schema):
        if field_name not in list(new_schema):
            prev_schema[field_name]['required'] = False

        elif new_schema[field_name]['type'] == 'None':
            prev_schema[field_name]['required'] = False

        elif prev_schema[field_name]['type'] == 'None':
            prev_schema[field_name]['type'] = new_schema[field_name]['type']
            prev_schema[field_name]['required'] = False

        elif prev_schema[field_name]['type'] != new_schema[field_name]['type']:
            raise Exception(
                "Unmatched data type is found during schema generation: " +
                f"field={field_name}.\n" +
                "Please make sure the input file is of correct format."
            )

    return prev_schema


def validate_record(record: dict, schema: dict):
    """
    Validate individual record with provided schema
    """
    errors = []

    # Check for missing field in record
    for field_name in schema.keys():
        if field_name not in record.keys() \
                and schema[field_name]['required'] is True:
            errors.append(
                {"type": "Missing Field", "name": field_name}
            )

    # Validate fields in record
    for name, field in record.items():
        errors += validate_field(name, field, schema)

    return errors


def validate_field(name, field, schema):
    """
    Validate individual field with provided schema
    """
    errors = []

    field_schema = schema.get(name)
    if not field_schema:
        errors.append(
            {"type": "Unexpected Field", "name": name, "value": field}
        )

    schema_type = field_schema.get('type')
    if (type(field) is dict and schema_type != 'object') \
            or (type(field) is list and schema_type != 'array') \
            or (type(field) is str and schema_type != 'string') \
            or (type(field) is bool and schema_type != 'boolean') \
            or (type(field) is int and schema_type != 'number') \
            or (type(field) is float and schema_type != 'number'):
        errors.append(
            {
                "type": "Unmatched data type",
                "name": name,
                "value": field,
                "schema_type": schema_type
            }
        )

    if type(field) is dict:
        dict_errors = validate_record(field, field_schema.get('fields'))
        for e in dict_errors:
            e['name'] = f"{name}.{e['name']}"
            errors.append(e)

    if type(field) is list:
        for item in field:
            list_errors = validate_field(
                'element_type',
                item,
                field_schema
            )
            for e in list_errors:
                e['name'] = f"{name}.{e['name']}"
                errors.append(e)

    if field is None and field_schema.get('required'):
        errors.append(
            {"type": "Missing Field", "name": name}
        )

    return errors
