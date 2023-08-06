"""Schema validation for VRF."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"

from jsonschema import validate, FormatChecker

from ipam.models import VRF

from netdoc import utils


def get_schema():
    """Return the JSON schema to validate VRF data."""
    return {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
            },
            "rd": {
                "type": "string",
            },
        },
    }


def get_schema_create():
    """Return the JSON schema to validate new VRF objects."""
    schema = get_schema()
    schema["required"] = [
        "name",
    ]
    return schema


def create(**kwargs):
    """Create an VRF."""
    kwargs = utils.delete_empty_keys(kwargs)
    validate(kwargs, get_schema_create(), format_checker=FormatChecker())
    obj = utils.object_create(VRF, **kwargs)
    return obj


def get(name):
    """Return an VRF."""
    obj = utils.object_get_or_none(VRF, name=name)
    return obj


def get_list(**kwargs):
    """Get a list of VRF objects."""
    validate(kwargs, get_schema(), format_checker=FormatChecker())
    result = utils.object_list(VRF, **kwargs)
    return result


def update(obj, **kwargs):
    """Update an VRF."""
    update_if_not_set = ["rd"]

    kwargs = utils.delete_empty_keys(kwargs)
    validate(kwargs, get_schema(), format_checker=FormatChecker())
    kwargs_if_not_set = utils.filter_keys(kwargs, update_if_not_set)
    obj = utils.object_update(obj, **kwargs_if_not_set, force=False)
    return obj
