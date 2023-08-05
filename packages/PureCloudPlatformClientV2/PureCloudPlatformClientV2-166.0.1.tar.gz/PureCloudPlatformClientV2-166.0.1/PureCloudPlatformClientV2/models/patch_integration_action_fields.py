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

class PatchIntegrationActionFields(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        PatchIntegrationActionFields - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'integration_action': 'PatchIntegrationAction',
            'request_mappings': 'list[RequestMapping]'
        }

        self.attribute_map = {
            'integration_action': 'integrationAction',
            'request_mappings': 'requestMappings'
        }

        self._integration_action = None
        self._request_mappings = None

    @property
    def integration_action(self):
        """
        Gets the integration_action of this PatchIntegrationActionFields.
        Reference to the Integration Action to be used when integrationAction type is qualified

        :return: The integration_action of this PatchIntegrationActionFields.
        :rtype: PatchIntegrationAction
        """
        return self._integration_action

    @integration_action.setter
    def integration_action(self, integration_action):
        """
        Sets the integration_action of this PatchIntegrationActionFields.
        Reference to the Integration Action to be used when integrationAction type is qualified

        :param integration_action: The integration_action of this PatchIntegrationActionFields.
        :type: PatchIntegrationAction
        """
        

        self._integration_action = integration_action

    @property
    def request_mappings(self):
        """
        Gets the request_mappings of this PatchIntegrationActionFields.
        Collection of Request Mappings to use

        :return: The request_mappings of this PatchIntegrationActionFields.
        :rtype: list[RequestMapping]
        """
        return self._request_mappings

    @request_mappings.setter
    def request_mappings(self, request_mappings):
        """
        Sets the request_mappings of this PatchIntegrationActionFields.
        Collection of Request Mappings to use

        :param request_mappings: The request_mappings of this PatchIntegrationActionFields.
        :type: list[RequestMapping]
        """
        

        self._request_mappings = request_mappings

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

