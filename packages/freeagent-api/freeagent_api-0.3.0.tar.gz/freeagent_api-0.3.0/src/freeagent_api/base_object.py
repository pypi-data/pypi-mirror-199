#!/usr/bin/env python3
"""Base class for API objects to inherit from.

Implements automatic attributes for API fields defined in derived classes, and adds an 'id'
attribute containing the identifier from the url field.

Derived classes should define an attribute called API_FIELDS, which should be a list of field names
for objects returned by that API. Field names can also have an optional type to cast the contents of
the field to that type, separated by a ':'. Unspecified types will be kept as strings. Currently
implemented types are:
    - integer: Basic whole number.
    - decimal: Currency values and similar
    - boolean: True/False values
    - date: Date field with no time component
    - datetime: Full date and time with hours, minutes, and seconds
    - id: URI-type field from which trailing digits will be extracted
"""
import re
from datetime import datetime, date
from decimal import Decimal


class BaseObject:
    """Base object for other API objects."""

    # Provide empty lists in case derived classes don't define these
    PARSED_API_FIELDS = []

    def __init__(self, data=None):
        """Initialise the object."""
        self._data = {}
        if data is not None:
            # Parse types out of the field names
            for field in self.API_FIELDS:
                try:
                    field, field_type = field.split(':')
                    value = data.get(field)
                    self.PARSED_API_FIELDS.append(field)

                    if field_type == 'integer':
                        self._data[field] = int(value or 0)
                    elif field_type == 'decimal':
                        self._data[field] = Decimal(value or 0)
                    elif field_type == 'boolean':
                        self._data[field] = bool(value)
                    elif field_type == 'datetime':
                        self._data[field] = datetime.fromisoformat(value or "")
                    elif field_type == 'date':
                        self._data[field] = datetime.fromisoformat(value or "").date()
                    elif field_type == 'id':
                        matches = re.search(r"(\d+)$", value or "")
                        self._data[field] = matches.group(0) if matches else None

                    else:
                        raise TypeError(f"Unknown type mapping '{field_type}' for {field}")

                except ValueError:
                    self.PARSED_API_FIELDS.append(field)
                    value = data.get(field)
                    self._data[field] = value

                    if field == 'url' and value is not None:
                        matches = re.search(r"(\d+)$", value or "")
                        self._data['id'] = matches.group(0) if matches else None


    def __getattr__(self, name: str):
        """Auto-generate attributes for the API fields.

        This overrides the basic object attribute getter to return data from the
        stored API data if the requested attribute name is an API field, and
        then look for a normal attribute of the object.

        Fields containing ID values are overridden to extract just the numerical
        ID instead of the full URL.
        """
        if name in self.PARSED_API_FIELDS or name == 'id':
            return self._data.get(name)

        if f"_{name}" in self.__dict__:
            return self.__dict__[f"_{name}"]

        raise AttributeError(f"{self.__class__.__name__} object has no attribute '{name}'")


    def as_dict(self) -> dict:
        """Get a dictionary based representation of the object.

        Mainly intended for testing and debugging.

        Returns:
            dict: Contents of object.
        """
        data = {}

        # Get API data
        for key in self.PARSED_API_FIELDS:
            if key in self._data:
                if isinstance(self._data[key], (datetime, date)):
                    data[key] = self._data[key].isoformat()
                else:
                    data[key] = self._data[key]

        # Other properties
        for key,value in self.__dict__.items():
            if not key.startswith("_") and value is not None:
                data[key] = value

        data['id'] = self.id

        return data
