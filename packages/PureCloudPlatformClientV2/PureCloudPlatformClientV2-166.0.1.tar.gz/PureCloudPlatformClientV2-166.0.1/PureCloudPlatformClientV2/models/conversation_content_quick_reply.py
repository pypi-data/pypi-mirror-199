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

class ConversationContentQuickReply(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ConversationContentQuickReply - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'text': 'str',
            'payload': 'str',
            'image': 'str',
            'action': 'str'
        }

        self.attribute_map = {
            'text': 'text',
            'payload': 'payload',
            'image': 'image',
            'action': 'action'
        }

        self._text = None
        self._payload = None
        self._image = None
        self._action = None

    @property
    def text(self):
        """
        Gets the text of this ConversationContentQuickReply.
        Text to show inside the quick reply. This is also used as the response text after clicking on the quick reply.

        :return: The text of this ConversationContentQuickReply.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Sets the text of this ConversationContentQuickReply.
        Text to show inside the quick reply. This is also used as the response text after clicking on the quick reply.

        :param text: The text of this ConversationContentQuickReply.
        :type: str
        """
        

        self._text = text

    @property
    def payload(self):
        """
        Gets the payload of this ConversationContentQuickReply.
        Content of the payload included in the quick reply response. Could be an ID identifying the quick reply response.

        :return: The payload of this ConversationContentQuickReply.
        :rtype: str
        """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """
        Sets the payload of this ConversationContentQuickReply.
        Content of the payload included in the quick reply response. Could be an ID identifying the quick reply response.

        :param payload: The payload of this ConversationContentQuickReply.
        :type: str
        """
        

        self._payload = payload

    @property
    def image(self):
        """
        Gets the image of this ConversationContentQuickReply.
        URL of an image associated with the quick reply.

        :return: The image of this ConversationContentQuickReply.
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """
        Sets the image of this ConversationContentQuickReply.
        URL of an image associated with the quick reply.

        :param image: The image of this ConversationContentQuickReply.
        :type: str
        """
        

        self._image = image

    @property
    def action(self):
        """
        Gets the action of this ConversationContentQuickReply.
        Specifies the type of action that is triggered upon clicking the quick reply.

        :return: The action of this ConversationContentQuickReply.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this ConversationContentQuickReply.
        Specifies the type of action that is triggered upon clicking the quick reply.

        :param action: The action of this ConversationContentQuickReply.
        :type: str
        """
        allowed_values = ["Message"]
        if action.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for action -> " + action)
            self._action = "outdated_sdk_version"
        else:
            self._action = action

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

