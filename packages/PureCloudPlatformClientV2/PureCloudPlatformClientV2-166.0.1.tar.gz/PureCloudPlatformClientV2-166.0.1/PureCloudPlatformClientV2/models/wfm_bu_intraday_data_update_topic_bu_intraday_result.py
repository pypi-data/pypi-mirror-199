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

class WfmBuIntradayDataUpdateTopicBuIntradayResult(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WfmBuIntradayDataUpdateTopicBuIntradayResult - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'start_date': 'datetime',
            'end_date': 'datetime',
            'interval_length_minutes': 'int',
            'intraday_data_groupings': 'list[WfmBuIntradayDataUpdateTopicBuIntradayDataGroup]',
            'categories': 'list[str]',
            'no_data_reason': 'str',
            'schedule': 'WfmBuIntradayDataUpdateTopicBuScheduleReference',
            'short_term_forecast': 'WfmBuIntradayDataUpdateTopicBuShortTermForecastReference'
        }

        self.attribute_map = {
            'start_date': 'startDate',
            'end_date': 'endDate',
            'interval_length_minutes': 'intervalLengthMinutes',
            'intraday_data_groupings': 'intradayDataGroupings',
            'categories': 'categories',
            'no_data_reason': 'noDataReason',
            'schedule': 'schedule',
            'short_term_forecast': 'shortTermForecast'
        }

        self._start_date = None
        self._end_date = None
        self._interval_length_minutes = None
        self._intraday_data_groupings = None
        self._categories = None
        self._no_data_reason = None
        self._schedule = None
        self._short_term_forecast = None

    @property
    def start_date(self):
        """
        Gets the start_date of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :return: The start_date of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :param start_date: The start_date of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :type: datetime
        """
        

        self._start_date = start_date

    @property
    def end_date(self):
        """
        Gets the end_date of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :return: The end_date of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Sets the end_date of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :param end_date: The end_date of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :type: datetime
        """
        

        self._end_date = end_date

    @property
    def interval_length_minutes(self):
        """
        Gets the interval_length_minutes of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :return: The interval_length_minutes of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :rtype: int
        """
        return self._interval_length_minutes

    @interval_length_minutes.setter
    def interval_length_minutes(self, interval_length_minutes):
        """
        Sets the interval_length_minutes of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :param interval_length_minutes: The interval_length_minutes of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :type: int
        """
        

        self._interval_length_minutes = interval_length_minutes

    @property
    def intraday_data_groupings(self):
        """
        Gets the intraday_data_groupings of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :return: The intraday_data_groupings of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :rtype: list[WfmBuIntradayDataUpdateTopicBuIntradayDataGroup]
        """
        return self._intraday_data_groupings

    @intraday_data_groupings.setter
    def intraday_data_groupings(self, intraday_data_groupings):
        """
        Sets the intraday_data_groupings of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :param intraday_data_groupings: The intraday_data_groupings of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :type: list[WfmBuIntradayDataUpdateTopicBuIntradayDataGroup]
        """
        

        self._intraday_data_groupings = intraday_data_groupings

    @property
    def categories(self):
        """
        Gets the categories of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :return: The categories of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :rtype: list[str]
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """
        Sets the categories of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :param categories: The categories of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :type: list[str]
        """
        

        self._categories = categories

    @property
    def no_data_reason(self):
        """
        Gets the no_data_reason of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :return: The no_data_reason of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :rtype: str
        """
        return self._no_data_reason

    @no_data_reason.setter
    def no_data_reason(self, no_data_reason):
        """
        Sets the no_data_reason of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :param no_data_reason: The no_data_reason of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :type: str
        """
        

        self._no_data_reason = no_data_reason

    @property
    def schedule(self):
        """
        Gets the schedule of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :return: The schedule of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :rtype: WfmBuIntradayDataUpdateTopicBuScheduleReference
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """
        Sets the schedule of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :param schedule: The schedule of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :type: WfmBuIntradayDataUpdateTopicBuScheduleReference
        """
        

        self._schedule = schedule

    @property
    def short_term_forecast(self):
        """
        Gets the short_term_forecast of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :return: The short_term_forecast of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :rtype: WfmBuIntradayDataUpdateTopicBuShortTermForecastReference
        """
        return self._short_term_forecast

    @short_term_forecast.setter
    def short_term_forecast(self, short_term_forecast):
        """
        Sets the short_term_forecast of this WfmBuIntradayDataUpdateTopicBuIntradayResult.


        :param short_term_forecast: The short_term_forecast of this WfmBuIntradayDataUpdateTopicBuIntradayResult.
        :type: WfmBuIntradayDataUpdateTopicBuShortTermForecastReference
        """
        

        self._short_term_forecast = short_term_forecast

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

