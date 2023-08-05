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

class CreateManagementUnitSettingsRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CreateManagementUnitSettingsRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'adherence': 'AdherenceSettings',
            'short_term_forecasting': 'ShortTermForecastingSettings',
            'time_off': 'TimeOffRequestSettings',
            'scheduling': 'SchedulingSettingsRequest',
            'shift_trading': 'ShiftTradeSettings'
        }

        self.attribute_map = {
            'adherence': 'adherence',
            'short_term_forecasting': 'shortTermForecasting',
            'time_off': 'timeOff',
            'scheduling': 'scheduling',
            'shift_trading': 'shiftTrading'
        }

        self._adherence = None
        self._short_term_forecasting = None
        self._time_off = None
        self._scheduling = None
        self._shift_trading = None

    @property
    def adherence(self):
        """
        Gets the adherence of this CreateManagementUnitSettingsRequest.
        Adherence settings for this management unit

        :return: The adherence of this CreateManagementUnitSettingsRequest.
        :rtype: AdherenceSettings
        """
        return self._adherence

    @adherence.setter
    def adherence(self, adherence):
        """
        Sets the adherence of this CreateManagementUnitSettingsRequest.
        Adherence settings for this management unit

        :param adherence: The adherence of this CreateManagementUnitSettingsRequest.
        :type: AdherenceSettings
        """
        

        self._adherence = adherence

    @property
    def short_term_forecasting(self):
        """
        Gets the short_term_forecasting of this CreateManagementUnitSettingsRequest.
        Short term forecasting settings for this management unit.  Moving to Business Unit

        :return: The short_term_forecasting of this CreateManagementUnitSettingsRequest.
        :rtype: ShortTermForecastingSettings
        """
        return self._short_term_forecasting

    @short_term_forecasting.setter
    def short_term_forecasting(self, short_term_forecasting):
        """
        Sets the short_term_forecasting of this CreateManagementUnitSettingsRequest.
        Short term forecasting settings for this management unit.  Moving to Business Unit

        :param short_term_forecasting: The short_term_forecasting of this CreateManagementUnitSettingsRequest.
        :type: ShortTermForecastingSettings
        """
        

        self._short_term_forecasting = short_term_forecasting

    @property
    def time_off(self):
        """
        Gets the time_off of this CreateManagementUnitSettingsRequest.
        Time off request settings for this management unit

        :return: The time_off of this CreateManagementUnitSettingsRequest.
        :rtype: TimeOffRequestSettings
        """
        return self._time_off

    @time_off.setter
    def time_off(self, time_off):
        """
        Sets the time_off of this CreateManagementUnitSettingsRequest.
        Time off request settings for this management unit

        :param time_off: The time_off of this CreateManagementUnitSettingsRequest.
        :type: TimeOffRequestSettings
        """
        

        self._time_off = time_off

    @property
    def scheduling(self):
        """
        Gets the scheduling of this CreateManagementUnitSettingsRequest.
        Scheduling settings for this management unit

        :return: The scheduling of this CreateManagementUnitSettingsRequest.
        :rtype: SchedulingSettingsRequest
        """
        return self._scheduling

    @scheduling.setter
    def scheduling(self, scheduling):
        """
        Sets the scheduling of this CreateManagementUnitSettingsRequest.
        Scheduling settings for this management unit

        :param scheduling: The scheduling of this CreateManagementUnitSettingsRequest.
        :type: SchedulingSettingsRequest
        """
        

        self._scheduling = scheduling

    @property
    def shift_trading(self):
        """
        Gets the shift_trading of this CreateManagementUnitSettingsRequest.
        Shift trade settings for this management unit

        :return: The shift_trading of this CreateManagementUnitSettingsRequest.
        :rtype: ShiftTradeSettings
        """
        return self._shift_trading

    @shift_trading.setter
    def shift_trading(self, shift_trading):
        """
        Sets the shift_trading of this CreateManagementUnitSettingsRequest.
        Shift trade settings for this management unit

        :param shift_trading: The shift_trading of this CreateManagementUnitSettingsRequest.
        :type: ShiftTradeSettings
        """
        

        self._shift_trading = shift_trading

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

