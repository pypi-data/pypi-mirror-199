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

class UserTokensTopicTokenNotification(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        UserTokensTopicTokenNotification - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'user': 'UserTokensTopicUriReference',
            'ip_address': 'str',
            'date_created': 'str',
            'token_expiration_date': 'str',
            'session_id': 'str',
            'client_id': 'str',
            'token_hash': 'str'
        }

        self.attribute_map = {
            'user': 'user',
            'ip_address': 'ipAddress',
            'date_created': 'dateCreated',
            'token_expiration_date': 'tokenExpirationDate',
            'session_id': 'sessionId',
            'client_id': 'clientId',
            'token_hash': 'tokenHash'
        }

        self._user = None
        self._ip_address = None
        self._date_created = None
        self._token_expiration_date = None
        self._session_id = None
        self._client_id = None
        self._token_hash = None

    @property
    def user(self):
        """
        Gets the user of this UserTokensTopicTokenNotification.


        :return: The user of this UserTokensTopicTokenNotification.
        :rtype: UserTokensTopicUriReference
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this UserTokensTopicTokenNotification.


        :param user: The user of this UserTokensTopicTokenNotification.
        :type: UserTokensTopicUriReference
        """
        

        self._user = user

    @property
    def ip_address(self):
        """
        Gets the ip_address of this UserTokensTopicTokenNotification.


        :return: The ip_address of this UserTokensTopicTokenNotification.
        :rtype: str
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        """
        Sets the ip_address of this UserTokensTopicTokenNotification.


        :param ip_address: The ip_address of this UserTokensTopicTokenNotification.
        :type: str
        """
        

        self._ip_address = ip_address

    @property
    def date_created(self):
        """
        Gets the date_created of this UserTokensTopicTokenNotification.


        :return: The date_created of this UserTokensTopicTokenNotification.
        :rtype: str
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this UserTokensTopicTokenNotification.


        :param date_created: The date_created of this UserTokensTopicTokenNotification.
        :type: str
        """
        

        self._date_created = date_created

    @property
    def token_expiration_date(self):
        """
        Gets the token_expiration_date of this UserTokensTopicTokenNotification.


        :return: The token_expiration_date of this UserTokensTopicTokenNotification.
        :rtype: str
        """
        return self._token_expiration_date

    @token_expiration_date.setter
    def token_expiration_date(self, token_expiration_date):
        """
        Sets the token_expiration_date of this UserTokensTopicTokenNotification.


        :param token_expiration_date: The token_expiration_date of this UserTokensTopicTokenNotification.
        :type: str
        """
        

        self._token_expiration_date = token_expiration_date

    @property
    def session_id(self):
        """
        Gets the session_id of this UserTokensTopicTokenNotification.


        :return: The session_id of this UserTokensTopicTokenNotification.
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """
        Sets the session_id of this UserTokensTopicTokenNotification.


        :param session_id: The session_id of this UserTokensTopicTokenNotification.
        :type: str
        """
        

        self._session_id = session_id

    @property
    def client_id(self):
        """
        Gets the client_id of this UserTokensTopicTokenNotification.


        :return: The client_id of this UserTokensTopicTokenNotification.
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """
        Sets the client_id of this UserTokensTopicTokenNotification.


        :param client_id: The client_id of this UserTokensTopicTokenNotification.
        :type: str
        """
        

        self._client_id = client_id

    @property
    def token_hash(self):
        """
        Gets the token_hash of this UserTokensTopicTokenNotification.


        :return: The token_hash of this UserTokensTopicTokenNotification.
        :rtype: str
        """
        return self._token_hash

    @token_hash.setter
    def token_hash(self, token_hash):
        """
        Sets the token_hash of this UserTokensTopicTokenNotification.


        :param token_hash: The token_hash of this UserTokensTopicTokenNotification.
        :type: str
        """
        

        self._token_hash = token_hash

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

