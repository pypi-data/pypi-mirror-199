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

class EffectiveConfiguration(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        EffectiveConfiguration - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'properties': 'dict(str, object)',
            'advanced': 'dict(str, object)',
            'name': 'str',
            'notes': 'str',
            'credentials': 'dict(str, CredentialInfo)'
        }

        self.attribute_map = {
            'properties': 'properties',
            'advanced': 'advanced',
            'name': 'name',
            'notes': 'notes',
            'credentials': 'credentials'
        }

        self._properties = None
        self._advanced = None
        self._name = None
        self._notes = None
        self._credentials = None

    @property
    def properties(self):
        """
        Gets the properties of this EffectiveConfiguration.
        Key-value configuration settings described by the schema in the propertiesSchemaUri field.

        :return: The properties of this EffectiveConfiguration.
        :rtype: dict(str, object)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this EffectiveConfiguration.
        Key-value configuration settings described by the schema in the propertiesSchemaUri field.

        :param properties: The properties of this EffectiveConfiguration.
        :type: dict(str, object)
        """
        

        self._properties = properties

    @property
    def advanced(self):
        """
        Gets the advanced of this EffectiveConfiguration.
        Advanced configuration described by the schema in the advancedSchemaUri field.

        :return: The advanced of this EffectiveConfiguration.
        :rtype: dict(str, object)
        """
        return self._advanced

    @advanced.setter
    def advanced(self, advanced):
        """
        Sets the advanced of this EffectiveConfiguration.
        Advanced configuration described by the schema in the advancedSchemaUri field.

        :param advanced: The advanced of this EffectiveConfiguration.
        :type: dict(str, object)
        """
        

        self._advanced = advanced

    @property
    def name(self):
        """
        Gets the name of this EffectiveConfiguration.
        The name of the integration, used to distinguish this integration from others of the same type.

        :return: The name of this EffectiveConfiguration.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this EffectiveConfiguration.
        The name of the integration, used to distinguish this integration from others of the same type.

        :param name: The name of this EffectiveConfiguration.
        :type: str
        """
        

        self._name = name

    @property
    def notes(self):
        """
        Gets the notes of this EffectiveConfiguration.
        Notes about the integration.

        :return: The notes of this EffectiveConfiguration.
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """
        Sets the notes of this EffectiveConfiguration.
        Notes about the integration.

        :param notes: The notes of this EffectiveConfiguration.
        :type: str
        """
        

        self._notes = notes

    @property
    def credentials(self):
        """
        Gets the credentials of this EffectiveConfiguration.
        Credentials required by the integration. The required keys are indicated in the credentials property of the Integration Type

        :return: The credentials of this EffectiveConfiguration.
        :rtype: dict(str, CredentialInfo)
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Sets the credentials of this EffectiveConfiguration.
        Credentials required by the integration. The required keys are indicated in the credentials property of the Integration Type

        :param credentials: The credentials of this EffectiveConfiguration.
        :type: dict(str, CredentialInfo)
        """
        

        self._credentials = credentials

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

