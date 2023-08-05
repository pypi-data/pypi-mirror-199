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

class V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'nickname': 'str',
            'id': 'str',
            'id_type': 'str',
            'image': 'str',
            'first_name': 'str',
            'last_name': 'str',
            'email': 'str',
            'additional_ids': 'list[V2ConversationMessageTypingEventForWorkflowTopicConversationRecipientAdditionalIdentifier]'
        }

        self.attribute_map = {
            'nickname': 'nickname',
            'id': 'id',
            'id_type': 'idType',
            'image': 'image',
            'first_name': 'firstName',
            'last_name': 'lastName',
            'email': 'email',
            'additional_ids': 'additionalIds'
        }

        self._nickname = None
        self._id = None
        self._id_type = None
        self._image = None
        self._first_name = None
        self._last_name = None
        self._email = None
        self._additional_ids = None

    @property
    def nickname(self):
        """
        Gets the nickname of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :return: The nickname of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :rtype: str
        """
        return self._nickname

    @nickname.setter
    def nickname(self, nickname):
        """
        Sets the nickname of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :param nickname: The nickname of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :type: str
        """
        

        self._nickname = nickname

    @property
    def id(self):
        """
        Gets the id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :return: The id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :param id: The id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :type: str
        """
        

        self._id = id

    @property
    def id_type(self):
        """
        Gets the id_type of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :return: The id_type of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :rtype: str
        """
        return self._id_type

    @id_type.setter
    def id_type(self, id_type):
        """
        Sets the id_type of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :param id_type: The id_type of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :type: str
        """
        allowed_values = ["Email", "Phone", "Opaque"]
        if id_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for id_type -> " + id_type)
            self._id_type = "outdated_sdk_version"
        else:
            self._id_type = id_type

    @property
    def image(self):
        """
        Gets the image of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :return: The image of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """
        Sets the image of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :param image: The image of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :type: str
        """
        

        self._image = image

    @property
    def first_name(self):
        """
        Gets the first_name of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :return: The first_name of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """
        Sets the first_name of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :param first_name: The first_name of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :type: str
        """
        

        self._first_name = first_name

    @property
    def last_name(self):
        """
        Gets the last_name of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :return: The last_name of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """
        Sets the last_name of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :param last_name: The last_name of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :type: str
        """
        

        self._last_name = last_name

    @property
    def email(self):
        """
        Gets the email of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :return: The email of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :param email: The email of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :type: str
        """
        

        self._email = email

    @property
    def additional_ids(self):
        """
        Gets the additional_ids of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :return: The additional_ids of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :rtype: list[V2ConversationMessageTypingEventForWorkflowTopicConversationRecipientAdditionalIdentifier]
        """
        return self._additional_ids

    @additional_ids.setter
    def additional_ids(self, additional_ids):
        """
        Sets the additional_ids of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.


        :param additional_ids: The additional_ids of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient.
        :type: list[V2ConversationMessageTypingEventForWorkflowTopicConversationRecipientAdditionalIdentifier]
        """
        

        self._additional_ids = additional_ids

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

