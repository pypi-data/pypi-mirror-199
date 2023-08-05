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

class ProgressTransferEvent(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ProgressTransferEvent - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'event_id': 'str',
            'event_date_time': 'datetime',
            'conversation_id': 'str',
            'command_id': 'str',
            'object_communication_id': 'str',
            'destination_communication_id': 'str'
        }

        self.attribute_map = {
            'event_id': 'eventId',
            'event_date_time': 'eventDateTime',
            'conversation_id': 'conversationId',
            'command_id': 'commandId',
            'object_communication_id': 'objectCommunicationId',
            'destination_communication_id': 'destinationCommunicationId'
        }

        self._event_id = None
        self._event_date_time = None
        self._conversation_id = None
        self._command_id = None
        self._object_communication_id = None
        self._destination_communication_id = None

    @property
    def event_id(self):
        """
        Gets the event_id of this ProgressTransferEvent.
        A unique (V4 UUID) eventId for this event

        :return: The event_id of this ProgressTransferEvent.
        :rtype: str
        """
        return self._event_id

    @event_id.setter
    def event_id(self, event_id):
        """
        Sets the event_id of this ProgressTransferEvent.
        A unique (V4 UUID) eventId for this event

        :param event_id: The event_id of this ProgressTransferEvent.
        :type: str
        """
        

        self._event_id = event_id

    @property
    def event_date_time(self):
        """
        Gets the event_date_time of this ProgressTransferEvent.
        A Date Time representing the time this event occurred. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The event_date_time of this ProgressTransferEvent.
        :rtype: datetime
        """
        return self._event_date_time

    @event_date_time.setter
    def event_date_time(self, event_date_time):
        """
        Sets the event_date_time of this ProgressTransferEvent.
        A Date Time representing the time this event occurred. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param event_date_time: The event_date_time of this ProgressTransferEvent.
        :type: datetime
        """
        

        self._event_date_time = event_date_time

    @property
    def conversation_id(self):
        """
        Gets the conversation_id of this ProgressTransferEvent.
        A unique Id (V4 UUID) identifying this conversation

        :return: The conversation_id of this ProgressTransferEvent.
        :rtype: str
        """
        return self._conversation_id

    @conversation_id.setter
    def conversation_id(self, conversation_id):
        """
        Sets the conversation_id of this ProgressTransferEvent.
        A unique Id (V4 UUID) identifying this conversation

        :param conversation_id: The conversation_id of this ProgressTransferEvent.
        :type: str
        """
        

        self._conversation_id = conversation_id

    @property
    def command_id(self):
        """
        Gets the command_id of this ProgressTransferEvent.
        The id (V4 UUID) used to identify the transfer already started by the external platform.

        :return: The command_id of this ProgressTransferEvent.
        :rtype: str
        """
        return self._command_id

    @command_id.setter
    def command_id(self, command_id):
        """
        Sets the command_id of this ProgressTransferEvent.
        The id (V4 UUID) used to identify the transfer already started by the external platform.

        :param command_id: The command_id of this ProgressTransferEvent.
        :type: str
        """
        

        self._command_id = command_id

    @property
    def object_communication_id(self):
        """
        Gets the object_communication_id of this ProgressTransferEvent.
        The id (V4 UUID) of the communication that is being transferred.

        :return: The object_communication_id of this ProgressTransferEvent.
        :rtype: str
        """
        return self._object_communication_id

    @object_communication_id.setter
    def object_communication_id(self, object_communication_id):
        """
        Sets the object_communication_id of this ProgressTransferEvent.
        The id (V4 UUID) of the communication that is being transferred.

        :param object_communication_id: The object_communication_id of this ProgressTransferEvent.
        :type: str
        """
        

        self._object_communication_id = object_communication_id

    @property
    def destination_communication_id(self):
        """
        Gets the destination_communication_id of this ProgressTransferEvent.
        The id (V4 UUID) of the communication that is being transferred to.

        :return: The destination_communication_id of this ProgressTransferEvent.
        :rtype: str
        """
        return self._destination_communication_id

    @destination_communication_id.setter
    def destination_communication_id(self, destination_communication_id):
        """
        Sets the destination_communication_id of this ProgressTransferEvent.
        The id (V4 UUID) of the communication that is being transferred to.

        :param destination_communication_id: The destination_communication_id of this ProgressTransferEvent.
        :type: str
        """
        

        self._destination_communication_id = destination_communication_id

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

