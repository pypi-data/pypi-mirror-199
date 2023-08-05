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

class GenericTemplate(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        GenericTemplate - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'title': 'str',
            'description': 'str',
            'url': 'str',
            'components': 'list[RecordingButtonComponent]',
            'actions': 'RecordingContentActions'
        }

        self.attribute_map = {
            'title': 'title',
            'description': 'description',
            'url': 'url',
            'components': 'components',
            'actions': 'actions'
        }

        self._title = None
        self._description = None
        self._url = None
        self._components = None
        self._actions = None

    @property
    def title(self):
        """
        Gets the title of this GenericTemplate.
        Text to show in the title.

        :return: The title of this GenericTemplate.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this GenericTemplate.
        Text to show in the title.

        :param title: The title of this GenericTemplate.
        :type: str
        """
        

        self._title = title

    @property
    def description(self):
        """
        Gets the description of this GenericTemplate.
        Text to show in the description.

        :return: The description of this GenericTemplate.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this GenericTemplate.
        Text to show in the description.

        :param description: The description of this GenericTemplate.
        :type: str
        """
        

        self._description = description

    @property
    def url(self):
        """
        Gets the url of this GenericTemplate.
        URL of an image.

        :return: The url of this GenericTemplate.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the url of this GenericTemplate.
        URL of an image.

        :param url: The url of this GenericTemplate.
        :type: str
        """
        

        self._url = url

    @property
    def components(self):
        """
        Gets the components of this GenericTemplate.
        List of button components offered with this message content.

        :return: The components of this GenericTemplate.
        :rtype: list[RecordingButtonComponent]
        """
        return self._components

    @components.setter
    def components(self, components):
        """
        Sets the components of this GenericTemplate.
        List of button components offered with this message content.

        :param components: The components of this GenericTemplate.
        :type: list[RecordingButtonComponent]
        """
        

        self._components = components

    @property
    def actions(self):
        """
        Gets the actions of this GenericTemplate.
        Actions to be taken.

        :return: The actions of this GenericTemplate.
        :rtype: RecordingContentActions
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """
        Sets the actions of this GenericTemplate.
        Actions to be taken.

        :param actions: The actions of this GenericTemplate.
        :type: RecordingContentActions
        """
        

        self._actions = actions

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

