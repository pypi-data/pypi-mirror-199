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

class FilterPreviewResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        FilterPreviewResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'filtered_contacts': 'int',
            'total_contacts': 'int',
            'preview': 'list[DialerContact]'
        }

        self.attribute_map = {
            'filtered_contacts': 'filteredContacts',
            'total_contacts': 'totalContacts',
            'preview': 'preview'
        }

        self._filtered_contacts = None
        self._total_contacts = None
        self._preview = None

    @property
    def filtered_contacts(self):
        """
        Gets the filtered_contacts of this FilterPreviewResponse.


        :return: The filtered_contacts of this FilterPreviewResponse.
        :rtype: int
        """
        return self._filtered_contacts

    @filtered_contacts.setter
    def filtered_contacts(self, filtered_contacts):
        """
        Sets the filtered_contacts of this FilterPreviewResponse.


        :param filtered_contacts: The filtered_contacts of this FilterPreviewResponse.
        :type: int
        """
        

        self._filtered_contacts = filtered_contacts

    @property
    def total_contacts(self):
        """
        Gets the total_contacts of this FilterPreviewResponse.


        :return: The total_contacts of this FilterPreviewResponse.
        :rtype: int
        """
        return self._total_contacts

    @total_contacts.setter
    def total_contacts(self, total_contacts):
        """
        Sets the total_contacts of this FilterPreviewResponse.


        :param total_contacts: The total_contacts of this FilterPreviewResponse.
        :type: int
        """
        

        self._total_contacts = total_contacts

    @property
    def preview(self):
        """
        Gets the preview of this FilterPreviewResponse.


        :return: The preview of this FilterPreviewResponse.
        :rtype: list[DialerContact]
        """
        return self._preview

    @preview.setter
    def preview(self, preview):
        """
        Sets the preview of this FilterPreviewResponse.


        :param preview: The preview of this FilterPreviewResponse.
        :type: list[DialerContact]
        """
        

        self._preview = preview

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

