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

class TextBotFlowLocation(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        TextBotFlowLocation - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'action_name': 'str',
            'action_number': 'int',
            'sequence_name': 'str'
        }

        self.attribute_map = {
            'action_name': 'actionName',
            'action_number': 'actionNumber',
            'sequence_name': 'sequenceName'
        }

        self._action_name = None
        self._action_number = None
        self._sequence_name = None

    @property
    def action_name(self):
        """
        Gets the action_name of this TextBotFlowLocation.
        The name of the action that was active when the event of interest happened.

        :return: The action_name of this TextBotFlowLocation.
        :rtype: str
        """
        return self._action_name

    @action_name.setter
    def action_name(self, action_name):
        """
        Sets the action_name of this TextBotFlowLocation.
        The name of the action that was active when the event of interest happened.

        :param action_name: The action_name of this TextBotFlowLocation.
        :type: str
        """
        

        self._action_name = action_name

    @property
    def action_number(self):
        """
        Gets the action_number of this TextBotFlowLocation.
        The number of the action that was active when the event of interest happened.

        :return: The action_number of this TextBotFlowLocation.
        :rtype: int
        """
        return self._action_number

    @action_number.setter
    def action_number(self, action_number):
        """
        Sets the action_number of this TextBotFlowLocation.
        The number of the action that was active when the event of interest happened.

        :param action_number: The action_number of this TextBotFlowLocation.
        :type: int
        """
        

        self._action_number = action_number

    @property
    def sequence_name(self):
        """
        Gets the sequence_name of this TextBotFlowLocation.
        The name of the state or task which was active when the event of interest happened.

        :return: The sequence_name of this TextBotFlowLocation.
        :rtype: str
        """
        return self._sequence_name

    @sequence_name.setter
    def sequence_name(self, sequence_name):
        """
        Sets the sequence_name of this TextBotFlowLocation.
        The name of the state or task which was active when the event of interest happened.

        :param sequence_name: The sequence_name of this TextBotFlowLocation.
        :type: str
        """
        

        self._sequence_name = sequence_name

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

