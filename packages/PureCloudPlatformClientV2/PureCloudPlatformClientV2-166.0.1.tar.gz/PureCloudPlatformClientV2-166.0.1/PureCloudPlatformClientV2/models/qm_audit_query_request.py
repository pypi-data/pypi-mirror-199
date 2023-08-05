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

class QMAuditQueryRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        QMAuditQueryRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'interval': 'str',
            'filters': 'list[QualityAuditQueryFilter]',
            'sort': 'list[AuditQuerySort]'
        }

        self.attribute_map = {
            'interval': 'interval',
            'filters': 'filters',
            'sort': 'sort'
        }

        self._interval = None
        self._filters = None
        self._sort = None

    @property
    def interval(self):
        """
        Gets the interval of this QMAuditQueryRequest.
        Date and time range of data to query. Intervals are represented as an ISO-8601 string. For example: YYYY-MM-DDThh:mm:ss/YYYY-MM-DDThh:mm:ss

        :return: The interval of this QMAuditQueryRequest.
        :rtype: str
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """
        Sets the interval of this QMAuditQueryRequest.
        Date and time range of data to query. Intervals are represented as an ISO-8601 string. For example: YYYY-MM-DDThh:mm:ss/YYYY-MM-DDThh:mm:ss

        :param interval: The interval of this QMAuditQueryRequest.
        :type: str
        """
        

        self._interval = interval

    @property
    def filters(self):
        """
        Gets the filters of this QMAuditQueryRequest.
        List of filters for the query.

        :return: The filters of this QMAuditQueryRequest.
        :rtype: list[QualityAuditQueryFilter]
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """
        Sets the filters of this QMAuditQueryRequest.
        List of filters for the query.

        :param filters: The filters of this QMAuditQueryRequest.
        :type: list[QualityAuditQueryFilter]
        """
        

        self._filters = filters

    @property
    def sort(self):
        """
        Gets the sort of this QMAuditQueryRequest.
        Sort parameter for the query.

        :return: The sort of this QMAuditQueryRequest.
        :rtype: list[AuditQuerySort]
        """
        return self._sort

    @sort.setter
    def sort(self, sort):
        """
        Sets the sort of this QMAuditQueryRequest.
        Sort parameter for the query.

        :param sort: The sort of this QMAuditQueryRequest.
        :type: list[AuditQuerySort]
        """
        

        self._sort = sort

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

