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

class LearningSlotWfmScheduleActivity(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        LearningSlotWfmScheduleActivity - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'user': 'UserReference',
            'activities': 'list[LearningSlotScheduleActivity]',
            'full_day_time_off_markers': 'list[LearningSlotFullDayTimeOffMarker]'
        }

        self.attribute_map = {
            'user': 'user',
            'activities': 'activities',
            'full_day_time_off_markers': 'fullDayTimeOffMarkers'
        }

        self._user = None
        self._activities = None
        self._full_day_time_off_markers = None

    @property
    def user(self):
        """
        Gets the user of this LearningSlotWfmScheduleActivity.
        User that the schedule is for

        :return: The user of this LearningSlotWfmScheduleActivity.
        :rtype: UserReference
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this LearningSlotWfmScheduleActivity.
        User that the schedule is for

        :param user: The user of this LearningSlotWfmScheduleActivity.
        :type: UserReference
        """
        

        self._user = user

    @property
    def activities(self):
        """
        Gets the activities of this LearningSlotWfmScheduleActivity.
        List of user's scheduled activities

        :return: The activities of this LearningSlotWfmScheduleActivity.
        :rtype: list[LearningSlotScheduleActivity]
        """
        return self._activities

    @activities.setter
    def activities(self, activities):
        """
        Sets the activities of this LearningSlotWfmScheduleActivity.
        List of user's scheduled activities

        :param activities: The activities of this LearningSlotWfmScheduleActivity.
        :type: list[LearningSlotScheduleActivity]
        """
        

        self._activities = activities

    @property
    def full_day_time_off_markers(self):
        """
        Gets the full_day_time_off_markers of this LearningSlotWfmScheduleActivity.
        List of user's days off

        :return: The full_day_time_off_markers of this LearningSlotWfmScheduleActivity.
        :rtype: list[LearningSlotFullDayTimeOffMarker]
        """
        return self._full_day_time_off_markers

    @full_day_time_off_markers.setter
    def full_day_time_off_markers(self, full_day_time_off_markers):
        """
        Sets the full_day_time_off_markers of this LearningSlotWfmScheduleActivity.
        List of user's days off

        :param full_day_time_off_markers: The full_day_time_off_markers of this LearningSlotWfmScheduleActivity.
        :type: list[LearningSlotFullDayTimeOffMarker]
        """
        

        self._full_day_time_off_markers = full_day_time_off_markers

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

