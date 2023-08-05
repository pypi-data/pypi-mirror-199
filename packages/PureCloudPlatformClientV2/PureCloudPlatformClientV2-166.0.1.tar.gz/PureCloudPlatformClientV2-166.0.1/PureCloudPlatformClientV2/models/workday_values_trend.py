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

class WorkdayValuesTrend(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WorkdayValuesTrend - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'date_start_workday': 'date',
            'date_end_workday': 'date',
            'date_reference_workday': 'date',
            'division': 'Division',
            'user': 'UserReference',
            'timezone': 'str',
            'results': 'list[WorkdayValuesMetricItem]',
            'performance_profile': 'AddressableEntityRef',
            'metric': 'AddressableEntityRef'
        }

        self.attribute_map = {
            'date_start_workday': 'dateStartWorkday',
            'date_end_workday': 'dateEndWorkday',
            'date_reference_workday': 'dateReferenceWorkday',
            'division': 'division',
            'user': 'user',
            'timezone': 'timezone',
            'results': 'results',
            'performance_profile': 'performanceProfile',
            'metric': 'metric'
        }

        self._date_start_workday = None
        self._date_end_workday = None
        self._date_reference_workday = None
        self._division = None
        self._user = None
        self._timezone = None
        self._results = None
        self._performance_profile = None
        self._metric = None

    @property
    def date_start_workday(self):
        """
        Gets the date_start_workday of this WorkdayValuesTrend.
        The start workday for the query range for the metric value trend. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :return: The date_start_workday of this WorkdayValuesTrend.
        :rtype: date
        """
        return self._date_start_workday

    @date_start_workday.setter
    def date_start_workday(self, date_start_workday):
        """
        Sets the date_start_workday of this WorkdayValuesTrend.
        The start workday for the query range for the metric value trend. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :param date_start_workday: The date_start_workday of this WorkdayValuesTrend.
        :type: date
        """
        

        self._date_start_workday = date_start_workday

    @property
    def date_end_workday(self):
        """
        Gets the date_end_workday of this WorkdayValuesTrend.
        The end workday for the query range for the metric value trend. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :return: The date_end_workday of this WorkdayValuesTrend.
        :rtype: date
        """
        return self._date_end_workday

    @date_end_workday.setter
    def date_end_workday(self, date_end_workday):
        """
        Sets the date_end_workday of this WorkdayValuesTrend.
        The end workday for the query range for the metric value trend. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :param date_end_workday: The date_end_workday of this WorkdayValuesTrend.
        :type: date
        """
        

        self._date_end_workday = date_end_workday

    @property
    def date_reference_workday(self):
        """
        Gets the date_reference_workday of this WorkdayValuesTrend.
        The reference workday used to determine the metric definition. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :return: The date_reference_workday of this WorkdayValuesTrend.
        :rtype: date
        """
        return self._date_reference_workday

    @date_reference_workday.setter
    def date_reference_workday(self, date_reference_workday):
        """
        Sets the date_reference_workday of this WorkdayValuesTrend.
        The reference workday used to determine the metric definition. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :param date_reference_workday: The date_reference_workday of this WorkdayValuesTrend.
        :type: date
        """
        

        self._date_reference_workday = date_reference_workday

    @property
    def division(self):
        """
        Gets the division of this WorkdayValuesTrend.
        The targeted division for the query

        :return: The division of this WorkdayValuesTrend.
        :rtype: Division
        """
        return self._division

    @division.setter
    def division(self, division):
        """
        Sets the division of this WorkdayValuesTrend.
        The targeted division for the query

        :param division: The division of this WorkdayValuesTrend.
        :type: Division
        """
        

        self._division = division

    @property
    def user(self):
        """
        Gets the user of this WorkdayValuesTrend.
        The targeted user for the query

        :return: The user of this WorkdayValuesTrend.
        :rtype: UserReference
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this WorkdayValuesTrend.
        The targeted user for the query

        :param user: The user of this WorkdayValuesTrend.
        :type: UserReference
        """
        

        self._user = user

    @property
    def timezone(self):
        """
        Gets the timezone of this WorkdayValuesTrend.
        The time zone used for aggregating metric values

        :return: The timezone of this WorkdayValuesTrend.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """
        Sets the timezone of this WorkdayValuesTrend.
        The time zone used for aggregating metric values

        :param timezone: The timezone of this WorkdayValuesTrend.
        :type: str
        """
        

        self._timezone = timezone

    @property
    def results(self):
        """
        Gets the results of this WorkdayValuesTrend.
        The metric value trends

        :return: The results of this WorkdayValuesTrend.
        :rtype: list[WorkdayValuesMetricItem]
        """
        return self._results

    @results.setter
    def results(self, results):
        """
        Sets the results of this WorkdayValuesTrend.
        The metric value trends

        :param results: The results of this WorkdayValuesTrend.
        :type: list[WorkdayValuesMetricItem]
        """
        

        self._results = results

    @property
    def performance_profile(self):
        """
        Gets the performance_profile of this WorkdayValuesTrend.
        The targeted performance profile for the average points

        :return: The performance_profile of this WorkdayValuesTrend.
        :rtype: AddressableEntityRef
        """
        return self._performance_profile

    @performance_profile.setter
    def performance_profile(self, performance_profile):
        """
        Sets the performance_profile of this WorkdayValuesTrend.
        The targeted performance profile for the average points

        :param performance_profile: The performance_profile of this WorkdayValuesTrend.
        :type: AddressableEntityRef
        """
        

        self._performance_profile = performance_profile

    @property
    def metric(self):
        """
        Gets the metric of this WorkdayValuesTrend.
        The targeted metric for the average points

        :return: The metric of this WorkdayValuesTrend.
        :rtype: AddressableEntityRef
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """
        Sets the metric of this WorkdayValuesTrend.
        The targeted metric for the average points

        :param metric: The metric of this WorkdayValuesTrend.
        :type: AddressableEntityRef
        """
        

        self._metric = metric

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

