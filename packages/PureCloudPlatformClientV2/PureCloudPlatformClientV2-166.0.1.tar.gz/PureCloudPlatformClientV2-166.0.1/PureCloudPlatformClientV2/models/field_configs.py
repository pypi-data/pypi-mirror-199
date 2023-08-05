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

class FieldConfigs(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        FieldConfigs - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'org': 'FieldConfig',
            'person': 'FieldConfig',
            'group': 'FieldConfig',
            'external_contact': 'FieldConfig'
        }

        self.attribute_map = {
            'org': 'org',
            'person': 'person',
            'group': 'group',
            'external_contact': 'externalContact'
        }

        self._org = None
        self._person = None
        self._group = None
        self._external_contact = None

    @property
    def org(self):
        """
        Gets the org of this FieldConfigs.


        :return: The org of this FieldConfigs.
        :rtype: FieldConfig
        """
        return self._org

    @org.setter
    def org(self, org):
        """
        Sets the org of this FieldConfigs.


        :param org: The org of this FieldConfigs.
        :type: FieldConfig
        """
        

        self._org = org

    @property
    def person(self):
        """
        Gets the person of this FieldConfigs.


        :return: The person of this FieldConfigs.
        :rtype: FieldConfig
        """
        return self._person

    @person.setter
    def person(self, person):
        """
        Sets the person of this FieldConfigs.


        :param person: The person of this FieldConfigs.
        :type: FieldConfig
        """
        

        self._person = person

    @property
    def group(self):
        """
        Gets the group of this FieldConfigs.


        :return: The group of this FieldConfigs.
        :rtype: FieldConfig
        """
        return self._group

    @group.setter
    def group(self, group):
        """
        Sets the group of this FieldConfigs.


        :param group: The group of this FieldConfigs.
        :type: FieldConfig
        """
        

        self._group = group

    @property
    def external_contact(self):
        """
        Gets the external_contact of this FieldConfigs.


        :return: The external_contact of this FieldConfigs.
        :rtype: FieldConfig
        """
        return self._external_contact

    @external_contact.setter
    def external_contact(self, external_contact):
        """
        Sets the external_contact of this FieldConfigs.


        :param external_contact: The external_contact of this FieldConfigs.
        :type: FieldConfig
        """
        

        self._external_contact = external_contact

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

