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

class BuAgentScheduleUpdate(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuAgentScheduleUpdate - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'type': 'str',
            'shift_start_dates': 'list[datetime]'
        }

        self.attribute_map = {
            'type': 'type',
            'shift_start_dates': 'shiftStartDates'
        }

        self._type = None
        self._shift_start_dates = None

    @property
    def type(self):
        """
        Gets the type of this BuAgentScheduleUpdate.
        The type of update

        :return: The type of this BuAgentScheduleUpdate.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this BuAgentScheduleUpdate.
        The type of update

        :param type: The type of this BuAgentScheduleUpdate.
        :type: str
        """
        allowed_values = ["Added", "Edited", "Deleted"]
        if type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for type -> " + type)
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def shift_start_dates(self):
        """
        Gets the shift_start_dates of this BuAgentScheduleUpdate.
        The start date for the affected shifts

        :return: The shift_start_dates of this BuAgentScheduleUpdate.
        :rtype: list[datetime]
        """
        return self._shift_start_dates

    @shift_start_dates.setter
    def shift_start_dates(self, shift_start_dates):
        """
        Sets the shift_start_dates of this BuAgentScheduleUpdate.
        The start date for the affected shifts

        :param shift_start_dates: The shift_start_dates of this BuAgentScheduleUpdate.
        :type: list[datetime]
        """
        

        self._shift_start_dates = shift_start_dates

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

