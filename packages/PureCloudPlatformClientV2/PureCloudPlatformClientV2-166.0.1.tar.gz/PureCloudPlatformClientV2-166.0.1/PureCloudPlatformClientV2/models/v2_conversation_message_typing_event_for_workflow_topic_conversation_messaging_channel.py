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

class V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'platform': 'str',
            'message_id': 'str',
            'to': 'V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient',
            'pcFrom': 'V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingFromRecipient',
            'time': 'datetime',
            'date_modified': 'datetime',
            'date_deleted': 'datetime',
            'metadata': 'V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannelMetadata'
        }

        self.attribute_map = {
            'id': 'id',
            'platform': 'platform',
            'message_id': 'messageId',
            'to': 'to',
            'pcFrom': 'from',
            'time': 'time',
            'date_modified': 'dateModified',
            'date_deleted': 'dateDeleted',
            'metadata': 'metadata'
        }

        self._id = None
        self._platform = None
        self._message_id = None
        self._to = None
        self._pcFrom = None
        self._time = None
        self._date_modified = None
        self._date_deleted = None
        self._metadata = None

    @property
    def id(self):
        """
        Gets the id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :return: The id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :param id: The id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :type: str
        """
        

        self._id = id

    @property
    def platform(self):
        """
        Gets the platform of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :return: The platform of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """
        Sets the platform of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :param platform: The platform of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :type: str
        """
        allowed_values = ["Twitter", "Facebook", "Instagram", "Line", "Whatsapp", "WebMessaging", "Open", "Sms"]
        if platform.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for platform -> " + platform)
            self._platform = "outdated_sdk_version"
        else:
            self._platform = platform

    @property
    def message_id(self):
        """
        Gets the message_id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :return: The message_id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :rtype: str
        """
        return self._message_id

    @message_id.setter
    def message_id(self, message_id):
        """
        Sets the message_id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :param message_id: The message_id of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :type: str
        """
        

        self._message_id = message_id

    @property
    def to(self):
        """
        Gets the to of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :return: The to of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :rtype: V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient
        """
        return self._to

    @to.setter
    def to(self, to):
        """
        Sets the to of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :param to: The to of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :type: V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingToRecipient
        """
        

        self._to = to

    @property
    def pcFrom(self):
        """
        Gets the pcFrom of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :return: The pcFrom of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :rtype: V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingFromRecipient
        """
        return self._pcFrom

    @pcFrom.setter
    def pcFrom(self, pcFrom):
        """
        Sets the pcFrom of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :param pcFrom: The pcFrom of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :type: V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingFromRecipient
        """
        

        self._pcFrom = pcFrom

    @property
    def time(self):
        """
        Gets the time of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :return: The time of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """
        Sets the time of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :param time: The time of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :type: datetime
        """
        

        self._time = time

    @property
    def date_modified(self):
        """
        Gets the date_modified of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :return: The date_modified of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :param date_modified: The date_modified of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :type: datetime
        """
        

        self._date_modified = date_modified

    @property
    def date_deleted(self):
        """
        Gets the date_deleted of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :return: The date_deleted of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :rtype: datetime
        """
        return self._date_deleted

    @date_deleted.setter
    def date_deleted(self, date_deleted):
        """
        Sets the date_deleted of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :param date_deleted: The date_deleted of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :type: datetime
        """
        

        self._date_deleted = date_deleted

    @property
    def metadata(self):
        """
        Gets the metadata of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :return: The metadata of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :rtype: V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannelMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.


        :param metadata: The metadata of this V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannel.
        :type: V2ConversationMessageTypingEventForWorkflowTopicConversationMessagingChannelMetadata
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

