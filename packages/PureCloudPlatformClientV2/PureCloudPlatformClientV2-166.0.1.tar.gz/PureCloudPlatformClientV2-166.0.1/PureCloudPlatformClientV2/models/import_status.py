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

class ImportStatus(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ImportStatus - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'state': 'str',
            'total_records': 'int',
            'completed_records': 'int',
            'percent_complete': 'int',
            'failure_reason': 'str'
        }

        self.attribute_map = {
            'state': 'state',
            'total_records': 'totalRecords',
            'completed_records': 'completedRecords',
            'percent_complete': 'percentComplete',
            'failure_reason': 'failureReason'
        }

        self._state = None
        self._total_records = None
        self._completed_records = None
        self._percent_complete = None
        self._failure_reason = None

    @property
    def state(self):
        """
        Gets the state of this ImportStatus.
        current status of the import

        :return: The state of this ImportStatus.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this ImportStatus.
        current status of the import

        :param state: The state of this ImportStatus.
        :type: str
        """
        allowed_values = ["IN_PROGRESS", "FAILED"]
        if state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for state -> " + state)
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def total_records(self):
        """
        Gets the total_records of this ImportStatus.
        total number of records to be imported

        :return: The total_records of this ImportStatus.
        :rtype: int
        """
        return self._total_records

    @total_records.setter
    def total_records(self, total_records):
        """
        Sets the total_records of this ImportStatus.
        total number of records to be imported

        :param total_records: The total_records of this ImportStatus.
        :type: int
        """
        

        self._total_records = total_records

    @property
    def completed_records(self):
        """
        Gets the completed_records of this ImportStatus.
        number of records finished importing

        :return: The completed_records of this ImportStatus.
        :rtype: int
        """
        return self._completed_records

    @completed_records.setter
    def completed_records(self, completed_records):
        """
        Sets the completed_records of this ImportStatus.
        number of records finished importing

        :param completed_records: The completed_records of this ImportStatus.
        :type: int
        """
        

        self._completed_records = completed_records

    @property
    def percent_complete(self):
        """
        Gets the percent_complete of this ImportStatus.
        percentage of records finished importing

        :return: The percent_complete of this ImportStatus.
        :rtype: int
        """
        return self._percent_complete

    @percent_complete.setter
    def percent_complete(self, percent_complete):
        """
        Sets the percent_complete of this ImportStatus.
        percentage of records finished importing

        :param percent_complete: The percent_complete of this ImportStatus.
        :type: int
        """
        

        self._percent_complete = percent_complete

    @property
    def failure_reason(self):
        """
        Gets the failure_reason of this ImportStatus.
        if the import has failed, the reason for the failure

        :return: The failure_reason of this ImportStatus.
        :rtype: str
        """
        return self._failure_reason

    @failure_reason.setter
    def failure_reason(self, failure_reason):
        """
        Sets the failure_reason of this ImportStatus.
        if the import has failed, the reason for the failure

        :param failure_reason: The failure_reason of this ImportStatus.
        :type: str
        """
        

        self._failure_reason = failure_reason

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

