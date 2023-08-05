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

class ConversationUserDisposition(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ConversationUserDisposition - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'code': 'str',
            'notes': 'str',
            'user': 'AddressableEntityRef'
        }

        self.attribute_map = {
            'code': 'code',
            'notes': 'notes',
            'user': 'user'
        }

        self._code = None
        self._notes = None
        self._user = None

    @property
    def code(self):
        """
        Gets the code of this ConversationUserDisposition.
        User-defined wrap-up code for the conversation.

        :return: The code of this ConversationUserDisposition.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this ConversationUserDisposition.
        User-defined wrap-up code for the conversation.

        :param code: The code of this ConversationUserDisposition.
        :type: str
        """
        

        self._code = code

    @property
    def notes(self):
        """
        Gets the notes of this ConversationUserDisposition.
        Text entered by the user to describe the call or disposition.

        :return: The notes of this ConversationUserDisposition.
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """
        Sets the notes of this ConversationUserDisposition.
        Text entered by the user to describe the call or disposition.

        :param notes: The notes of this ConversationUserDisposition.
        :type: str
        """
        

        self._notes = notes

    @property
    def user(self):
        """
        Gets the user of this ConversationUserDisposition.
        The user that wrapped up the conversation.

        :return: The user of this ConversationUserDisposition.
        :rtype: AddressableEntityRef
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this ConversationUserDisposition.
        The user that wrapped up the conversation.

        :param user: The user of this ConversationUserDisposition.
        :type: AddressableEntityRef
        """
        

        self._user = user

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

