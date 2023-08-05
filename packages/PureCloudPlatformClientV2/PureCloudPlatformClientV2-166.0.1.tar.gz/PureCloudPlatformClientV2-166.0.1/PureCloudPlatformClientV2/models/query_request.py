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

class QueryRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        QueryRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'query_phrase': 'str',
            'page_number': 'int',
            'page_size': 'int',
            'facet_name_requests': 'list[str]',
            'sort': 'list[SortItem]',
            'filters': 'list[ContentFilterItem]',
            'attribute_filters': 'list[AttributeFilterItem]',
            'include_shares': 'bool'
        }

        self.attribute_map = {
            'query_phrase': 'queryPhrase',
            'page_number': 'pageNumber',
            'page_size': 'pageSize',
            'facet_name_requests': 'facetNameRequests',
            'sort': 'sort',
            'filters': 'filters',
            'attribute_filters': 'attributeFilters',
            'include_shares': 'includeShares'
        }

        self._query_phrase = None
        self._page_number = None
        self._page_size = None
        self._facet_name_requests = None
        self._sort = None
        self._filters = None
        self._attribute_filters = None
        self._include_shares = None

    @property
    def query_phrase(self):
        """
        Gets the query_phrase of this QueryRequest.


        :return: The query_phrase of this QueryRequest.
        :rtype: str
        """
        return self._query_phrase

    @query_phrase.setter
    def query_phrase(self, query_phrase):
        """
        Sets the query_phrase of this QueryRequest.


        :param query_phrase: The query_phrase of this QueryRequest.
        :type: str
        """
        

        self._query_phrase = query_phrase

    @property
    def page_number(self):
        """
        Gets the page_number of this QueryRequest.


        :return: The page_number of this QueryRequest.
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """
        Sets the page_number of this QueryRequest.


        :param page_number: The page_number of this QueryRequest.
        :type: int
        """
        

        self._page_number = page_number

    @property
    def page_size(self):
        """
        Gets the page_size of this QueryRequest.


        :return: The page_size of this QueryRequest.
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """
        Sets the page_size of this QueryRequest.


        :param page_size: The page_size of this QueryRequest.
        :type: int
        """
        

        self._page_size = page_size

    @property
    def facet_name_requests(self):
        """
        Gets the facet_name_requests of this QueryRequest.


        :return: The facet_name_requests of this QueryRequest.
        :rtype: list[str]
        """
        return self._facet_name_requests

    @facet_name_requests.setter
    def facet_name_requests(self, facet_name_requests):
        """
        Sets the facet_name_requests of this QueryRequest.


        :param facet_name_requests: The facet_name_requests of this QueryRequest.
        :type: list[str]
        """
        

        self._facet_name_requests = facet_name_requests

    @property
    def sort(self):
        """
        Gets the sort of this QueryRequest.


        :return: The sort of this QueryRequest.
        :rtype: list[SortItem]
        """
        return self._sort

    @sort.setter
    def sort(self, sort):
        """
        Sets the sort of this QueryRequest.


        :param sort: The sort of this QueryRequest.
        :type: list[SortItem]
        """
        

        self._sort = sort

    @property
    def filters(self):
        """
        Gets the filters of this QueryRequest.


        :return: The filters of this QueryRequest.
        :rtype: list[ContentFilterItem]
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """
        Sets the filters of this QueryRequest.


        :param filters: The filters of this QueryRequest.
        :type: list[ContentFilterItem]
        """
        

        self._filters = filters

    @property
    def attribute_filters(self):
        """
        Gets the attribute_filters of this QueryRequest.


        :return: The attribute_filters of this QueryRequest.
        :rtype: list[AttributeFilterItem]
        """
        return self._attribute_filters

    @attribute_filters.setter
    def attribute_filters(self, attribute_filters):
        """
        Sets the attribute_filters of this QueryRequest.


        :param attribute_filters: The attribute_filters of this QueryRequest.
        :type: list[AttributeFilterItem]
        """
        

        self._attribute_filters = attribute_filters

    @property
    def include_shares(self):
        """
        Gets the include_shares of this QueryRequest.


        :return: The include_shares of this QueryRequest.
        :rtype: bool
        """
        return self._include_shares

    @include_shares.setter
    def include_shares(self, include_shares):
        """
        Sets the include_shares of this QueryRequest.


        :param include_shares: The include_shares of this QueryRequest.
        :type: bool
        """
        

        self._include_shares = include_shares

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

