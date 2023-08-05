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

class DomainNetworkCommandResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DomainNetworkCommandResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'correlation_id': 'str',
            'command_name': 'str',
            'acknowledged': 'bool',
            'error_info': 'ErrorDetails'
        }

        self.attribute_map = {
            'correlation_id': 'correlationId',
            'command_name': 'commandName',
            'acknowledged': 'acknowledged',
            'error_info': 'errorInfo'
        }

        self._correlation_id = None
        self._command_name = None
        self._acknowledged = None
        self._error_info = None

    @property
    def correlation_id(self):
        """
        Gets the correlation_id of this DomainNetworkCommandResponse.


        :return: The correlation_id of this DomainNetworkCommandResponse.
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """
        Sets the correlation_id of this DomainNetworkCommandResponse.


        :param correlation_id: The correlation_id of this DomainNetworkCommandResponse.
        :type: str
        """
        

        self._correlation_id = correlation_id

    @property
    def command_name(self):
        """
        Gets the command_name of this DomainNetworkCommandResponse.


        :return: The command_name of this DomainNetworkCommandResponse.
        :rtype: str
        """
        return self._command_name

    @command_name.setter
    def command_name(self, command_name):
        """
        Sets the command_name of this DomainNetworkCommandResponse.


        :param command_name: The command_name of this DomainNetworkCommandResponse.
        :type: str
        """
        

        self._command_name = command_name

    @property
    def acknowledged(self):
        """
        Gets the acknowledged of this DomainNetworkCommandResponse.


        :return: The acknowledged of this DomainNetworkCommandResponse.
        :rtype: bool
        """
        return self._acknowledged

    @acknowledged.setter
    def acknowledged(self, acknowledged):
        """
        Sets the acknowledged of this DomainNetworkCommandResponse.


        :param acknowledged: The acknowledged of this DomainNetworkCommandResponse.
        :type: bool
        """
        

        self._acknowledged = acknowledged

    @property
    def error_info(self):
        """
        Gets the error_info of this DomainNetworkCommandResponse.


        :return: The error_info of this DomainNetworkCommandResponse.
        :rtype: ErrorDetails
        """
        return self._error_info

    @error_info.setter
    def error_info(self, error_info):
        """
        Sets the error_info of this DomainNetworkCommandResponse.


        :param error_info: The error_info of this DomainNetworkCommandResponse.
        :type: ErrorDetails
        """
        

        self._error_info = error_info

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

