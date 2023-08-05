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

class V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'type': 'str',
            'session_id': 'str',
            'session_join_token': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'session_id': 'sessionId',
            'session_join_token': 'sessionJoinToken'
        }

        self._type = None
        self._session_id = None
        self._session_join_token = None

    @property
    def type(self):
        """
        Gets the type of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.


        :return: The type of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.


        :param type: The type of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.
        :type: str
        """
        allowed_values = ["Offering", "OfferingExpired", "OfferingAccepted", "OfferingRejected"]
        if type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for type -> " + type)
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def session_id(self):
        """
        Gets the session_id of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.


        :return: The session_id of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """
        Sets the session_id of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.


        :param session_id: The session_id of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.
        :type: str
        """
        

        self._session_id = session_id

    @property
    def session_join_token(self):
        """
        Gets the session_join_token of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.


        :return: The session_join_token of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.
        :rtype: str
        """
        return self._session_join_token

    @session_join_token.setter
    def session_join_token(self, session_join_token):
        """
        Sets the session_join_token of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.


        :param session_join_token: The session_join_token of this V2ConversationMessageTypingEventForUserTopicConversationEventCoBrowse.
        :type: str
        """
        

        self._session_join_token = session_join_token

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

