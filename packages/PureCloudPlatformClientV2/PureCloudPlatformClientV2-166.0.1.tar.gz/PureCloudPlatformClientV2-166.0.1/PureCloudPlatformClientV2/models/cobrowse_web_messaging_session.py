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

class CobrowseWebMessagingSession(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CobrowseWebMessagingSession - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'join_code': 'str',
            'websocket_url': 'str',
            'date_offer_ends': 'datetime',
            'communication_type': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'join_code': 'joinCode',
            'websocket_url': 'websocketUrl',
            'date_offer_ends': 'dateOfferEnds',
            'communication_type': 'communicationType',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._join_code = None
        self._websocket_url = None
        self._date_offer_ends = None
        self._communication_type = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this CobrowseWebMessagingSession.
        The globally unique identifier for the object.

        :return: The id of this CobrowseWebMessagingSession.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this CobrowseWebMessagingSession.
        The globally unique identifier for the object.

        :param id: The id of this CobrowseWebMessagingSession.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this CobrowseWebMessagingSession.


        :return: The name of this CobrowseWebMessagingSession.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CobrowseWebMessagingSession.


        :param name: The name of this CobrowseWebMessagingSession.
        :type: str
        """
        

        self._name = name

    @property
    def join_code(self):
        """
        Gets the join_code of this CobrowseWebMessagingSession.
        Cobrowse session join code

        :return: The join_code of this CobrowseWebMessagingSession.
        :rtype: str
        """
        return self._join_code

    @join_code.setter
    def join_code(self, join_code):
        """
        Sets the join_code of this CobrowseWebMessagingSession.
        Cobrowse session join code

        :param join_code: The join_code of this CobrowseWebMessagingSession.
        :type: str
        """
        

        self._join_code = join_code

    @property
    def websocket_url(self):
        """
        Gets the websocket_url of this CobrowseWebMessagingSession.
        WebSocket URL for the JS client

        :return: The websocket_url of this CobrowseWebMessagingSession.
        :rtype: str
        """
        return self._websocket_url

    @websocket_url.setter
    def websocket_url(self, websocket_url):
        """
        Sets the websocket_url of this CobrowseWebMessagingSession.
        WebSocket URL for the JS client

        :param websocket_url: The websocket_url of this CobrowseWebMessagingSession.
        :type: str
        """
        

        self._websocket_url = websocket_url

    @property
    def date_offer_ends(self):
        """
        Gets the date_offer_ends of this CobrowseWebMessagingSession.
        Date when Cobrowse Offer Expires. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_offer_ends of this CobrowseWebMessagingSession.
        :rtype: datetime
        """
        return self._date_offer_ends

    @date_offer_ends.setter
    def date_offer_ends(self, date_offer_ends):
        """
        Sets the date_offer_ends of this CobrowseWebMessagingSession.
        Date when Cobrowse Offer Expires. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_offer_ends: The date_offer_ends of this CobrowseWebMessagingSession.
        :type: datetime
        """
        

        self._date_offer_ends = date_offer_ends

    @property
    def communication_type(self):
        """
        Gets the communication_type of this CobrowseWebMessagingSession.
        CommunicationType for Cobrowse Session

        :return: The communication_type of this CobrowseWebMessagingSession.
        :rtype: str
        """
        return self._communication_type

    @communication_type.setter
    def communication_type(self, communication_type):
        """
        Sets the communication_type of this CobrowseWebMessagingSession.
        CommunicationType for Cobrowse Session

        :param communication_type: The communication_type of this CobrowseWebMessagingSession.
        :type: str
        """
        allowed_values = ["Call", "Message"]
        if communication_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for communication_type -> " + communication_type)
            self._communication_type = "outdated_sdk_version"
        else:
            self._communication_type = communication_type

    @property
    def self_uri(self):
        """
        Gets the self_uri of this CobrowseWebMessagingSession.
        The URI for this object

        :return: The self_uri of this CobrowseWebMessagingSession.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this CobrowseWebMessagingSession.
        The URI for this object

        :param self_uri: The self_uri of this CobrowseWebMessagingSession.
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

