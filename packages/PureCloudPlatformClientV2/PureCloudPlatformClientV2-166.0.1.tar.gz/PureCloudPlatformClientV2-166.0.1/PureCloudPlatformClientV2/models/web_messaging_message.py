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

class WebMessagingMessage(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WebMessagingMessage - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'channel': 'WebMessagingChannel',
            'type': 'str',
            'text': 'str',
            'content': 'list[WebMessagingContent]',
            'events': 'list[WebMessagingEvent]',
            'direction': 'str',
            'originating_entity': 'str',
            'metadata': 'dict(str, str)'
        }

        self.attribute_map = {
            'id': 'id',
            'channel': 'channel',
            'type': 'type',
            'text': 'text',
            'content': 'content',
            'events': 'events',
            'direction': 'direction',
            'originating_entity': 'originatingEntity',
            'metadata': 'metadata'
        }

        self._id = None
        self._channel = None
        self._type = None
        self._text = None
        self._content = None
        self._events = None
        self._direction = None
        self._originating_entity = None
        self._metadata = None

    @property
    def id(self):
        """
        Gets the id of this WebMessagingMessage.
        Unique ID of the message. This ID is generated by Messaging Platform. Message receipts will have the same ID as the message they reference.

        :return: The id of this WebMessagingMessage.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WebMessagingMessage.
        Unique ID of the message. This ID is generated by Messaging Platform. Message receipts will have the same ID as the message they reference.

        :param id: The id of this WebMessagingMessage.
        :type: str
        """
        

        self._id = id

    @property
    def channel(self):
        """
        Gets the channel of this WebMessagingMessage.
        Channel-specific information that describes the message and the message channel/provider.

        :return: The channel of this WebMessagingMessage.
        :rtype: WebMessagingChannel
        """
        return self._channel

    @channel.setter
    def channel(self, channel):
        """
        Sets the channel of this WebMessagingMessage.
        Channel-specific information that describes the message and the message channel/provider.

        :param channel: The channel of this WebMessagingMessage.
        :type: WebMessagingChannel
        """
        

        self._channel = channel

    @property
    def type(self):
        """
        Gets the type of this WebMessagingMessage.
        Message type.

        :return: The type of this WebMessagingMessage.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this WebMessagingMessage.
        Message type.

        :param type: The type of this WebMessagingMessage.
        :type: str
        """
        allowed_values = ["Text", "Structured", "Receipt", "Event"]
        if type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for type -> " + type)
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def text(self):
        """
        Gets the text of this WebMessagingMessage.
        Message text.

        :return: The text of this WebMessagingMessage.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Sets the text of this WebMessagingMessage.
        Message text.

        :param text: The text of this WebMessagingMessage.
        :type: str
        """
        

        self._text = text

    @property
    def content(self):
        """
        Gets the content of this WebMessagingMessage.
        List of content elements.

        :return: The content of this WebMessagingMessage.
        :rtype: list[WebMessagingContent]
        """
        return self._content

    @content.setter
    def content(self, content):
        """
        Sets the content of this WebMessagingMessage.
        List of content elements.

        :param content: The content of this WebMessagingMessage.
        :type: list[WebMessagingContent]
        """
        

        self._content = content

    @property
    def events(self):
        """
        Gets the events of this WebMessagingMessage.
        List of event elements.

        :return: The events of this WebMessagingMessage.
        :rtype: list[WebMessagingEvent]
        """
        return self._events

    @events.setter
    def events(self, events):
        """
        Sets the events of this WebMessagingMessage.
        List of event elements.

        :param events: The events of this WebMessagingMessage.
        :type: list[WebMessagingEvent]
        """
        

        self._events = events

    @property
    def direction(self):
        """
        Gets the direction of this WebMessagingMessage.
        The direction of the message.  Direction is always from the perspective of the Genesys Cloud platform.  An Inbound message is one sent from a guest to the Genesys Cloud Platform.  An Outbound message is one sent from the Genesys Cloud Platform to a guest.

        :return: The direction of this WebMessagingMessage.
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """
        Sets the direction of this WebMessagingMessage.
        The direction of the message.  Direction is always from the perspective of the Genesys Cloud platform.  An Inbound message is one sent from a guest to the Genesys Cloud Platform.  An Outbound message is one sent from the Genesys Cloud Platform to a guest.

        :param direction: The direction of this WebMessagingMessage.
        :type: str
        """
        allowed_values = ["Inbound", "Outbound"]
        if direction.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for direction -> " + direction)
            self._direction = "outdated_sdk_version"
        else:
            self._direction = direction

    @property
    def originating_entity(self):
        """
        Gets the originating_entity of this WebMessagingMessage.
        Specifies if this message was sent by a human agent or bot. The platform may use this to apply appropriate provider policies.

        :return: The originating_entity of this WebMessagingMessage.
        :rtype: str
        """
        return self._originating_entity

    @originating_entity.setter
    def originating_entity(self, originating_entity):
        """
        Sets the originating_entity of this WebMessagingMessage.
        Specifies if this message was sent by a human agent or bot. The platform may use this to apply appropriate provider policies.

        :param originating_entity: The originating_entity of this WebMessagingMessage.
        :type: str
        """
        allowed_values = ["Human", "Bot"]
        if originating_entity.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for originating_entity -> " + originating_entity)
            self._originating_entity = "outdated_sdk_version"
        else:
            self._originating_entity = originating_entity

    @property
    def metadata(self):
        """
        Gets the metadata of this WebMessagingMessage.
        Additional metadata about this message.

        :return: The metadata of this WebMessagingMessage.
        :rtype: dict(str, str)
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this WebMessagingMessage.
        Additional metadata about this message.

        :param metadata: The metadata of this WebMessagingMessage.
        :type: dict(str, str)
        """
        

        self._metadata = metadata

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

