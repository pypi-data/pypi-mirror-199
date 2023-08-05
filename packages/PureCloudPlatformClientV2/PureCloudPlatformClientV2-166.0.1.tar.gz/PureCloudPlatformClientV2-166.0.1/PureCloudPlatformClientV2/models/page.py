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

class Page(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Page - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'version_id': 'str',
            'created_date': 'datetime',
            'modified_date': 'datetime',
            'root_container': 'dict(str, object)',
            'properties': 'dict(str, object)',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'version_id': 'versionId',
            'created_date': 'createdDate',
            'modified_date': 'modifiedDate',
            'root_container': 'rootContainer',
            'properties': 'properties',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._version_id = None
        self._created_date = None
        self._modified_date = None
        self._root_container = None
        self._properties = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this Page.
        The globally unique identifier for the object.

        :return: The id of this Page.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Page.
        The globally unique identifier for the object.

        :param id: The id of this Page.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Page.


        :return: The name of this Page.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Page.


        :param name: The name of this Page.
        :type: str
        """
        

        self._name = name

    @property
    def version_id(self):
        """
        Gets the version_id of this Page.


        :return: The version_id of this Page.
        :rtype: str
        """
        return self._version_id

    @version_id.setter
    def version_id(self, version_id):
        """
        Sets the version_id of this Page.


        :param version_id: The version_id of this Page.
        :type: str
        """
        

        self._version_id = version_id

    @property
    def created_date(self):
        """
        Gets the created_date of this Page.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The created_date of this Page.
        :rtype: datetime
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """
        Sets the created_date of this Page.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param created_date: The created_date of this Page.
        :type: datetime
        """
        

        self._created_date = created_date

    @property
    def modified_date(self):
        """
        Gets the modified_date of this Page.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The modified_date of this Page.
        :rtype: datetime
        """
        return self._modified_date

    @modified_date.setter
    def modified_date(self, modified_date):
        """
        Sets the modified_date of this Page.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param modified_date: The modified_date of this Page.
        :type: datetime
        """
        

        self._modified_date = modified_date

    @property
    def root_container(self):
        """
        Gets the root_container of this Page.


        :return: The root_container of this Page.
        :rtype: dict(str, object)
        """
        return self._root_container

    @root_container.setter
    def root_container(self, root_container):
        """
        Sets the root_container of this Page.


        :param root_container: The root_container of this Page.
        :type: dict(str, object)
        """
        

        self._root_container = root_container

    @property
    def properties(self):
        """
        Gets the properties of this Page.


        :return: The properties of this Page.
        :rtype: dict(str, object)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this Page.


        :param properties: The properties of this Page.
        :type: dict(str, object)
        """
        

        self._properties = properties

    @property
    def self_uri(self):
        """
        Gets the self_uri of this Page.
        The URI for this object

        :return: The self_uri of this Page.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this Page.
        The URI for this object

        :param self_uri: The self_uri of this Page.
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

