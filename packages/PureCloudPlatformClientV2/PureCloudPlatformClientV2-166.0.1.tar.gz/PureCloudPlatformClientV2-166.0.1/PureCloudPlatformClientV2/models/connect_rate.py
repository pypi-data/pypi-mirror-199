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

class ConnectRate(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ConnectRate - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'attempts': 'int',
            'connects': 'int',
            'connect_ratio': 'float'
        }

        self.attribute_map = {
            'attempts': 'attempts',
            'connects': 'connects',
            'connect_ratio': 'connectRatio'
        }

        self._attempts = None
        self._connects = None
        self._connect_ratio = None

    @property
    def attempts(self):
        """
        Gets the attempts of this ConnectRate.
        Number of call attempts made

        :return: The attempts of this ConnectRate.
        :rtype: int
        """
        return self._attempts

    @attempts.setter
    def attempts(self, attempts):
        """
        Sets the attempts of this ConnectRate.
        Number of call attempts made

        :param attempts: The attempts of this ConnectRate.
        :type: int
        """
        

        self._attempts = attempts

    @property
    def connects(self):
        """
        Gets the connects of this ConnectRate.
        Number of calls with a live voice detected

        :return: The connects of this ConnectRate.
        :rtype: int
        """
        return self._connects

    @connects.setter
    def connects(self, connects):
        """
        Sets the connects of this ConnectRate.
        Number of calls with a live voice detected

        :param connects: The connects of this ConnectRate.
        :type: int
        """
        

        self._connects = connects

    @property
    def connect_ratio(self):
        """
        Gets the connect_ratio of this ConnectRate.
        Ratio of connects to attempts

        :return: The connect_ratio of this ConnectRate.
        :rtype: float
        """
        return self._connect_ratio

    @connect_ratio.setter
    def connect_ratio(self, connect_ratio):
        """
        Sets the connect_ratio of this ConnectRate.
        Ratio of connects to attempts

        :param connect_ratio: The connect_ratio of this ConnectRate.
        :type: float
        """
        

        self._connect_ratio = connect_ratio

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

