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

class EdgeLogicalInterfacesChangeTopicErrorInfo(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        EdgeLogicalInterfacesChangeTopicErrorInfo - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'message': 'str',
            'message_with_params': 'str',
            'message_params': 'dict(str, str)',
            'code': 'str'
        }

        self.attribute_map = {
            'message': 'message',
            'message_with_params': 'messageWithParams',
            'message_params': 'messageParams',
            'code': 'code'
        }

        self._message = None
        self._message_with_params = None
        self._message_params = None
        self._code = None

    @property
    def message(self):
        """
        Gets the message of this EdgeLogicalInterfacesChangeTopicErrorInfo.


        :return: The message of this EdgeLogicalInterfacesChangeTopicErrorInfo.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this EdgeLogicalInterfacesChangeTopicErrorInfo.


        :param message: The message of this EdgeLogicalInterfacesChangeTopicErrorInfo.
        :type: str
        """
        

        self._message = message

    @property
    def message_with_params(self):
        """
        Gets the message_with_params of this EdgeLogicalInterfacesChangeTopicErrorInfo.


        :return: The message_with_params of this EdgeLogicalInterfacesChangeTopicErrorInfo.
        :rtype: str
        """
        return self._message_with_params

    @message_with_params.setter
    def message_with_params(self, message_with_params):
        """
        Sets the message_with_params of this EdgeLogicalInterfacesChangeTopicErrorInfo.


        :param message_with_params: The message_with_params of this EdgeLogicalInterfacesChangeTopicErrorInfo.
        :type: str
        """
        

        self._message_with_params = message_with_params

    @property
    def message_params(self):
        """
        Gets the message_params of this EdgeLogicalInterfacesChangeTopicErrorInfo.


        :return: The message_params of this EdgeLogicalInterfacesChangeTopicErrorInfo.
        :rtype: dict(str, str)
        """
        return self._message_params

    @message_params.setter
    def message_params(self, message_params):
        """
        Sets the message_params of this EdgeLogicalInterfacesChangeTopicErrorInfo.


        :param message_params: The message_params of this EdgeLogicalInterfacesChangeTopicErrorInfo.
        :type: dict(str, str)
        """
        

        self._message_params = message_params

    @property
    def code(self):
        """
        Gets the code of this EdgeLogicalInterfacesChangeTopicErrorInfo.


        :return: The code of this EdgeLogicalInterfacesChangeTopicErrorInfo.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this EdgeLogicalInterfacesChangeTopicErrorInfo.


        :param code: The code of this EdgeLogicalInterfacesChangeTopicErrorInfo.
        :type: str
        """
        

        self._code = code

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

