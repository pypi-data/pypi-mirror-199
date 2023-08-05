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

class ChatMediaPolicyConditions(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ChatMediaPolicyConditions - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'for_users': 'list[User]',
            'date_ranges': 'list[str]',
            'for_queues': 'list[Queue]',
            'wrapup_codes': 'list[WrapupCode]',
            'languages': 'list[Language]',
            'time_allowed': 'TimeAllowed',
            'duration': 'DurationCondition'
        }

        self.attribute_map = {
            'for_users': 'forUsers',
            'date_ranges': 'dateRanges',
            'for_queues': 'forQueues',
            'wrapup_codes': 'wrapupCodes',
            'languages': 'languages',
            'time_allowed': 'timeAllowed',
            'duration': 'duration'
        }

        self._for_users = None
        self._date_ranges = None
        self._for_queues = None
        self._wrapup_codes = None
        self._languages = None
        self._time_allowed = None
        self._duration = None

    @property
    def for_users(self):
        """
        Gets the for_users of this ChatMediaPolicyConditions.


        :return: The for_users of this ChatMediaPolicyConditions.
        :rtype: list[User]
        """
        return self._for_users

    @for_users.setter
    def for_users(self, for_users):
        """
        Sets the for_users of this ChatMediaPolicyConditions.


        :param for_users: The for_users of this ChatMediaPolicyConditions.
        :type: list[User]
        """
        

        self._for_users = for_users

    @property
    def date_ranges(self):
        """
        Gets the date_ranges of this ChatMediaPolicyConditions.


        :return: The date_ranges of this ChatMediaPolicyConditions.
        :rtype: list[str]
        """
        return self._date_ranges

    @date_ranges.setter
    def date_ranges(self, date_ranges):
        """
        Sets the date_ranges of this ChatMediaPolicyConditions.


        :param date_ranges: The date_ranges of this ChatMediaPolicyConditions.
        :type: list[str]
        """
        

        self._date_ranges = date_ranges

    @property
    def for_queues(self):
        """
        Gets the for_queues of this ChatMediaPolicyConditions.


        :return: The for_queues of this ChatMediaPolicyConditions.
        :rtype: list[Queue]
        """
        return self._for_queues

    @for_queues.setter
    def for_queues(self, for_queues):
        """
        Sets the for_queues of this ChatMediaPolicyConditions.


        :param for_queues: The for_queues of this ChatMediaPolicyConditions.
        :type: list[Queue]
        """
        

        self._for_queues = for_queues

    @property
    def wrapup_codes(self):
        """
        Gets the wrapup_codes of this ChatMediaPolicyConditions.


        :return: The wrapup_codes of this ChatMediaPolicyConditions.
        :rtype: list[WrapupCode]
        """
        return self._wrapup_codes

    @wrapup_codes.setter
    def wrapup_codes(self, wrapup_codes):
        """
        Sets the wrapup_codes of this ChatMediaPolicyConditions.


        :param wrapup_codes: The wrapup_codes of this ChatMediaPolicyConditions.
        :type: list[WrapupCode]
        """
        

        self._wrapup_codes = wrapup_codes

    @property
    def languages(self):
        """
        Gets the languages of this ChatMediaPolicyConditions.


        :return: The languages of this ChatMediaPolicyConditions.
        :rtype: list[Language]
        """
        return self._languages

    @languages.setter
    def languages(self, languages):
        """
        Sets the languages of this ChatMediaPolicyConditions.


        :param languages: The languages of this ChatMediaPolicyConditions.
        :type: list[Language]
        """
        

        self._languages = languages

    @property
    def time_allowed(self):
        """
        Gets the time_allowed of this ChatMediaPolicyConditions.


        :return: The time_allowed of this ChatMediaPolicyConditions.
        :rtype: TimeAllowed
        """
        return self._time_allowed

    @time_allowed.setter
    def time_allowed(self, time_allowed):
        """
        Sets the time_allowed of this ChatMediaPolicyConditions.


        :param time_allowed: The time_allowed of this ChatMediaPolicyConditions.
        :type: TimeAllowed
        """
        

        self._time_allowed = time_allowed

    @property
    def duration(self):
        """
        Gets the duration of this ChatMediaPolicyConditions.


        :return: The duration of this ChatMediaPolicyConditions.
        :rtype: DurationCondition
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """
        Sets the duration of this ChatMediaPolicyConditions.


        :param duration: The duration of this ChatMediaPolicyConditions.
        :type: DurationCondition
        """
        

        self._duration = duration

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

