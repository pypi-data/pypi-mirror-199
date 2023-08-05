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

class FlowStartDetailEventTopicFlowStartEvent(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        FlowStartDetailEventTopicFlowStartEvent - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'event_time': 'int',
            'conversation_id': 'str',
            'participant_id': 'str',
            'session_id': 'str',
            'media_type': 'str',
            'provider': 'str',
            'direction': 'str',
            'ani': 'str',
            'dnis': 'str',
            'address_to': 'str',
            'address_from': 'str',
            'subject': 'str',
            'message_type': 'str',
            'flow_type': 'str',
            'flow_id': 'str',
            'division_id': 'str',
            'flow_version': 'str'
        }

        self.attribute_map = {
            'event_time': 'eventTime',
            'conversation_id': 'conversationId',
            'participant_id': 'participantId',
            'session_id': 'sessionId',
            'media_type': 'mediaType',
            'provider': 'provider',
            'direction': 'direction',
            'ani': 'ani',
            'dnis': 'dnis',
            'address_to': 'addressTo',
            'address_from': 'addressFrom',
            'subject': 'subject',
            'message_type': 'messageType',
            'flow_type': 'flowType',
            'flow_id': 'flowId',
            'division_id': 'divisionId',
            'flow_version': 'flowVersion'
        }

        self._event_time = None
        self._conversation_id = None
        self._participant_id = None
        self._session_id = None
        self._media_type = None
        self._provider = None
        self._direction = None
        self._ani = None
        self._dnis = None
        self._address_to = None
        self._address_from = None
        self._subject = None
        self._message_type = None
        self._flow_type = None
        self._flow_id = None
        self._division_id = None
        self._flow_version = None

    @property
    def event_time(self):
        """
        Gets the event_time of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The event_time of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: int
        """
        return self._event_time

    @event_time.setter
    def event_time(self, event_time):
        """
        Sets the event_time of this FlowStartDetailEventTopicFlowStartEvent.


        :param event_time: The event_time of this FlowStartDetailEventTopicFlowStartEvent.
        :type: int
        """
        

        self._event_time = event_time

    @property
    def conversation_id(self):
        """
        Gets the conversation_id of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The conversation_id of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._conversation_id

    @conversation_id.setter
    def conversation_id(self, conversation_id):
        """
        Sets the conversation_id of this FlowStartDetailEventTopicFlowStartEvent.


        :param conversation_id: The conversation_id of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._conversation_id = conversation_id

    @property
    def participant_id(self):
        """
        Gets the participant_id of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The participant_id of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._participant_id

    @participant_id.setter
    def participant_id(self, participant_id):
        """
        Sets the participant_id of this FlowStartDetailEventTopicFlowStartEvent.


        :param participant_id: The participant_id of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._participant_id = participant_id

    @property
    def session_id(self):
        """
        Gets the session_id of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The session_id of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """
        Sets the session_id of this FlowStartDetailEventTopicFlowStartEvent.


        :param session_id: The session_id of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._session_id = session_id

    @property
    def media_type(self):
        """
        Gets the media_type of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The media_type of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        """
        Sets the media_type of this FlowStartDetailEventTopicFlowStartEvent.


        :param media_type: The media_type of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        allowed_values = ["UNKNOWN", "VOICE", "CHAT", "EMAIL", "CALLBACK", "COBROWSE", "VIDEO", "SCREENSHARE", "MESSAGE"]
        if media_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for media_type -> " + media_type)
            self._media_type = "outdated_sdk_version"
        else:
            self._media_type = media_type

    @property
    def provider(self):
        """
        Gets the provider of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The provider of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this FlowStartDetailEventTopicFlowStartEvent.


        :param provider: The provider of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._provider = provider

    @property
    def direction(self):
        """
        Gets the direction of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The direction of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """
        Sets the direction of this FlowStartDetailEventTopicFlowStartEvent.


        :param direction: The direction of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        allowed_values = ["UNKNOWN", "INBOUND", "OUTBOUND"]
        if direction.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for direction -> " + direction)
            self._direction = "outdated_sdk_version"
        else:
            self._direction = direction

    @property
    def ani(self):
        """
        Gets the ani of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The ani of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._ani

    @ani.setter
    def ani(self, ani):
        """
        Sets the ani of this FlowStartDetailEventTopicFlowStartEvent.


        :param ani: The ani of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._ani = ani

    @property
    def dnis(self):
        """
        Gets the dnis of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The dnis of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._dnis

    @dnis.setter
    def dnis(self, dnis):
        """
        Sets the dnis of this FlowStartDetailEventTopicFlowStartEvent.


        :param dnis: The dnis of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._dnis = dnis

    @property
    def address_to(self):
        """
        Gets the address_to of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The address_to of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._address_to

    @address_to.setter
    def address_to(self, address_to):
        """
        Sets the address_to of this FlowStartDetailEventTopicFlowStartEvent.


        :param address_to: The address_to of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._address_to = address_to

    @property
    def address_from(self):
        """
        Gets the address_from of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The address_from of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._address_from

    @address_from.setter
    def address_from(self, address_from):
        """
        Sets the address_from of this FlowStartDetailEventTopicFlowStartEvent.


        :param address_from: The address_from of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._address_from = address_from

    @property
    def subject(self):
        """
        Gets the subject of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The subject of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """
        Sets the subject of this FlowStartDetailEventTopicFlowStartEvent.


        :param subject: The subject of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._subject = subject

    @property
    def message_type(self):
        """
        Gets the message_type of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The message_type of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._message_type

    @message_type.setter
    def message_type(self, message_type):
        """
        Sets the message_type of this FlowStartDetailEventTopicFlowStartEvent.


        :param message_type: The message_type of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        allowed_values = ["UNKNOWN", "SMS", "TWITTER", "FACEBOOK", "LINE", "WHATSAPP", "WEBMESSAGING", "OPEN", "INSTAGRAM"]
        if message_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for message_type -> " + message_type)
            self._message_type = "outdated_sdk_version"
        else:
            self._message_type = message_type

    @property
    def flow_type(self):
        """
        Gets the flow_type of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The flow_type of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._flow_type

    @flow_type.setter
    def flow_type(self, flow_type):
        """
        Sets the flow_type of this FlowStartDetailEventTopicFlowStartEvent.


        :param flow_type: The flow_type of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        allowed_values = ["UNKNOWN", "INBOUNDCALL", "OUTBOUNDCALL", "INQUEUECALL", "SECURECALL", "INBOUNDEMAIL", "SURVEYINVITE", "INBOUNDSHORTMESSAGE", "INBOUNDCHAT", "WORKFLOW", "BOT", "DIGITALBOT", "COMMONMODULE", "INQUEUEEMAIL", "INQUEUESHORTMESSAGE", "VOICE", "VOICEMAIL", "WORKITEM"]
        if flow_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for flow_type -> " + flow_type)
            self._flow_type = "outdated_sdk_version"
        else:
            self._flow_type = flow_type

    @property
    def flow_id(self):
        """
        Gets the flow_id of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The flow_id of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._flow_id

    @flow_id.setter
    def flow_id(self, flow_id):
        """
        Sets the flow_id of this FlowStartDetailEventTopicFlowStartEvent.


        :param flow_id: The flow_id of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._flow_id = flow_id

    @property
    def division_id(self):
        """
        Gets the division_id of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The division_id of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._division_id

    @division_id.setter
    def division_id(self, division_id):
        """
        Sets the division_id of this FlowStartDetailEventTopicFlowStartEvent.


        :param division_id: The division_id of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._division_id = division_id

    @property
    def flow_version(self):
        """
        Gets the flow_version of this FlowStartDetailEventTopicFlowStartEvent.


        :return: The flow_version of this FlowStartDetailEventTopicFlowStartEvent.
        :rtype: str
        """
        return self._flow_version

    @flow_version.setter
    def flow_version(self, flow_version):
        """
        Sets the flow_version of this FlowStartDetailEventTopicFlowStartEvent.


        :param flow_version: The flow_version of this FlowStartDetailEventTopicFlowStartEvent.
        :type: str
        """
        

        self._flow_version = flow_version

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

