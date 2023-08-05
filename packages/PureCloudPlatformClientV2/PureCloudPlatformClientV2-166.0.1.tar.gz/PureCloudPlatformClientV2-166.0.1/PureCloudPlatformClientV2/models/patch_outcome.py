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

class PatchOutcome(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        PatchOutcome - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'is_active': 'bool',
            'display_name': 'str',
            'version': 'int',
            'description': 'str',
            'is_positive': 'bool',
            'context': 'Context',
            'journey': 'Journey',
            'associated_value_field': 'AssociatedValueField',
            'self_uri': 'str',
            'created_date': 'datetime',
            'modified_date': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'is_active': 'isActive',
            'display_name': 'displayName',
            'version': 'version',
            'description': 'description',
            'is_positive': 'isPositive',
            'context': 'context',
            'journey': 'journey',
            'associated_value_field': 'associatedValueField',
            'self_uri': 'selfUri',
            'created_date': 'createdDate',
            'modified_date': 'modifiedDate'
        }

        self._id = None
        self._is_active = None
        self._display_name = None
        self._version = None
        self._description = None
        self._is_positive = None
        self._context = None
        self._journey = None
        self._associated_value_field = None
        self._self_uri = None
        self._created_date = None
        self._modified_date = None

    @property
    def id(self):
        """
        Gets the id of this PatchOutcome.
        The globally unique identifier for the object.

        :return: The id of this PatchOutcome.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this PatchOutcome.
        The globally unique identifier for the object.

        :param id: The id of this PatchOutcome.
        :type: str
        """
        

        self._id = id

    @property
    def is_active(self):
        """
        Gets the is_active of this PatchOutcome.
        Whether or not the outcome is active.

        :return: The is_active of this PatchOutcome.
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """
        Sets the is_active of this PatchOutcome.
        Whether or not the outcome is active.

        :param is_active: The is_active of this PatchOutcome.
        :type: bool
        """
        

        self._is_active = is_active

    @property
    def display_name(self):
        """
        Gets the display_name of this PatchOutcome.
        The display name of the outcome.

        :return: The display_name of this PatchOutcome.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this PatchOutcome.
        The display name of the outcome.

        :param display_name: The display_name of this PatchOutcome.
        :type: str
        """
        

        self._display_name = display_name

    @property
    def version(self):
        """
        Gets the version of this PatchOutcome.
        The version of the outcome.

        :return: The version of this PatchOutcome.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this PatchOutcome.
        The version of the outcome.

        :param version: The version of this PatchOutcome.
        :type: int
        """
        

        self._version = version

    @property
    def description(self):
        """
        Gets the description of this PatchOutcome.
        A description of the outcome.

        :return: The description of this PatchOutcome.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this PatchOutcome.
        A description of the outcome.

        :param description: The description of this PatchOutcome.
        :type: str
        """
        

        self._description = description

    @property
    def is_positive(self):
        """
        Gets the is_positive of this PatchOutcome.
        Whether or not the outcome is positive.

        :return: The is_positive of this PatchOutcome.
        :rtype: bool
        """
        return self._is_positive

    @is_positive.setter
    def is_positive(self, is_positive):
        """
        Sets the is_positive of this PatchOutcome.
        Whether or not the outcome is positive.

        :param is_positive: The is_positive of this PatchOutcome.
        :type: bool
        """
        

        self._is_positive = is_positive

    @property
    def context(self):
        """
        Gets the context of this PatchOutcome.
        The context of the outcome.

        :return: The context of this PatchOutcome.
        :rtype: Context
        """
        return self._context

    @context.setter
    def context(self, context):
        """
        Sets the context of this PatchOutcome.
        The context of the outcome.

        :param context: The context of this PatchOutcome.
        :type: Context
        """
        

        self._context = context

    @property
    def journey(self):
        """
        Gets the journey of this PatchOutcome.
        The pattern of rules defining the filter of the outcome.

        :return: The journey of this PatchOutcome.
        :rtype: Journey
        """
        return self._journey

    @journey.setter
    def journey(self, journey):
        """
        Sets the journey of this PatchOutcome.
        The pattern of rules defining the filter of the outcome.

        :param journey: The journey of this PatchOutcome.
        :type: Journey
        """
        

        self._journey = journey

    @property
    def associated_value_field(self):
        """
        Gets the associated_value_field of this PatchOutcome.
        The field from the event indicating the associated value.

        :return: The associated_value_field of this PatchOutcome.
        :rtype: AssociatedValueField
        """
        return self._associated_value_field

    @associated_value_field.setter
    def associated_value_field(self, associated_value_field):
        """
        Sets the associated_value_field of this PatchOutcome.
        The field from the event indicating the associated value.

        :param associated_value_field: The associated_value_field of this PatchOutcome.
        :type: AssociatedValueField
        """
        

        self._associated_value_field = associated_value_field

    @property
    def self_uri(self):
        """
        Gets the self_uri of this PatchOutcome.
        The URI for this object

        :return: The self_uri of this PatchOutcome.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this PatchOutcome.
        The URI for this object

        :param self_uri: The self_uri of this PatchOutcome.
        :type: str
        """
        

        self._self_uri = self_uri

    @property
    def created_date(self):
        """
        Gets the created_date of this PatchOutcome.
        Timestamp indicating when the outcome was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The created_date of this PatchOutcome.
        :rtype: datetime
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """
        Sets the created_date of this PatchOutcome.
        Timestamp indicating when the outcome was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param created_date: The created_date of this PatchOutcome.
        :type: datetime
        """
        

        self._created_date = created_date

    @property
    def modified_date(self):
        """
        Gets the modified_date of this PatchOutcome.
        Timestamp indicating when the outcome was last updated. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The modified_date of this PatchOutcome.
        :rtype: datetime
        """
        return self._modified_date

    @modified_date.setter
    def modified_date(self, modified_date):
        """
        Sets the modified_date of this PatchOutcome.
        Timestamp indicating when the outcome was last updated. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param modified_date: The modified_date of this PatchOutcome.
        :type: datetime
        """
        

        self._modified_date = modified_date

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

