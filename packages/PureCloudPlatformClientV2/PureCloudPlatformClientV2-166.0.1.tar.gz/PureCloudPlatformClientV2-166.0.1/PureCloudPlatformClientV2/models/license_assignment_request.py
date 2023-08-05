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

class LicenseAssignmentRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        LicenseAssignmentRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'license_id': 'str',
            'user_ids_add': 'list[str]',
            'user_ids_remove': 'list[str]'
        }

        self.attribute_map = {
            'license_id': 'licenseId',
            'user_ids_add': 'userIdsAdd',
            'user_ids_remove': 'userIdsRemove'
        }

        self._license_id = None
        self._user_ids_add = None
        self._user_ids_remove = None

    @property
    def license_id(self):
        """
        Gets the license_id of this LicenseAssignmentRequest.
        The id of the license to assign/unassign.

        :return: The license_id of this LicenseAssignmentRequest.
        :rtype: str
        """
        return self._license_id

    @license_id.setter
    def license_id(self, license_id):
        """
        Sets the license_id of this LicenseAssignmentRequest.
        The id of the license to assign/unassign.

        :param license_id: The license_id of this LicenseAssignmentRequest.
        :type: str
        """
        

        self._license_id = license_id

    @property
    def user_ids_add(self):
        """
        Gets the user_ids_add of this LicenseAssignmentRequest.
        The ids of users to assign this license to.

        :return: The user_ids_add of this LicenseAssignmentRequest.
        :rtype: list[str]
        """
        return self._user_ids_add

    @user_ids_add.setter
    def user_ids_add(self, user_ids_add):
        """
        Sets the user_ids_add of this LicenseAssignmentRequest.
        The ids of users to assign this license to.

        :param user_ids_add: The user_ids_add of this LicenseAssignmentRequest.
        :type: list[str]
        """
        

        self._user_ids_add = user_ids_add

    @property
    def user_ids_remove(self):
        """
        Gets the user_ids_remove of this LicenseAssignmentRequest.
        The ids of users to unassign this license from.

        :return: The user_ids_remove of this LicenseAssignmentRequest.
        :rtype: list[str]
        """
        return self._user_ids_remove

    @user_ids_remove.setter
    def user_ids_remove(self, user_ids_remove):
        """
        Sets the user_ids_remove of this LicenseAssignmentRequest.
        The ids of users to unassign this license from.

        :param user_ids_remove: The user_ids_remove of this LicenseAssignmentRequest.
        :type: list[str]
        """
        

        self._user_ids_remove = user_ids_remove

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

