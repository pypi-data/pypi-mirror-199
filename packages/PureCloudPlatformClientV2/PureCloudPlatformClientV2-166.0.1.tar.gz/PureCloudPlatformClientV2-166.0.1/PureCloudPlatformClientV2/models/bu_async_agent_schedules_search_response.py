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

class BuAsyncAgentSchedulesSearchResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuAsyncAgentSchedulesSearchResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'status': 'str',
            'operation_id': 'str',
            'result': 'BuAgentSchedulesSearchResponse',
            'progress': 'int',
            'download_url': 'str'
        }

        self.attribute_map = {
            'status': 'status',
            'operation_id': 'operationId',
            'result': 'result',
            'progress': 'progress',
            'download_url': 'downloadUrl'
        }

        self._status = None
        self._operation_id = None
        self._result = None
        self._progress = None
        self._download_url = None

    @property
    def status(self):
        """
        Gets the status of this BuAsyncAgentSchedulesSearchResponse.
        The status of the operation

        :return: The status of this BuAsyncAgentSchedulesSearchResponse.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this BuAsyncAgentSchedulesSearchResponse.
        The status of the operation

        :param status: The status of this BuAsyncAgentSchedulesSearchResponse.
        :type: str
        """
        allowed_values = ["Processing", "Complete", "Canceled", "Error"]
        if status.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for status -> " + status)
            self._status = "outdated_sdk_version"
        else:
            self._status = status

    @property
    def operation_id(self):
        """
        Gets the operation_id of this BuAsyncAgentSchedulesSearchResponse.
        The ID for the operation

        :return: The operation_id of this BuAsyncAgentSchedulesSearchResponse.
        :rtype: str
        """
        return self._operation_id

    @operation_id.setter
    def operation_id(self, operation_id):
        """
        Sets the operation_id of this BuAsyncAgentSchedulesSearchResponse.
        The ID for the operation

        :param operation_id: The operation_id of this BuAsyncAgentSchedulesSearchResponse.
        :type: str
        """
        

        self._operation_id = operation_id

    @property
    def result(self):
        """
        Gets the result of this BuAsyncAgentSchedulesSearchResponse.
        The result of the operation.  Null unless status == Complete

        :return: The result of this BuAsyncAgentSchedulesSearchResponse.
        :rtype: BuAgentSchedulesSearchResponse
        """
        return self._result

    @result.setter
    def result(self, result):
        """
        Sets the result of this BuAsyncAgentSchedulesSearchResponse.
        The result of the operation.  Null unless status == Complete

        :param result: The result of this BuAsyncAgentSchedulesSearchResponse.
        :type: BuAgentSchedulesSearchResponse
        """
        

        self._result = result

    @property
    def progress(self):
        """
        Gets the progress of this BuAsyncAgentSchedulesSearchResponse.
        Percent progress for the operation

        :return: The progress of this BuAsyncAgentSchedulesSearchResponse.
        :rtype: int
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """
        Sets the progress of this BuAsyncAgentSchedulesSearchResponse.
        Percent progress for the operation

        :param progress: The progress of this BuAsyncAgentSchedulesSearchResponse.
        :type: int
        """
        

        self._progress = progress

    @property
    def download_url(self):
        """
        Gets the download_url of this BuAsyncAgentSchedulesSearchResponse.
        The URL from which to download the result if it is too large to pass directly

        :return: The download_url of this BuAsyncAgentSchedulesSearchResponse.
        :rtype: str
        """
        return self._download_url

    @download_url.setter
    def download_url(self, download_url):
        """
        Sets the download_url of this BuAsyncAgentSchedulesSearchResponse.
        The URL from which to download the result if it is too large to pass directly

        :param download_url: The download_url of this BuAsyncAgentSchedulesSearchResponse.
        :type: str
        """
        

        self._download_url = download_url

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

