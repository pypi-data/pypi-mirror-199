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

class WfmAgentScheduleUpdateTopicWfmScheduleActivity(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WfmAgentScheduleUpdateTopicWfmScheduleActivity - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'activity_code_id': 'str',
            'start_date': 'datetime',
            'counts_as_paid_time': 'bool',
            'length_in_minutes': 'int',
            'time_off_request_id': 'str',
            'description': 'str'
        }

        self.attribute_map = {
            'activity_code_id': 'activityCodeId',
            'start_date': 'startDate',
            'counts_as_paid_time': 'countsAsPaidTime',
            'length_in_minutes': 'lengthInMinutes',
            'time_off_request_id': 'timeOffRequestId',
            'description': 'description'
        }

        self._activity_code_id = None
        self._start_date = None
        self._counts_as_paid_time = None
        self._length_in_minutes = None
        self._time_off_request_id = None
        self._description = None

    @property
    def activity_code_id(self):
        """
        Gets the activity_code_id of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :return: The activity_code_id of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :rtype: str
        """
        return self._activity_code_id

    @activity_code_id.setter
    def activity_code_id(self, activity_code_id):
        """
        Sets the activity_code_id of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :param activity_code_id: The activity_code_id of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :type: str
        """
        

        self._activity_code_id = activity_code_id

    @property
    def start_date(self):
        """
        Gets the start_date of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :return: The start_date of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :param start_date: The start_date of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :type: datetime
        """
        

        self._start_date = start_date

    @property
    def counts_as_paid_time(self):
        """
        Gets the counts_as_paid_time of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :return: The counts_as_paid_time of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :rtype: bool
        """
        return self._counts_as_paid_time

    @counts_as_paid_time.setter
    def counts_as_paid_time(self, counts_as_paid_time):
        """
        Sets the counts_as_paid_time of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :param counts_as_paid_time: The counts_as_paid_time of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :type: bool
        """
        

        self._counts_as_paid_time = counts_as_paid_time

    @property
    def length_in_minutes(self):
        """
        Gets the length_in_minutes of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :return: The length_in_minutes of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :rtype: int
        """
        return self._length_in_minutes

    @length_in_minutes.setter
    def length_in_minutes(self, length_in_minutes):
        """
        Sets the length_in_minutes of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :param length_in_minutes: The length_in_minutes of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :type: int
        """
        

        self._length_in_minutes = length_in_minutes

    @property
    def time_off_request_id(self):
        """
        Gets the time_off_request_id of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :return: The time_off_request_id of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :rtype: str
        """
        return self._time_off_request_id

    @time_off_request_id.setter
    def time_off_request_id(self, time_off_request_id):
        """
        Sets the time_off_request_id of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :param time_off_request_id: The time_off_request_id of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :type: str
        """
        

        self._time_off_request_id = time_off_request_id

    @property
    def description(self):
        """
        Gets the description of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :return: The description of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.


        :param description: The description of this WfmAgentScheduleUpdateTopicWfmScheduleActivity.
        :type: str
        """
        

        self._description = description

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

