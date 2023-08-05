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

class SingleWorkdayAverageValues(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SingleWorkdayAverageValues - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'date_workday': 'date',
            'division': 'Division',
            'user': 'UserReference',
            'timezone': 'str',
            'results': 'list[WorkdayValuesMetricItem]',
            'performance_profile': 'AddressableEntityRef'
        }

        self.attribute_map = {
            'date_workday': 'dateWorkday',
            'division': 'division',
            'user': 'user',
            'timezone': 'timezone',
            'results': 'results',
            'performance_profile': 'performanceProfile'
        }

        self._date_workday = None
        self._division = None
        self._user = None
        self._timezone = None
        self._results = None
        self._performance_profile = None

    @property
    def date_workday(self):
        """
        Gets the date_workday of this SingleWorkdayAverageValues.
        The targeted workday for average value query. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :return: The date_workday of this SingleWorkdayAverageValues.
        :rtype: date
        """
        return self._date_workday

    @date_workday.setter
    def date_workday(self, date_workday):
        """
        Sets the date_workday of this SingleWorkdayAverageValues.
        The targeted workday for average value query. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :param date_workday: The date_workday of this SingleWorkdayAverageValues.
        :type: date
        """
        

        self._date_workday = date_workday

    @property
    def division(self):
        """
        Gets the division of this SingleWorkdayAverageValues.
        The targeted division for the metrics

        :return: The division of this SingleWorkdayAverageValues.
        :rtype: Division
        """
        return self._division

    @division.setter
    def division(self, division):
        """
        Sets the division of this SingleWorkdayAverageValues.
        The targeted division for the metrics

        :param division: The division of this SingleWorkdayAverageValues.
        :type: Division
        """
        

        self._division = division

    @property
    def user(self):
        """
        Gets the user of this SingleWorkdayAverageValues.
        The targeted user for the metrics

        :return: The user of this SingleWorkdayAverageValues.
        :rtype: UserReference
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this SingleWorkdayAverageValues.
        The targeted user for the metrics

        :param user: The user of this SingleWorkdayAverageValues.
        :type: UserReference
        """
        

        self._user = user

    @property
    def timezone(self):
        """
        Gets the timezone of this SingleWorkdayAverageValues.
        The time zone used for aggregating metric values

        :return: The timezone of this SingleWorkdayAverageValues.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """
        Sets the timezone of this SingleWorkdayAverageValues.
        The time zone used for aggregating metric values

        :param timezone: The timezone of this SingleWorkdayAverageValues.
        :type: str
        """
        

        self._timezone = timezone

    @property
    def results(self):
        """
        Gets the results of this SingleWorkdayAverageValues.
        The metric value averages

        :return: The results of this SingleWorkdayAverageValues.
        :rtype: list[WorkdayValuesMetricItem]
        """
        return self._results

    @results.setter
    def results(self, results):
        """
        Sets the results of this SingleWorkdayAverageValues.
        The metric value averages

        :param results: The results of this SingleWorkdayAverageValues.
        :type: list[WorkdayValuesMetricItem]
        """
        

        self._results = results

    @property
    def performance_profile(self):
        """
        Gets the performance_profile of this SingleWorkdayAverageValues.
        The targeted performance profile for the average points

        :return: The performance_profile of this SingleWorkdayAverageValues.
        :rtype: AddressableEntityRef
        """
        return self._performance_profile

    @performance_profile.setter
    def performance_profile(self, performance_profile):
        """
        Sets the performance_profile of this SingleWorkdayAverageValues.
        The targeted performance profile for the average points

        :param performance_profile: The performance_profile of this SingleWorkdayAverageValues.
        :type: AddressableEntityRef
        """
        

        self._performance_profile = performance_profile

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

