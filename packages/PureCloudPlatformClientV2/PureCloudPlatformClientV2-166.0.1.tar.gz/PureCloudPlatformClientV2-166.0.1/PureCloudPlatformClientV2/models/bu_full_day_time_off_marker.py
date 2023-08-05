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

class BuFullDayTimeOffMarker(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuFullDayTimeOffMarker - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'business_unit_date': 'date',
            'length_minutes': 'int',
            'description': 'str',
            'activity_code_id': 'str',
            'paid': 'bool',
            'time_off_request_id': 'str'
        }

        self.attribute_map = {
            'business_unit_date': 'businessUnitDate',
            'length_minutes': 'lengthMinutes',
            'description': 'description',
            'activity_code_id': 'activityCodeId',
            'paid': 'paid',
            'time_off_request_id': 'timeOffRequestId'
        }

        self._business_unit_date = None
        self._length_minutes = None
        self._description = None
        self._activity_code_id = None
        self._paid = None
        self._time_off_request_id = None

    @property
    def business_unit_date(self):
        """
        Gets the business_unit_date of this BuFullDayTimeOffMarker.
        The date of the time off marker, interpreted in the business unit's time zone. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :return: The business_unit_date of this BuFullDayTimeOffMarker.
        :rtype: date
        """
        return self._business_unit_date

    @business_unit_date.setter
    def business_unit_date(self, business_unit_date):
        """
        Sets the business_unit_date of this BuFullDayTimeOffMarker.
        The date of the time off marker, interpreted in the business unit's time zone. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :param business_unit_date: The business_unit_date of this BuFullDayTimeOffMarker.
        :type: date
        """
        

        self._business_unit_date = business_unit_date

    @property
    def length_minutes(self):
        """
        Gets the length_minutes of this BuFullDayTimeOffMarker.
        The length of the time off marker in minutes

        :return: The length_minutes of this BuFullDayTimeOffMarker.
        :rtype: int
        """
        return self._length_minutes

    @length_minutes.setter
    def length_minutes(self, length_minutes):
        """
        Sets the length_minutes of this BuFullDayTimeOffMarker.
        The length of the time off marker in minutes

        :param length_minutes: The length_minutes of this BuFullDayTimeOffMarker.
        :type: int
        """
        

        self._length_minutes = length_minutes

    @property
    def description(self):
        """
        Gets the description of this BuFullDayTimeOffMarker.
        The description of the time off marker

        :return: The description of this BuFullDayTimeOffMarker.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this BuFullDayTimeOffMarker.
        The description of the time off marker

        :param description: The description of this BuFullDayTimeOffMarker.
        :type: str
        """
        

        self._description = description

    @property
    def activity_code_id(self):
        """
        Gets the activity_code_id of this BuFullDayTimeOffMarker.
        The ID of the activity code associated with the time off marker

        :return: The activity_code_id of this BuFullDayTimeOffMarker.
        :rtype: str
        """
        return self._activity_code_id

    @activity_code_id.setter
    def activity_code_id(self, activity_code_id):
        """
        Sets the activity_code_id of this BuFullDayTimeOffMarker.
        The ID of the activity code associated with the time off marker

        :param activity_code_id: The activity_code_id of this BuFullDayTimeOffMarker.
        :type: str
        """
        

        self._activity_code_id = activity_code_id

    @property
    def paid(self):
        """
        Gets the paid of this BuFullDayTimeOffMarker.
        Whether the time off marker is paid

        :return: The paid of this BuFullDayTimeOffMarker.
        :rtype: bool
        """
        return self._paid

    @paid.setter
    def paid(self, paid):
        """
        Sets the paid of this BuFullDayTimeOffMarker.
        Whether the time off marker is paid

        :param paid: The paid of this BuFullDayTimeOffMarker.
        :type: bool
        """
        

        self._paid = paid

    @property
    def time_off_request_id(self):
        """
        Gets the time_off_request_id of this BuFullDayTimeOffMarker.
        The ID of the time off request

        :return: The time_off_request_id of this BuFullDayTimeOffMarker.
        :rtype: str
        """
        return self._time_off_request_id

    @time_off_request_id.setter
    def time_off_request_id(self, time_off_request_id):
        """
        Sets the time_off_request_id of this BuFullDayTimeOffMarker.
        The ID of the time off request

        :param time_off_request_id: The time_off_request_id of this BuFullDayTimeOffMarker.
        :type: str
        """
        

        self._time_off_request_id = time_off_request_id

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

