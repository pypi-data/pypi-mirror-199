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

class QueueConversationVideoEventTopicAfterCallWork(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        QueueConversationVideoEventTopicAfterCallWork - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'state': 'str',
            'start_time': 'datetime',
            'end_time': 'datetime'
        }

        self.attribute_map = {
            'state': 'state',
            'start_time': 'startTime',
            'end_time': 'endTime'
        }

        self._state = None
        self._start_time = None
        self._end_time = None

    @property
    def state(self):
        """
        Gets the state of this QueueConversationVideoEventTopicAfterCallWork.
        The communication's after-call work state.

        :return: The state of this QueueConversationVideoEventTopicAfterCallWork.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this QueueConversationVideoEventTopicAfterCallWork.
        The communication's after-call work state.

        :param state: The state of this QueueConversationVideoEventTopicAfterCallWork.
        :type: str
        """
        allowed_values = ["unknown", "skipped", "pending", "complete", "notApplicable"]
        if state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for state -> " + state)
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def start_time(self):
        """
        Gets the start_time of this QueueConversationVideoEventTopicAfterCallWork.
        The timestamp when this communication started after-call work in the cloud clock.

        :return: The start_time of this QueueConversationVideoEventTopicAfterCallWork.
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Sets the start_time of this QueueConversationVideoEventTopicAfterCallWork.
        The timestamp when this communication started after-call work in the cloud clock.

        :param start_time: The start_time of this QueueConversationVideoEventTopicAfterCallWork.
        :type: datetime
        """
        

        self._start_time = start_time

    @property
    def end_time(self):
        """
        Gets the end_time of this QueueConversationVideoEventTopicAfterCallWork.
        The timestamp when this communication ended after-call work in the cloud clock.

        :return: The end_time of this QueueConversationVideoEventTopicAfterCallWork.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """
        Sets the end_time of this QueueConversationVideoEventTopicAfterCallWork.
        The timestamp when this communication ended after-call work in the cloud clock.

        :param end_time: The end_time of this QueueConversationVideoEventTopicAfterCallWork.
        :type: datetime
        """
        

        self._end_time = end_time

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

