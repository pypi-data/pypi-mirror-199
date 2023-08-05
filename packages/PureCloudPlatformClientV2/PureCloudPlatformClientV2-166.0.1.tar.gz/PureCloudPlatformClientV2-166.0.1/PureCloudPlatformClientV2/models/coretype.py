# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re
import json

from ..utils import sanitize_for_serialization

class Coretype(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Coretype - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'version': 'int',
            'date_created': 'datetime',
            'schema': 'Schema',
            'current': 'bool',
            'validation_fields': 'list[str]',
            'validation_limits': 'ValidationLimits',
            'item_validation_fields': 'list[str]',
            'item_validation_limits': 'ItemValidationLimits',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'version': 'version',
            'date_created': 'dateCreated',
            'schema': 'schema',
            'current': 'current',
            'validation_fields': 'validationFields',
            'validation_limits': 'validationLimits',
            'item_validation_fields': 'itemValidationFields',
            'item_validation_limits': 'itemValidationLimits',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._version = None
        self._date_created = None
        self._schema = None
        self._current = None
        self._validation_fields = None
        self._validation_limits = None
        self._item_validation_fields = None
        self._item_validation_limits = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this Coretype.
        The globally unique identifier for the object.

        :return: The id of this Coretype.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Coretype.
        The globally unique identifier for the object.

        :param id: The id of this Coretype.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Coretype.


        :return: The name of this Coretype.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Coretype.


        :param name: The name of this Coretype.
        :type: str
        """
        

        self._name = name

    @property
    def version(self):
        """
        Gets the version of this Coretype.
        A positive integer denoting the core type's version

        :return: The version of this Coretype.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this Coretype.
        A positive integer denoting the core type's version

        :param version: The version of this Coretype.
        :type: int
        """
        

        self._version = version

    @property
    def date_created(self):
        """
        Gets the date_created of this Coretype.
        The date the core type was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_created of this Coretype.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this Coretype.
        The date the core type was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_created: The date_created of this Coretype.
        :type: datetime
        """
        

        self._date_created = date_created

    @property
    def schema(self):
        """
        Gets the schema of this Coretype.
        The core type's built-in schema

        :return: The schema of this Coretype.
        :rtype: Schema
        """
        return self._schema

    @schema.setter
    def schema(self, schema):
        """
        Sets the schema of this Coretype.
        The core type's built-in schema

        :param schema: The schema of this Coretype.
        :type: Schema
        """
        

        self._schema = schema

    @property
    def current(self):
        """
        Gets the current of this Coretype.
        A boolean indicating if the core type's version is the current one in use by the system

        :return: The current of this Coretype.
        :rtype: bool
        """
        return self._current

    @current.setter
    def current(self, current):
        """
        Sets the current of this Coretype.
        A boolean indicating if the core type's version is the current one in use by the system

        :param current: The current of this Coretype.
        :type: bool
        """
        

        self._current = current

    @property
    def validation_fields(self):
        """
        Gets the validation_fields of this Coretype.
        An array of strings naming the fields of the core type subject to validation.  Validation constraints are specified by a schema author using the core type.

        :return: The validation_fields of this Coretype.
        :rtype: list[str]
        """
        return self._validation_fields

    @validation_fields.setter
    def validation_fields(self, validation_fields):
        """
        Sets the validation_fields of this Coretype.
        An array of strings naming the fields of the core type subject to validation.  Validation constraints are specified by a schema author using the core type.

        :param validation_fields: The validation_fields of this Coretype.
        :type: list[str]
        """
        

        self._validation_fields = validation_fields

    @property
    def validation_limits(self):
        """
        Gets the validation_limits of this Coretype.
        A structure denoting the system-imposed minimum and maximum string length (for text-based core types) or numeric values (for number-based) core types.  For example, the validationLimits for a text-based core type specify the min/max values for a minimum string length (minLength) constraint supplied by a schemaauthor on a text field.  Similarly, the maxLength's min/max specifies maximum string length constraint supplied by a schema author for the same field.

        :return: The validation_limits of this Coretype.
        :rtype: ValidationLimits
        """
        return self._validation_limits

    @validation_limits.setter
    def validation_limits(self, validation_limits):
        """
        Sets the validation_limits of this Coretype.
        A structure denoting the system-imposed minimum and maximum string length (for text-based core types) or numeric values (for number-based) core types.  For example, the validationLimits for a text-based core type specify the min/max values for a minimum string length (minLength) constraint supplied by a schemaauthor on a text field.  Similarly, the maxLength's min/max specifies maximum string length constraint supplied by a schema author for the same field.

        :param validation_limits: The validation_limits of this Coretype.
        :type: ValidationLimits
        """
        

        self._validation_limits = validation_limits

    @property
    def item_validation_fields(self):
        """
        Gets the item_validation_fields of this Coretype.
        Specific to the \"tag\" core type, this is an array of strings naming the tag item fields of the core type subject to validation

        :return: The item_validation_fields of this Coretype.
        :rtype: list[str]
        """
        return self._item_validation_fields

    @item_validation_fields.setter
    def item_validation_fields(self, item_validation_fields):
        """
        Sets the item_validation_fields of this Coretype.
        Specific to the \"tag\" core type, this is an array of strings naming the tag item fields of the core type subject to validation

        :param item_validation_fields: The item_validation_fields of this Coretype.
        :type: list[str]
        """
        

        self._item_validation_fields = item_validation_fields

    @property
    def item_validation_limits(self):
        """
        Gets the item_validation_limits of this Coretype.
        A structure denoting the system-imposed minimum and maximum string length for string-array based core types such as \"tag\" and \"enum\".  Forexample, the validationLimits for a schema field using a tag core type specify the min/max values for a minimum string length (minLength) constraint supplied by a schema author on individual tags.  Similarly, the maxLength's min/max specifies maximum string length constraint supplied by a schema author for the same field's tags.

        :return: The item_validation_limits of this Coretype.
        :rtype: ItemValidationLimits
        """
        return self._item_validation_limits

    @item_validation_limits.setter
    def item_validation_limits(self, item_validation_limits):
        """
        Sets the item_validation_limits of this Coretype.
        A structure denoting the system-imposed minimum and maximum string length for string-array based core types such as \"tag\" and \"enum\".  Forexample, the validationLimits for a schema field using a tag core type specify the min/max values for a minimum string length (minLength) constraint supplied by a schema author on individual tags.  Similarly, the maxLength's min/max specifies maximum string length constraint supplied by a schema author for the same field's tags.

        :param item_validation_limits: The item_validation_limits of this Coretype.
        :type: ItemValidationLimits
        """
        

        self._item_validation_limits = item_validation_limits

    @property
    def self_uri(self):
        """
        Gets the self_uri of this Coretype.
        The URI for this object

        :return: The self_uri of this Coretype.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this Coretype.
        The URI for this object

        :param self_uri: The self_uri of this Coretype.
        :type: str
        """
        

        self._self_uri = self_uri

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

