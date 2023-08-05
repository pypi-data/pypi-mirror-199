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

class JourneyWebEventsNotificationPage(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        JourneyWebEventsNotificationPage - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'url': 'str',
            'title': 'str',
            'domain': 'str',
            'fragment': 'str',
            'hostname': 'str',
            'keywords': 'str',
            'lang': 'str',
            'pathname': 'str',
            'query_string': 'str',
            'breadcrumb': 'list[str]'
        }

        self.attribute_map = {
            'url': 'url',
            'title': 'title',
            'domain': 'domain',
            'fragment': 'fragment',
            'hostname': 'hostname',
            'keywords': 'keywords',
            'lang': 'lang',
            'pathname': 'pathname',
            'query_string': 'queryString',
            'breadcrumb': 'breadcrumb'
        }

        self._url = None
        self._title = None
        self._domain = None
        self._fragment = None
        self._hostname = None
        self._keywords = None
        self._lang = None
        self._pathname = None
        self._query_string = None
        self._breadcrumb = None

    @property
    def url(self):
        """
        Gets the url of this JourneyWebEventsNotificationPage.


        :return: The url of this JourneyWebEventsNotificationPage.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the url of this JourneyWebEventsNotificationPage.


        :param url: The url of this JourneyWebEventsNotificationPage.
        :type: str
        """
        

        self._url = url

    @property
    def title(self):
        """
        Gets the title of this JourneyWebEventsNotificationPage.


        :return: The title of this JourneyWebEventsNotificationPage.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this JourneyWebEventsNotificationPage.


        :param title: The title of this JourneyWebEventsNotificationPage.
        :type: str
        """
        

        self._title = title

    @property
    def domain(self):
        """
        Gets the domain of this JourneyWebEventsNotificationPage.


        :return: The domain of this JourneyWebEventsNotificationPage.
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """
        Sets the domain of this JourneyWebEventsNotificationPage.


        :param domain: The domain of this JourneyWebEventsNotificationPage.
        :type: str
        """
        

        self._domain = domain

    @property
    def fragment(self):
        """
        Gets the fragment of this JourneyWebEventsNotificationPage.


        :return: The fragment of this JourneyWebEventsNotificationPage.
        :rtype: str
        """
        return self._fragment

    @fragment.setter
    def fragment(self, fragment):
        """
        Sets the fragment of this JourneyWebEventsNotificationPage.


        :param fragment: The fragment of this JourneyWebEventsNotificationPage.
        :type: str
        """
        

        self._fragment = fragment

    @property
    def hostname(self):
        """
        Gets the hostname of this JourneyWebEventsNotificationPage.


        :return: The hostname of this JourneyWebEventsNotificationPage.
        :rtype: str
        """
        return self._hostname

    @hostname.setter
    def hostname(self, hostname):
        """
        Sets the hostname of this JourneyWebEventsNotificationPage.


        :param hostname: The hostname of this JourneyWebEventsNotificationPage.
        :type: str
        """
        

        self._hostname = hostname

    @property
    def keywords(self):
        """
        Gets the keywords of this JourneyWebEventsNotificationPage.


        :return: The keywords of this JourneyWebEventsNotificationPage.
        :rtype: str
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        """
        Sets the keywords of this JourneyWebEventsNotificationPage.


        :param keywords: The keywords of this JourneyWebEventsNotificationPage.
        :type: str
        """
        

        self._keywords = keywords

    @property
    def lang(self):
        """
        Gets the lang of this JourneyWebEventsNotificationPage.


        :return: The lang of this JourneyWebEventsNotificationPage.
        :rtype: str
        """
        return self._lang

    @lang.setter
    def lang(self, lang):
        """
        Sets the lang of this JourneyWebEventsNotificationPage.


        :param lang: The lang of this JourneyWebEventsNotificationPage.
        :type: str
        """
        

        self._lang = lang

    @property
    def pathname(self):
        """
        Gets the pathname of this JourneyWebEventsNotificationPage.


        :return: The pathname of this JourneyWebEventsNotificationPage.
        :rtype: str
        """
        return self._pathname

    @pathname.setter
    def pathname(self, pathname):
        """
        Sets the pathname of this JourneyWebEventsNotificationPage.


        :param pathname: The pathname of this JourneyWebEventsNotificationPage.
        :type: str
        """
        

        self._pathname = pathname

    @property
    def query_string(self):
        """
        Gets the query_string of this JourneyWebEventsNotificationPage.


        :return: The query_string of this JourneyWebEventsNotificationPage.
        :rtype: str
        """
        return self._query_string

    @query_string.setter
    def query_string(self, query_string):
        """
        Sets the query_string of this JourneyWebEventsNotificationPage.


        :param query_string: The query_string of this JourneyWebEventsNotificationPage.
        :type: str
        """
        

        self._query_string = query_string

    @property
    def breadcrumb(self):
        """
        Gets the breadcrumb of this JourneyWebEventsNotificationPage.


        :return: The breadcrumb of this JourneyWebEventsNotificationPage.
        :rtype: list[str]
        """
        return self._breadcrumb

    @breadcrumb.setter
    def breadcrumb(self, breadcrumb):
        """
        Sets the breadcrumb of this JourneyWebEventsNotificationPage.


        :param breadcrumb: The breadcrumb of this JourneyWebEventsNotificationPage.
        :type: list[str]
        """
        

        self._breadcrumb = breadcrumb

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

