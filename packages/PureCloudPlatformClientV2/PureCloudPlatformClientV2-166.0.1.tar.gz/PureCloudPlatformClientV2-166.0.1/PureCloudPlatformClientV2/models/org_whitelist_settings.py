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

class OrgWhitelistSettings(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        OrgWhitelistSettings - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'enable_whitelist': 'bool',
            'domain_whitelist': 'list[str]'
        }

        self.attribute_map = {
            'enable_whitelist': 'enableWhitelist',
            'domain_whitelist': 'domainWhitelist'
        }

        self._enable_whitelist = None
        self._domain_whitelist = None

    @property
    def enable_whitelist(self):
        """
        Gets the enable_whitelist of this OrgWhitelistSettings.


        :return: The enable_whitelist of this OrgWhitelistSettings.
        :rtype: bool
        """
        return self._enable_whitelist

    @enable_whitelist.setter
    def enable_whitelist(self, enable_whitelist):
        """
        Sets the enable_whitelist of this OrgWhitelistSettings.


        :param enable_whitelist: The enable_whitelist of this OrgWhitelistSettings.
        :type: bool
        """
        

        self._enable_whitelist = enable_whitelist

    @property
    def domain_whitelist(self):
        """
        Gets the domain_whitelist of this OrgWhitelistSettings.


        :return: The domain_whitelist of this OrgWhitelistSettings.
        :rtype: list[str]
        """
        return self._domain_whitelist

    @domain_whitelist.setter
    def domain_whitelist(self, domain_whitelist):
        """
        Sets the domain_whitelist of this OrgWhitelistSettings.


        :param domain_whitelist: The domain_whitelist of this OrgWhitelistSettings.
        :type: list[str]
        """
        

        self._domain_whitelist = domain_whitelist

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

