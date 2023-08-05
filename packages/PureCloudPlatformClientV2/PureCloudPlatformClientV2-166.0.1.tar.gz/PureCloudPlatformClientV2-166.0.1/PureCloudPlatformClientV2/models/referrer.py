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

class Referrer(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Referrer - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'url': 'str',
            'domain': 'str',
            'hostname': 'str',
            'keywords': 'str',
            'pathname': 'str',
            'query_string': 'str',
            'fragment': 'str',
            'name': 'str',
            'medium': 'str'
        }

        self.attribute_map = {
            'url': 'url',
            'domain': 'domain',
            'hostname': 'hostname',
            'keywords': 'keywords',
            'pathname': 'pathname',
            'query_string': 'queryString',
            'fragment': 'fragment',
            'name': 'name',
            'medium': 'medium'
        }

        self._url = None
        self._domain = None
        self._hostname = None
        self._keywords = None
        self._pathname = None
        self._query_string = None
        self._fragment = None
        self._name = None
        self._medium = None

    @property
    def url(self):
        """
        Gets the url of this Referrer.
        Referrer URL.

        :return: The url of this Referrer.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the url of this Referrer.
        Referrer URL.

        :param url: The url of this Referrer.
        :type: str
        """
        

        self._url = url

    @property
    def domain(self):
        """
        Gets the domain of this Referrer.
        Referrer URL domain.

        :return: The domain of this Referrer.
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """
        Sets the domain of this Referrer.
        Referrer URL domain.

        :param domain: The domain of this Referrer.
        :type: str
        """
        

        self._domain = domain

    @property
    def hostname(self):
        """
        Gets the hostname of this Referrer.
        Referrer URL hostname.

        :return: The hostname of this Referrer.
        :rtype: str
        """
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        """
        Sets the hostname of this Referrer.
        Referrer URL hostname.

        :param hostname: The hostname of this Referrer.
        :type: str
        """
        

        self._hostname = hostname

    @property
    def keywords(self):
        """
        Gets the keywords of this Referrer.
        Referrer keywords.

        :return: The keywords of this Referrer.
        :rtype: str
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        """
        Sets the keywords of this Referrer.
        Referrer keywords.

        :param keywords: The keywords of this Referrer.
        :type: str
        """
        

        self._keywords = keywords

    @property
    def pathname(self):
        """
        Gets the pathname of this Referrer.
        Referrer URL pathname.

        :return: The pathname of this Referrer.
        :rtype: str
        """
        return self._pathname

    @pathname.setter
    def pathname(self, pathname):
        """
        Sets the pathname of this Referrer.
        Referrer URL pathname.

        :param pathname: The pathname of this Referrer.
        :type: str
        """
        

        self._pathname = pathname

    @property
    def query_string(self):
        """
        Gets the query_string of this Referrer.
        Referrer URL querystring.

        :return: The query_string of this Referrer.
        :rtype: str
        """
        return self._query_string

    @query_string.setter
    def query_string(self, query_string):
        """
        Sets the query_string of this Referrer.
        Referrer URL querystring.

        :param query_string: The query_string of this Referrer.
        :type: str
        """
        

        self._query_string = query_string

    @property
    def fragment(self):
        """
        Gets the fragment of this Referrer.
        Referrer URL fragment.

        :return: The fragment of this Referrer.
        :rtype: str
        """
        return self._fragment

    @fragment.setter
    def fragment(self, fragment):
        """
        Sets the fragment of this Referrer.
        Referrer URL fragment.

        :param fragment: The fragment of this Referrer.
        :type: str
        """
        

        self._fragment = fragment

    @property
    def name(self):
        """
        Gets the name of this Referrer.
        Name of referrer (e.g. Yahoo!, Google, InfoSpace).

        :return: The name of this Referrer.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Referrer.
        Name of referrer (e.g. Yahoo!, Google, InfoSpace).

        :param name: The name of this Referrer.
        :type: str
        """
        

        self._name = name

    @property
    def medium(self):
        """
        Gets the medium of this Referrer.
        Type of referrer (e.g. search, social).

        :return: The medium of this Referrer.
        :rtype: str
        """
        return self._medium

    @medium.setter
    def medium(self, medium):
        """
        Sets the medium of this Referrer.
        Type of referrer (e.g. search, social).

        :param medium: The medium of this Referrer.
        :type: str
        """
        allowed_values = ["internal", "search", "social", "email", "unknown", "paid"]
        if medium.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for medium -> " + medium)
            self._medium = "outdated_sdk_version"
        else:
            self._medium = medium

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

