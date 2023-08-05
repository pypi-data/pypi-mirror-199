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

class BulkRelationshipsResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BulkRelationshipsResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'results': 'list[BulkResponseResultRelationshipRelationship]',
            'error_count': 'int',
            'error_indexes': 'list[int]'
        }

        self.attribute_map = {
            'results': 'results',
            'error_count': 'errorCount',
            'error_indexes': 'errorIndexes'
        }

        self._results = None
        self._error_count = None
        self._error_indexes = None

    @property
    def results(self):
        """
        Gets the results of this BulkRelationshipsResponse.


        :return: The results of this BulkRelationshipsResponse.
        :rtype: list[BulkResponseResultRelationshipRelationship]
        """
        return self._results

    @results.setter
    def results(self, results):
        """
        Sets the results of this BulkRelationshipsResponse.


        :param results: The results of this BulkRelationshipsResponse.
        :type: list[BulkResponseResultRelationshipRelationship]
        """
        

        self._results = results

    @property
    def error_count(self):
        """
        Gets the error_count of this BulkRelationshipsResponse.


        :return: The error_count of this BulkRelationshipsResponse.
        :rtype: int
        """
        return self._error_count

    @error_count.setter
    def error_count(self, error_count):
        """
        Sets the error_count of this BulkRelationshipsResponse.


        :param error_count: The error_count of this BulkRelationshipsResponse.
        :type: int
        """
        

        self._error_count = error_count

    @property
    def error_indexes(self):
        """
        Gets the error_indexes of this BulkRelationshipsResponse.


        :return: The error_indexes of this BulkRelationshipsResponse.
        :rtype: list[int]
        """
        return self._error_indexes

    @error_indexes.setter
    def error_indexes(self, error_indexes):
        """
        Sets the error_indexes of this BulkRelationshipsResponse.


        :param error_indexes: The error_indexes of this BulkRelationshipsResponse.
        :type: list[int]
        """
        

        self._error_indexes = error_indexes

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

