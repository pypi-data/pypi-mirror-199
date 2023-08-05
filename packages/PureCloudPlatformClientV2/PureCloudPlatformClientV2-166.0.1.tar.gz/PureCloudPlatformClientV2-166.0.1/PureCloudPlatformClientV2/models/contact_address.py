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

class ContactAddress(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ContactAddress - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'address1': 'str',
            'address2': 'str',
            'city': 'str',
            'state': 'str',
            'postal_code': 'str',
            'country_code': 'str'
        }

        self.attribute_map = {
            'address1': 'address1',
            'address2': 'address2',
            'city': 'city',
            'state': 'state',
            'postal_code': 'postalCode',
            'country_code': 'countryCode'
        }

        self._address1 = None
        self._address2 = None
        self._city = None
        self._state = None
        self._postal_code = None
        self._country_code = None

    @property
    def address1(self):
        """
        Gets the address1 of this ContactAddress.


        :return: The address1 of this ContactAddress.
        :rtype: str
        """
        return self._address1

    @address1.setter
    def address1(self, address1):
        """
        Sets the address1 of this ContactAddress.


        :param address1: The address1 of this ContactAddress.
        :type: str
        """
        

        self._address1 = address1

    @property
    def address2(self):
        """
        Gets the address2 of this ContactAddress.


        :return: The address2 of this ContactAddress.
        :rtype: str
        """
        return self._address2

    @address2.setter
    def address2(self, address2):
        """
        Sets the address2 of this ContactAddress.


        :param address2: The address2 of this ContactAddress.
        :type: str
        """
        

        self._address2 = address2

    @property
    def city(self):
        """
        Gets the city of this ContactAddress.


        :return: The city of this ContactAddress.
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """
        Sets the city of this ContactAddress.


        :param city: The city of this ContactAddress.
        :type: str
        """
        

        self._city = city

    @property
    def state(self):
        """
        Gets the state of this ContactAddress.


        :return: The state of this ContactAddress.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this ContactAddress.


        :param state: The state of this ContactAddress.
        :type: str
        """
        

        self._state = state

    @property
    def postal_code(self):
        """
        Gets the postal_code of this ContactAddress.


        :return: The postal_code of this ContactAddress.
        :rtype: str
        """
        return self._postal_code

    @postal_code.setter
    def postal_code(self, postal_code):
        """
        Sets the postal_code of this ContactAddress.


        :param postal_code: The postal_code of this ContactAddress.
        :type: str
        """
        

        self._postal_code = postal_code

    @property
    def country_code(self):
        """
        Gets the country_code of this ContactAddress.


        :return: The country_code of this ContactAddress.
        :rtype: str
        """
        return self._country_code

    @country_code.setter
    def country_code(self, country_code):
        """
        Sets the country_code of this ContactAddress.


        :param country_code: The country_code of this ContactAddress.
        :type: str
        """
        

        self._country_code = country_code

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

