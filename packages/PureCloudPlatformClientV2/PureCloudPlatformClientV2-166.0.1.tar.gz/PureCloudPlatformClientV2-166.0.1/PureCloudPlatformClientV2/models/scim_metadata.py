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

class ScimMetadata(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ScimMetadata - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'resource_type': 'str',
            'last_modified': 'datetime',
            'location': 'str',
            'version': 'str'
        }

        self.attribute_map = {
            'resource_type': 'resourceType',
            'last_modified': 'lastModified',
            'location': 'location',
            'version': 'version'
        }

        self._resource_type = None
        self._last_modified = None
        self._location = None
        self._version = None

    @property
    def resource_type(self):
        """
        Gets the resource_type of this ScimMetadata.
        The type of SCIM resource.

        :return: The resource_type of this ScimMetadata.
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """
        Sets the resource_type of this ScimMetadata.
        The type of SCIM resource.

        :param resource_type: The resource_type of this ScimMetadata.
        :type: str
        """
        allowed_values = ["User", "Group", "ServiceProviderConfig", "ResourceType", "Schema"]
        if resource_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for resource_type -> " + resource_type)
            self._resource_type = "outdated_sdk_version"
        else:
            self._resource_type = resource_type

    @property
    def last_modified(self):
        """
        Gets the last_modified of this ScimMetadata.
        The last time that the resource was modified. Date time is represented as an \"ISO-8601 string\", for example, yyyy-MM-ddTHH:mm:ss.SSSZ. Not included with \"Schema\" and \"ResourceType\" resources.

        :return: The last_modified of this ScimMetadata.
        :rtype: datetime
        """
        return self._last_modified

    @last_modified.setter
    def last_modified(self, last_modified):
        """
        Sets the last_modified of this ScimMetadata.
        The last time that the resource was modified. Date time is represented as an \"ISO-8601 string\", for example, yyyy-MM-ddTHH:mm:ss.SSSZ. Not included with \"Schema\" and \"ResourceType\" resources.

        :param last_modified: The last_modified of this ScimMetadata.
        :type: datetime
        """
        

        self._last_modified = last_modified

    @property
    def location(self):
        """
        Gets the location of this ScimMetadata.
        The URI of the resource.

        :return: The location of this ScimMetadata.
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Sets the location of this ScimMetadata.
        The URI of the resource.

        :param location: The location of this ScimMetadata.
        :type: str
        """
        

        self._location = location

    @property
    def version(self):
        """
        Gets the version of this ScimMetadata.
        The version of the resource. Matches the ETag HTTP response header. Not included with \"Schema\" and \"ResourceType\" resources.

        :return: The version of this ScimMetadata.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this ScimMetadata.
        The version of the resource. Matches the ETag HTTP response header. Not included with \"Schema\" and \"ResourceType\" resources.

        :param version: The version of this ScimMetadata.
        :type: str
        """
        

        self._version = version

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

