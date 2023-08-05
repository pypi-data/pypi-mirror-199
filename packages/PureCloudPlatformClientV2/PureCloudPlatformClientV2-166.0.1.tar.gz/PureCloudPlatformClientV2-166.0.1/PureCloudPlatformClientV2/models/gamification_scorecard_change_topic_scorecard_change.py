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

class GamificationScorecardChangeTopicScorecardChange(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        GamificationScorecardChangeTopicScorecardChange - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'workday': 'str',
            'division_id': 'str',
            'team_id': 'str',
            'performance_profile_id': 'str',
            'user_id': 'str',
            'performance_metrics': 'list[GamificationScorecardChangeTopicPerformanceMetric]'
        }

        self.attribute_map = {
            'workday': 'workday',
            'division_id': 'divisionId',
            'team_id': 'teamId',
            'performance_profile_id': 'performanceProfileId',
            'user_id': 'userId',
            'performance_metrics': 'performanceMetrics'
        }

        self._workday = None
        self._division_id = None
        self._team_id = None
        self._performance_profile_id = None
        self._user_id = None
        self._performance_metrics = None

    @property
    def workday(self):
        """
        Gets the workday of this GamificationScorecardChangeTopicScorecardChange.


        :return: The workday of this GamificationScorecardChangeTopicScorecardChange.
        :rtype: str
        """
        return self._workday

    @workday.setter
    def workday(self, workday):
        """
        Sets the workday of this GamificationScorecardChangeTopicScorecardChange.


        :param workday: The workday of this GamificationScorecardChangeTopicScorecardChange.
        :type: str
        """
        

        self._workday = workday

    @property
    def division_id(self):
        """
        Gets the division_id of this GamificationScorecardChangeTopicScorecardChange.


        :return: The division_id of this GamificationScorecardChangeTopicScorecardChange.
        :rtype: str
        """
        return self._division_id

    @division_id.setter
    def division_id(self, division_id):
        """
        Sets the division_id of this GamificationScorecardChangeTopicScorecardChange.


        :param division_id: The division_id of this GamificationScorecardChangeTopicScorecardChange.
        :type: str
        """
        

        self._division_id = division_id

    @property
    def team_id(self):
        """
        Gets the team_id of this GamificationScorecardChangeTopicScorecardChange.


        :return: The team_id of this GamificationScorecardChangeTopicScorecardChange.
        :rtype: str
        """
        return self._team_id

    @team_id.setter
    def team_id(self, team_id):
        """
        Sets the team_id of this GamificationScorecardChangeTopicScorecardChange.


        :param team_id: The team_id of this GamificationScorecardChangeTopicScorecardChange.
        :type: str
        """
        

        self._team_id = team_id

    @property
    def performance_profile_id(self):
        """
        Gets the performance_profile_id of this GamificationScorecardChangeTopicScorecardChange.


        :return: The performance_profile_id of this GamificationScorecardChangeTopicScorecardChange.
        :rtype: str
        """
        return self._performance_profile_id

    @performance_profile_id.setter
    def performance_profile_id(self, performance_profile_id):
        """
        Sets the performance_profile_id of this GamificationScorecardChangeTopicScorecardChange.


        :param performance_profile_id: The performance_profile_id of this GamificationScorecardChangeTopicScorecardChange.
        :type: str
        """
        

        self._performance_profile_id = performance_profile_id

    @property
    def user_id(self):
        """
        Gets the user_id of this GamificationScorecardChangeTopicScorecardChange.


        :return: The user_id of this GamificationScorecardChangeTopicScorecardChange.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this GamificationScorecardChangeTopicScorecardChange.


        :param user_id: The user_id of this GamificationScorecardChangeTopicScorecardChange.
        :type: str
        """
        

        self._user_id = user_id

    @property
    def performance_metrics(self):
        """
        Gets the performance_metrics of this GamificationScorecardChangeTopicScorecardChange.


        :return: The performance_metrics of this GamificationScorecardChangeTopicScorecardChange.
        :rtype: list[GamificationScorecardChangeTopicPerformanceMetric]
        """
        return self._performance_metrics

    @performance_metrics.setter
    def performance_metrics(self, performance_metrics):
        """
        Sets the performance_metrics of this GamificationScorecardChangeTopicScorecardChange.


        :param performance_metrics: The performance_metrics of this GamificationScorecardChangeTopicScorecardChange.
        :type: list[GamificationScorecardChangeTopicPerformanceMetric]
        """
        

        self._performance_metrics = performance_metrics

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

