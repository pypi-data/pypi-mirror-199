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

class BuAgentScheduleShift(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuAgentScheduleShift - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'start_date': 'datetime',
            'length_minutes': 'int',
            'activities': 'list[BuAgentScheduleActivity]',
            'manually_edited': 'bool',
            'schedule': 'BuScheduleReference'
        }

        self.attribute_map = {
            'id': 'id',
            'start_date': 'startDate',
            'length_minutes': 'lengthMinutes',
            'activities': 'activities',
            'manually_edited': 'manuallyEdited',
            'schedule': 'schedule'
        }

        self._id = None
        self._start_date = None
        self._length_minutes = None
        self._activities = None
        self._manually_edited = None
        self._schedule = None

    @property
    def id(self):
        """
        Gets the id of this BuAgentScheduleShift.
        The ID of the shift

        :return: The id of this BuAgentScheduleShift.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this BuAgentScheduleShift.
        The ID of the shift

        :param id: The id of this BuAgentScheduleShift.
        :type: str
        """
        

        self._id = id

    @property
    def start_date(self):
        """
        Gets the start_date of this BuAgentScheduleShift.
        The start date of this shift. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The start_date of this BuAgentScheduleShift.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this BuAgentScheduleShift.
        The start date of this shift. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param start_date: The start_date of this BuAgentScheduleShift.
        :type: datetime
        """
        

        self._start_date = start_date

    @property
    def length_minutes(self):
        """
        Gets the length_minutes of this BuAgentScheduleShift.
        The length of this shift in minutes

        :return: The length_minutes of this BuAgentScheduleShift.
        :rtype: int
        """
        return self._length_minutes

    @length_minutes.setter
    def length_minutes(self, length_minutes):
        """
        Sets the length_minutes of this BuAgentScheduleShift.
        The length of this shift in minutes

        :param length_minutes: The length_minutes of this BuAgentScheduleShift.
        :type: int
        """
        

        self._length_minutes = length_minutes

    @property
    def activities(self):
        """
        Gets the activities of this BuAgentScheduleShift.
        The activities associated with this shift

        :return: The activities of this BuAgentScheduleShift.
        :rtype: list[BuAgentScheduleActivity]
        """
        return self._activities

    @activities.setter
    def activities(self, activities):
        """
        Sets the activities of this BuAgentScheduleShift.
        The activities associated with this shift

        :param activities: The activities of this BuAgentScheduleShift.
        :type: list[BuAgentScheduleActivity]
        """
        

        self._activities = activities

    @property
    def manually_edited(self):
        """
        Gets the manually_edited of this BuAgentScheduleShift.
        Whether this shift was manually edited. This is only set by clients and is used for rescheduling

        :return: The manually_edited of this BuAgentScheduleShift.
        :rtype: bool
        """
        return self._manually_edited

    @manually_edited.setter
    def manually_edited(self, manually_edited):
        """
        Sets the manually_edited of this BuAgentScheduleShift.
        Whether this shift was manually edited. This is only set by clients and is used for rescheduling

        :param manually_edited: The manually_edited of this BuAgentScheduleShift.
        :type: bool
        """
        

        self._manually_edited = manually_edited

    @property
    def schedule(self):
        """
        Gets the schedule of this BuAgentScheduleShift.
        The schedule to which this shift belongs

        :return: The schedule of this BuAgentScheduleShift.
        :rtype: BuScheduleReference
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """
        Sets the schedule of this BuAgentScheduleShift.
        The schedule to which this shift belongs

        :param schedule: The schedule of this BuAgentScheduleShift.
        :type: BuScheduleReference
        """
        

        self._schedule = schedule

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

