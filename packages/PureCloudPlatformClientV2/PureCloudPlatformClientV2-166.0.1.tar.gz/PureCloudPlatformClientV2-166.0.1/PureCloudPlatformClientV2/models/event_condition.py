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

class EventCondition(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        EventCondition - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'key': 'str',
            'values': 'list[str]',
            'operator': 'str',
            'stream_type': 'str',
            'session_type': 'str',
            'event_name': 'str'
        }

        self.attribute_map = {
            'key': 'key',
            'values': 'values',
            'operator': 'operator',
            'stream_type': 'streamType',
            'session_type': 'sessionType',
            'event_name': 'eventName'
        }

        self._key = None
        self._values = None
        self._operator = None
        self._stream_type = None
        self._session_type = None
        self._event_name = None

    @property
    def key(self):
        """
        Gets the key of this EventCondition.
        The event key.

        :return: The key of this EventCondition.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this EventCondition.
        The event key.

        :param key: The key of this EventCondition.
        :type: str
        """
        

        self._key = key

    @property
    def values(self):
        """
        Gets the values of this EventCondition.
        The event values.

        :return: The values of this EventCondition.
        :rtype: list[str]
        """
        return self._values

    @values.setter
    def values(self, values):
        """
        Sets the values of this EventCondition.
        The event values.

        :param values: The values of this EventCondition.
        :type: list[str]
        """
        

        self._values = values

    @property
    def operator(self):
        """
        Gets the operator of this EventCondition.
        The comparison operator.

        :return: The operator of this EventCondition.
        :rtype: str
        """
        return self._operator

    @operator.setter
    def operator(self, operator):
        """
        Sets the operator of this EventCondition.
        The comparison operator.

        :param operator: The operator of this EventCondition.
        :type: str
        """
        allowed_values = ["containsAll", "containsAny", "notContainsAll", "notContainsAny", "equal", "notEqual", "greaterThan", "greaterThanOrEqual", "lessThan", "lessThanOrEqual", "startsWith", "endsWith"]
        if operator.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for operator -> " + operator)
            self._operator = "outdated_sdk_version"
        else:
            self._operator = operator

    @property
    def stream_type(self):
        """
        Gets the stream_type of this EventCondition.
        The stream type for which this condition can be satisfied.

        :return: The stream_type of this EventCondition.
        :rtype: str
        """
        return self._stream_type

    @stream_type.setter
    def stream_type(self, stream_type):
        """
        Sets the stream_type of this EventCondition.
        The stream type for which this condition can be satisfied.

        :param stream_type: The stream_type of this EventCondition.
        :type: str
        """
        allowed_values = ["Web", "Custom", "Conversation", "App"]
        if stream_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for stream_type -> " + stream_type)
            self._stream_type = "outdated_sdk_version"
        else:
            self._stream_type = stream_type

    @property
    def session_type(self):
        """
        Gets the session_type of this EventCondition.
        The session type for which this condition can be satisfied.

        :return: The session_type of this EventCondition.
        :rtype: str
        """
        return self._session_type

    @session_type.setter
    def session_type(self, session_type):
        """
        Sets the session_type of this EventCondition.
        The session type for which this condition can be satisfied.

        :param session_type: The session_type of this EventCondition.
        :type: str
        """
        

        self._session_type = session_type

    @property
    def event_name(self):
        """
        Gets the event_name of this EventCondition.
        The name of the event for which this condition can be satisfied.

        :return: The event_name of this EventCondition.
        :rtype: str
        """
        return self._event_name

    @event_name.setter
    def event_name(self, event_name):
        """
        Sets the event_name of this EventCondition.
        The name of the event for which this condition can be satisfied.

        :param event_name: The event_name of this EventCondition.
        :type: str
        """
        

        self._event_name = event_name

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

