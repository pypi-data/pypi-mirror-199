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

class ProgramsMappingsEntityListing(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ProgramsMappingsEntityListing - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'entities': 'list[ProgramMappings]',
            'page_size': 'int',
            'next_uri': 'str',
            'page_count': 'int',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'entities': 'entities',
            'page_size': 'pageSize',
            'next_uri': 'nextUri',
            'page_count': 'pageCount',
            'self_uri': 'selfUri'
        }

        self._entities = None
        self._page_size = None
        self._next_uri = None
        self._page_count = None
        self._self_uri = None

    @property
    def entities(self):
        """
        Gets the entities of this ProgramsMappingsEntityListing.


        :return: The entities of this ProgramsMappingsEntityListing.
        :rtype: list[ProgramMappings]
        """
        return self._entities

    @entities.setter
    def entities(self, entities):
        """
        Sets the entities of this ProgramsMappingsEntityListing.


        :param entities: The entities of this ProgramsMappingsEntityListing.
        :type: list[ProgramMappings]
        """
        

        self._entities = entities

    @property
    def page_size(self):
        """
        Gets the page_size of this ProgramsMappingsEntityListing.


        :return: The page_size of this ProgramsMappingsEntityListing.
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """
        Sets the page_size of this ProgramsMappingsEntityListing.


        :param page_size: The page_size of this ProgramsMappingsEntityListing.
        :type: int
        """
        

        self._page_size = page_size

    @property
    def next_uri(self):
        """
        Gets the next_uri of this ProgramsMappingsEntityListing.


        :return: The next_uri of this ProgramsMappingsEntityListing.
        :rtype: str
        """
        return self._next_uri

    @next_uri.setter
    def next_uri(self, next_uri):
        """
        Sets the next_uri of this ProgramsMappingsEntityListing.


        :param next_uri: The next_uri of this ProgramsMappingsEntityListing.
        :type: str
        """
        

        self._next_uri = next_uri

    @property
    def page_count(self):
        """
        Gets the page_count of this ProgramsMappingsEntityListing.


        :return: The page_count of this ProgramsMappingsEntityListing.
        :rtype: int
        """
        return self._page_count

    @page_count.setter
    def page_count(self, page_count):
        """
        Sets the page_count of this ProgramsMappingsEntityListing.


        :param page_count: The page_count of this ProgramsMappingsEntityListing.
        :type: int
        """
        

        self._page_count = page_count

    @property
    def self_uri(self):
        """
        Gets the self_uri of this ProgramsMappingsEntityListing.


        :return: The self_uri of this ProgramsMappingsEntityListing.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this ProgramsMappingsEntityListing.


        :param self_uri: The self_uri of this ProgramsMappingsEntityListing.
        :type: str
        """
        

        self._self_uri = self_uri

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

