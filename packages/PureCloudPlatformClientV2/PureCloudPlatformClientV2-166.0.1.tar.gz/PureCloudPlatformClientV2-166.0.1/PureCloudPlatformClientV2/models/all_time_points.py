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

class AllTimePoints(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AllTimePoints - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'user': 'UserReference',
            'date_end_workday': 'date',
            'all_time_points': 'int'
        }

        self.attribute_map = {
            'user': 'user',
            'date_end_workday': 'dateEndWorkday',
            'all_time_points': 'allTimePoints'
        }

        self._user = None
        self._date_end_workday = None
        self._all_time_points = None

    @property
    def user(self):
        """
        Gets the user of this AllTimePoints.
        Queried user

        :return: The user of this AllTimePoints.
        :rtype: UserReference
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this AllTimePoints.
        Queried user

        :param user: The user of this AllTimePoints.
        :type: UserReference
        """
        

        self._user = user

    @property
    def date_end_workday(self):
        """
        Gets the date_end_workday of this AllTimePoints.
        Queried end workday for all time points to be collected. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :return: The date_end_workday of this AllTimePoints.
        :rtype: date
        """
        return self._date_end_workday

    @date_end_workday.setter
    def date_end_workday(self, date_end_workday):
        """
        Sets the date_end_workday of this AllTimePoints.
        Queried end workday for all time points to be collected. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :param date_end_workday: The date_end_workday of this AllTimePoints.
        :type: date
        """
        

        self._date_end_workday = date_end_workday

    @property
    def all_time_points(self):
        """
        Gets the all_time_points of this AllTimePoints.
        All time point collected bt the user

        :return: The all_time_points of this AllTimePoints.
        :rtype: int
        """
        return self._all_time_points

    @all_time_points.setter
    def all_time_points(self, all_time_points):
        """
        Sets the all_time_points of this AllTimePoints.
        All time point collected bt the user

        :param all_time_points: The all_time_points of this AllTimePoints.
        :type: int
        """
        

        self._all_time_points = all_time_points

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

