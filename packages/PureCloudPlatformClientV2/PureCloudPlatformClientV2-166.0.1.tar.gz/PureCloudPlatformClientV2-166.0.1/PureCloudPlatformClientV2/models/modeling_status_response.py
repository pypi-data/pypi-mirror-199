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

class ModelingStatusResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ModelingStatusResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'status': 'str',
            'error_details': 'list[ModelingProcessingError]',
            'modeling_result_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'status': 'status',
            'error_details': 'errorDetails',
            'modeling_result_uri': 'modelingResultUri'
        }

        self._id = None
        self._status = None
        self._error_details = None
        self._modeling_result_uri = None

    @property
    def id(self):
        """
        Gets the id of this ModelingStatusResponse.
        The ID generated for the modeling job.  Use to GET result when job is completed.

        :return: The id of this ModelingStatusResponse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ModelingStatusResponse.
        The ID generated for the modeling job.  Use to GET result when job is completed.

        :param id: The id of this ModelingStatusResponse.
        :type: str
        """
        

        self._id = id

    @property
    def status(self):
        """
        Gets the status of this ModelingStatusResponse.
        The status of the modeling job.

        :return: The status of this ModelingStatusResponse.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this ModelingStatusResponse.
        The status of the modeling job.

        :param status: The status of this ModelingStatusResponse.
        :type: str
        """
        allowed_values = ["Pending", "Success", "Failed", "Ongoing", "PartialFailure"]
        if status.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for status -> " + status)
            self._status = "outdated_sdk_version"
        else:
            self._status = status

    @property
    def error_details(self):
        """
        Gets the error_details of this ModelingStatusResponse.
        If the request could not be properly processed, error details will be given here.

        :return: The error_details of this ModelingStatusResponse.
        :rtype: list[ModelingProcessingError]
        """
        return self._error_details

    @error_details.setter
    def error_details(self, error_details):
        """
        Sets the error_details of this ModelingStatusResponse.
        If the request could not be properly processed, error details will be given here.

        :param error_details: The error_details of this ModelingStatusResponse.
        :type: list[ModelingProcessingError]
        """
        

        self._error_details = error_details

    @property
    def modeling_result_uri(self):
        """
        Gets the modeling_result_uri of this ModelingStatusResponse.
        The uri of the modeling result. It has a value if the status is either 'Success', 'PartialFailure', or 'Failed'.

        :return: The modeling_result_uri of this ModelingStatusResponse.
        :rtype: str
        """
        return self._modeling_result_uri

    @modeling_result_uri.setter
    def modeling_result_uri(self, modeling_result_uri):
        """
        Sets the modeling_result_uri of this ModelingStatusResponse.
        The uri of the modeling result. It has a value if the status is either 'Success', 'PartialFailure', or 'Failed'.

        :param modeling_result_uri: The modeling_result_uri of this ModelingStatusResponse.
        :type: str
        """
        

        self._modeling_result_uri = modeling_result_uri

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

