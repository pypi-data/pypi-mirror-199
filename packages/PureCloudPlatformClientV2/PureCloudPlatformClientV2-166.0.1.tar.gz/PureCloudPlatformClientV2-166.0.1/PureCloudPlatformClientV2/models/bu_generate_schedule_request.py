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

class BuGenerateScheduleRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuGenerateScheduleRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'description': 'str',
            'short_term_forecast': 'BuShortTermForecastReference',
            'week_count': 'int',
            'options': 'SchedulingOptionsRequest'
        }

        self.attribute_map = {
            'description': 'description',
            'short_term_forecast': 'shortTermForecast',
            'week_count': 'weekCount',
            'options': 'options'
        }

        self._description = None
        self._short_term_forecast = None
        self._week_count = None
        self._options = None

    @property
    def description(self):
        """
        Gets the description of this BuGenerateScheduleRequest.
        The description for the schedule

        :return: The description of this BuGenerateScheduleRequest.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this BuGenerateScheduleRequest.
        The description for the schedule

        :param description: The description of this BuGenerateScheduleRequest.
        :type: str
        """
        

        self._description = description

    @property
    def short_term_forecast(self):
        """
        Gets the short_term_forecast of this BuGenerateScheduleRequest.
        The forecast to use when generating the schedule.  Note that the forecast must fully encompass the schedule's start week + week count

        :return: The short_term_forecast of this BuGenerateScheduleRequest.
        :rtype: BuShortTermForecastReference
        """
        return self._short_term_forecast

    @short_term_forecast.setter
    def short_term_forecast(self, short_term_forecast):
        """
        Sets the short_term_forecast of this BuGenerateScheduleRequest.
        The forecast to use when generating the schedule.  Note that the forecast must fully encompass the schedule's start week + week count

        :param short_term_forecast: The short_term_forecast of this BuGenerateScheduleRequest.
        :type: BuShortTermForecastReference
        """
        

        self._short_term_forecast = short_term_forecast

    @property
    def week_count(self):
        """
        Gets the week_count of this BuGenerateScheduleRequest.
        The number of weeks in the schedule. One extra day is added at the end

        :return: The week_count of this BuGenerateScheduleRequest.
        :rtype: int
        """
        return self._week_count

    @week_count.setter
    def week_count(self, week_count):
        """
        Sets the week_count of this BuGenerateScheduleRequest.
        The number of weeks in the schedule. One extra day is added at the end

        :param week_count: The week_count of this BuGenerateScheduleRequest.
        :type: int
        """
        

        self._week_count = week_count

    @property
    def options(self):
        """
        Gets the options of this BuGenerateScheduleRequest.
        Additional scheduling options

        :return: The options of this BuGenerateScheduleRequest.
        :rtype: SchedulingOptionsRequest
        """
        return self._options

    @options.setter
    def options(self, options):
        """
        Sets the options of this BuGenerateScheduleRequest.
        Additional scheduling options

        :param options: The options of this BuGenerateScheduleRequest.
        :type: SchedulingOptionsRequest
        """
        

        self._options = options

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

