# Create your views here.
import logging
import json
import jsonschema
from pathlib import Path

logger = logging.getLogger("info_logs")


def schema_validation(data, path):
    """Function for validating Json Schema functionality."""
    flag = 0
    schema = load(path)
    v = jsonschema.Draft4Validator(schema)
    errors = sorted(v.iter_errors(data), key=lambda e: e.path)

    for error in errors:
        logger.info('json validation failed')
        flag = 452
        output_json = dict(zip(['Status', 'Message'], [flag, error.message]))
        return output_json
    logger.info('schema validation done')
    output_json = dict(zip(['Status', 'Message'], [flag, 'schema validation done']))
    return output_json


def load(schema_path):
    """
    :param schema_path:
    :return:
    """
    schema = Path(schema_path)

    with schema.open() as f:
        return json.load(f)
