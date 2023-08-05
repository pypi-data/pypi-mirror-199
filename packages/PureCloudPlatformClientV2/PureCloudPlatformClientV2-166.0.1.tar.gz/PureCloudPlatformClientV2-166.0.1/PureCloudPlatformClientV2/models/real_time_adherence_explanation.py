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

class RealTimeAdherenceExplanation(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        RealTimeAdherenceExplanation - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'start_date': 'datetime',
            'length_minutes': 'int',
            'status': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'start_date': 'startDate',
            'length_minutes': 'lengthMinutes',
            'status': 'status',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._start_date = None
        self._length_minutes = None
        self._status = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this RealTimeAdherenceExplanation.
        The globally unique identifier for the object.

        :return: The id of this RealTimeAdherenceExplanation.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this RealTimeAdherenceExplanation.
        The globally unique identifier for the object.

        :param id: The id of this RealTimeAdherenceExplanation.
        :type: str
        """
        

        self._id = id

    @property
    def start_date(self):
        """
        Gets the start_date of this RealTimeAdherenceExplanation.
        The start timestamp of the adherence explanation in ISO-8601 format

        :return: The start_date of this RealTimeAdherenceExplanation.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this RealTimeAdherenceExplanation.
        The start timestamp of the adherence explanation in ISO-8601 format

        :param start_date: The start_date of this RealTimeAdherenceExplanation.
        :type: datetime
        """
        

        self._start_date = start_date

    @property
    def length_minutes(self):
        """
        Gets the length_minutes of this RealTimeAdherenceExplanation.
        The length of the adherence explanation in minutes

        :return: The length_minutes of this RealTimeAdherenceExplanation.
        :rtype: int
        """
        return self._length_minutes

    @length_minutes.setter
    def length_minutes(self, length_minutes):
        """
        Sets the length_minutes of this RealTimeAdherenceExplanation.
        The length of the adherence explanation in minutes

        :param length_minutes: The length_minutes of this RealTimeAdherenceExplanation.
        :type: int
        """
        

        self._length_minutes = length_minutes

    @property
    def status(self):
        """
        Gets the status of this RealTimeAdherenceExplanation.
        The status of the adherence explanation

        :return: The status of this RealTimeAdherenceExplanation.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this RealTimeAdherenceExplanation.
        The status of the adherence explanation

        :param status: The status of this RealTimeAdherenceExplanation.
        :type: str
        """
        allowed_values = ["Pending", "Approved", "Denied"]
        if status.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for status -> " + status)
            self._status = "outdated_sdk_version"
        else:
            self._status = status

    @property
    def self_uri(self):
        """
        Gets the self_uri of this RealTimeAdherenceExplanation.
        The URI for this object

        :return: The self_uri of this RealTimeAdherenceExplanation.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this RealTimeAdherenceExplanation.
        The URI for this object

        :param self_uri: The self_uri of this RealTimeAdherenceExplanation.
        :type: str
        """
        

        self._self_uri = self_uri

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

