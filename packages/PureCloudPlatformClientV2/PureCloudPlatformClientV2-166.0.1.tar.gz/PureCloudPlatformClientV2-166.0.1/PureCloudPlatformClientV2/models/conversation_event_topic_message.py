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

class ConversationEventTopicMessage(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ConversationEventTopicMessage - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'state': 'str',
            'initial_state': 'str',
            'direction': 'str',
            'held': 'bool',
            'error_info': 'ConversationEventTopicErrorDetails',
            'provider': 'str',
            'script_id': 'str',
            'peer_id': 'str',
            'disconnect_type': 'str',
            'start_hold_time': 'datetime',
            'connected_time': 'datetime',
            'disconnected_time': 'datetime',
            'to_address': 'ConversationEventTopicAddress',
            'from_address': 'ConversationEventTopicAddress',
            'messages': 'list[ConversationEventTopicMessageDetails]',
            'messages_transcript_uri': 'str',
            'type': 'str',
            'recipient_country': 'str',
            'recipient_type': 'str',
            'journey_context': 'ConversationEventTopicJourneyContext',
            'wrapup': 'ConversationEventTopicWrapup',
            'after_call_work': 'ConversationEventTopicAfterCallWork',
            'after_call_work_required': 'bool',
            'agent_assistant_id': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'state': 'state',
            'initial_state': 'initialState',
            'direction': 'direction',
            'held': 'held',
            'error_info': 'errorInfo',
            'provider': 'provider',
            'script_id': 'scriptId',
            'peer_id': 'peerId',
            'disconnect_type': 'disconnectType',
            'start_hold_time': 'startHoldTime',
            'connected_time': 'connectedTime',
            'disconnected_time': 'disconnectedTime',
            'to_address': 'toAddress',
            'from_address': 'fromAddress',
            'messages': 'messages',
            'messages_transcript_uri': 'messagesTranscriptUri',
            'type': 'type',
            'recipient_country': 'recipientCountry',
            'recipient_type': 'recipientType',
            'journey_context': 'journeyContext',
            'wrapup': 'wrapup',
            'after_call_work': 'afterCallWork',
            'after_call_work_required': 'afterCallWorkRequired',
            'agent_assistant_id': 'agentAssistantId'
        }

        self._id = None
        self._state = None
        self._initial_state = None
        self._direction = None
        self._held = None
        self._error_info = None
        self._provider = None
        self._script_id = None
        self._peer_id = None
        self._disconnect_type = None
        self._start_hold_time = None
        self._connected_time = None
        self._disconnected_time = None
        self._to_address = None
        self._from_address = None
        self._messages = None
        self._messages_transcript_uri = None
        self._type = None
        self._recipient_country = None
        self._recipient_type = None
        self._journey_context = None
        self._wrapup = None
        self._after_call_work = None
        self._after_call_work_required = None
        self._agent_assistant_id = None

    @property
    def id(self):
        """
        Gets the id of this ConversationEventTopicMessage.
        A globally unique identifier for this communication.

        :return: The id of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ConversationEventTopicMessage.
        A globally unique identifier for this communication.

        :param id: The id of this ConversationEventTopicMessage.
        :type: str
        """
        

        self._id = id

    @property
    def state(self):
        """
        Gets the state of this ConversationEventTopicMessage.


        :return: The state of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this ConversationEventTopicMessage.


        :param state: The state of this ConversationEventTopicMessage.
        :type: str
        """
        allowed_values = ["alerting", "connected", "disconnected"]
        if state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for state -> " + state)
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def initial_state(self):
        """
        Gets the initial_state of this ConversationEventTopicMessage.


        :return: The initial_state of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._initial_state

    @initial_state.setter
    def initial_state(self, initial_state):
        """
        Sets the initial_state of this ConversationEventTopicMessage.


        :param initial_state: The initial_state of this ConversationEventTopicMessage.
        :type: str
        """
        allowed_values = ["alerting", "connected", "disconnected"]
        if initial_state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for initial_state -> " + initial_state)
            self._initial_state = "outdated_sdk_version"
        else:
            self._initial_state = initial_state

    @property
    def direction(self):
        """
        Gets the direction of this ConversationEventTopicMessage.
        Whether a message is inbound or outbound.

        :return: The direction of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """
        Sets the direction of this ConversationEventTopicMessage.
        Whether a message is inbound or outbound.

        :param direction: The direction of this ConversationEventTopicMessage.
        :type: str
        """
        allowed_values = ["outbound", "inbound"]
        if direction.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for direction -> " + direction)
            self._direction = "outdated_sdk_version"
        else:
            self._direction = direction

    @property
    def held(self):
        """
        Gets the held of this ConversationEventTopicMessage.
        True if this call is held and the person on this side hears silence.

        :return: The held of this ConversationEventTopicMessage.
        :rtype: bool
        """
        return self._held

    @held.setter
    def held(self, held):
        """
        Sets the held of this ConversationEventTopicMessage.
        True if this call is held and the person on this side hears silence.

        :param held: The held of this ConversationEventTopicMessage.
        :type: bool
        """
        

        self._held = held

    @property
    def error_info(self):
        """
        Gets the error_info of this ConversationEventTopicMessage.
        Detailed information about an error response.

        :return: The error_info of this ConversationEventTopicMessage.
        :rtype: ConversationEventTopicErrorDetails
        """
        return self._error_info

    @error_info.setter
    def error_info(self, error_info):
        """
        Sets the error_info of this ConversationEventTopicMessage.
        Detailed information about an error response.

        :param error_info: The error_info of this ConversationEventTopicMessage.
        :type: ConversationEventTopicErrorDetails
        """
        

        self._error_info = error_info

    @property
    def provider(self):
        """
        Gets the provider of this ConversationEventTopicMessage.
        The source provider of the email.

        :return: The provider of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this ConversationEventTopicMessage.
        The source provider of the email.

        :param provider: The provider of this ConversationEventTopicMessage.
        :type: str
        """
        

        self._provider = provider

    @property
    def script_id(self):
        """
        Gets the script_id of this ConversationEventTopicMessage.
        The UUID of the script to use.

        :return: The script_id of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._script_id

    @script_id.setter
    def script_id(self, script_id):
        """
        Sets the script_id of this ConversationEventTopicMessage.
        The UUID of the script to use.

        :param script_id: The script_id of this ConversationEventTopicMessage.
        :type: str
        """
        

        self._script_id = script_id

    @property
    def peer_id(self):
        """
        Gets the peer_id of this ConversationEventTopicMessage.
        The id of the peer communication corresponding to a matching leg for this communication.

        :return: The peer_id of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._peer_id

    @peer_id.setter
    def peer_id(self, peer_id):
        """
        Sets the peer_id of this ConversationEventTopicMessage.
        The id of the peer communication corresponding to a matching leg for this communication.

        :param peer_id: The peer_id of this ConversationEventTopicMessage.
        :type: str
        """
        

        self._peer_id = peer_id

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this ConversationEventTopicMessage.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :return: The disconnect_type of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this ConversationEventTopicMessage.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :param disconnect_type: The disconnect_type of this ConversationEventTopicMessage.
        :type: str
        """
        allowed_values = ["endpoint", "client", "system", "timeout", "transfer", "transfer.conference", "transfer.consult", "transfer.forward", "transfer.noanswer", "transfer.notavailable", "transport.failure", "error", "peer", "other", "spam", "uncallable"]
        if disconnect_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for disconnect_type -> " + disconnect_type)
            self._disconnect_type = "outdated_sdk_version"
        else:
            self._disconnect_type = disconnect_type

    @property
    def start_hold_time(self):
        """
        Gets the start_hold_time of this ConversationEventTopicMessage.
        The timestamp the email was placed on hold in the cloud clock if the email is currently on hold.

        :return: The start_hold_time of this ConversationEventTopicMessage.
        :rtype: datetime
        """
        return self._start_hold_time

    @start_hold_time.setter
    def start_hold_time(self, start_hold_time):
        """
        Sets the start_hold_time of this ConversationEventTopicMessage.
        The timestamp the email was placed on hold in the cloud clock if the email is currently on hold.

        :param start_hold_time: The start_hold_time of this ConversationEventTopicMessage.
        :type: datetime
        """
        

        self._start_hold_time = start_hold_time

    @property
    def connected_time(self):
        """
        Gets the connected_time of this ConversationEventTopicMessage.
        The timestamp when this communication was connected in the cloud clock.

        :return: The connected_time of this ConversationEventTopicMessage.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this ConversationEventTopicMessage.
        The timestamp when this communication was connected in the cloud clock.

        :param connected_time: The connected_time of this ConversationEventTopicMessage.
        :type: datetime
        """
        

        self._connected_time = connected_time

    @property
    def disconnected_time(self):
        """
        Gets the disconnected_time of this ConversationEventTopicMessage.
        The timestamp when this communication disconnected from the conversation in the provider clock.

        :return: The disconnected_time of this ConversationEventTopicMessage.
        :rtype: datetime
        """
        return self._disconnected_time

    @disconnected_time.setter
    def disconnected_time(self, disconnected_time):
        """
        Sets the disconnected_time of this ConversationEventTopicMessage.
        The timestamp when this communication disconnected from the conversation in the provider clock.

        :param disconnected_time: The disconnected_time of this ConversationEventTopicMessage.
        :type: datetime
        """
        

        self._disconnected_time = disconnected_time

    @property
    def to_address(self):
        """
        Gets the to_address of this ConversationEventTopicMessage.
        Address and name data for a call endpoint.

        :return: The to_address of this ConversationEventTopicMessage.
        :rtype: ConversationEventTopicAddress
        """
        return self._to_address

    @to_address.setter
    def to_address(self, to_address):
        """
        Sets the to_address of this ConversationEventTopicMessage.
        Address and name data for a call endpoint.

        :param to_address: The to_address of this ConversationEventTopicMessage.
        :type: ConversationEventTopicAddress
        """
        

        self._to_address = to_address

    @property
    def from_address(self):
        """
        Gets the from_address of this ConversationEventTopicMessage.
        Address and name data for a call endpoint.

        :return: The from_address of this ConversationEventTopicMessage.
        :rtype: ConversationEventTopicAddress
        """
        return self._from_address

    @from_address.setter
    def from_address(self, from_address):
        """
        Sets the from_address of this ConversationEventTopicMessage.
        Address and name data for a call endpoint.

        :param from_address: The from_address of this ConversationEventTopicMessage.
        :type: ConversationEventTopicAddress
        """
        

        self._from_address = from_address

    @property
    def messages(self):
        """
        Gets the messages of this ConversationEventTopicMessage.
        The messages sent on this communication channel.

        :return: The messages of this ConversationEventTopicMessage.
        :rtype: list[ConversationEventTopicMessageDetails]
        """
        return self._messages

    @messages.setter
    def messages(self, messages):
        """
        Sets the messages of this ConversationEventTopicMessage.
        The messages sent on this communication channel.

        :param messages: The messages of this ConversationEventTopicMessage.
        :type: list[ConversationEventTopicMessageDetails]
        """
        

        self._messages = messages

    @property
    def messages_transcript_uri(self):
        """
        Gets the messages_transcript_uri of this ConversationEventTopicMessage.
        the messages transcript file uri.

        :return: The messages_transcript_uri of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._messages_transcript_uri

    @messages_transcript_uri.setter
    def messages_transcript_uri(self, messages_transcript_uri):
        """
        Sets the messages_transcript_uri of this ConversationEventTopicMessage.
        the messages transcript file uri.

        :param messages_transcript_uri: The messages_transcript_uri of this ConversationEventTopicMessage.
        :type: str
        """
        

        self._messages_transcript_uri = messages_transcript_uri

    @property
    def type(self):
        """
        Gets the type of this ConversationEventTopicMessage.
        Indicates the type of message platform from which the message originated.

        :return: The type of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ConversationEventTopicMessage.
        Indicates the type of message platform from which the message originated.

        :param type: The type of this ConversationEventTopicMessage.
        :type: str
        """
        allowed_values = ["unknown", "sms", "twitter", "facebook", "line", "viber", "wechat", "whatsapp", "telegram", "kakao", "webmessaging", "open", "instagram"]
        if type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for type -> " + type)
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def recipient_country(self):
        """
        Gets the recipient_country of this ConversationEventTopicMessage.
        Indicates the country where the recipient is associated in ISO 3166-1 alpha-2 format.

        :return: The recipient_country of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._recipient_country

    @recipient_country.setter
    def recipient_country(self, recipient_country):
        """
        Sets the recipient_country of this ConversationEventTopicMessage.
        Indicates the country where the recipient is associated in ISO 3166-1 alpha-2 format.

        :param recipient_country: The recipient_country of this ConversationEventTopicMessage.
        :type: str
        """
        

        self._recipient_country = recipient_country

    @property
    def recipient_type(self):
        """
        Gets the recipient_type of this ConversationEventTopicMessage.
        The type of the recipient. Eg: Provisioned phoneNumber is the recipient for sms message type.

        :return: The recipient_type of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._recipient_type

    @recipient_type.setter
    def recipient_type(self, recipient_type):
        """
        Sets the recipient_type of this ConversationEventTopicMessage.
        The type of the recipient. Eg: Provisioned phoneNumber is the recipient for sms message type.

        :param recipient_type: The recipient_type of this ConversationEventTopicMessage.
        :type: str
        """
        

        self._recipient_type = recipient_type

    @property
    def journey_context(self):
        """
        Gets the journey_context of this ConversationEventTopicMessage.
        A subset of the Journey System's data relevant to a part of a conversation (for external linkage and internal usage/context).

        :return: The journey_context of this ConversationEventTopicMessage.
        :rtype: ConversationEventTopicJourneyContext
        """
        return self._journey_context

    @journey_context.setter
    def journey_context(self, journey_context):
        """
        Sets the journey_context of this ConversationEventTopicMessage.
        A subset of the Journey System's data relevant to a part of a conversation (for external linkage and internal usage/context).

        :param journey_context: The journey_context of this ConversationEventTopicMessage.
        :type: ConversationEventTopicJourneyContext
        """
        

        self._journey_context = journey_context

    @property
    def wrapup(self):
        """
        Gets the wrapup of this ConversationEventTopicMessage.
        Call wrap up or disposition data.

        :return: The wrapup of this ConversationEventTopicMessage.
        :rtype: ConversationEventTopicWrapup
        """
        return self._wrapup

    @wrapup.setter
    def wrapup(self, wrapup):
        """
        Sets the wrapup of this ConversationEventTopicMessage.
        Call wrap up or disposition data.

        :param wrapup: The wrapup of this ConversationEventTopicMessage.
        :type: ConversationEventTopicWrapup
        """
        

        self._wrapup = wrapup

    @property
    def after_call_work(self):
        """
        Gets the after_call_work of this ConversationEventTopicMessage.
        A communication's after-call work data.

        :return: The after_call_work of this ConversationEventTopicMessage.
        :rtype: ConversationEventTopicAfterCallWork
        """
        return self._after_call_work

    @after_call_work.setter
    def after_call_work(self, after_call_work):
        """
        Sets the after_call_work of this ConversationEventTopicMessage.
        A communication's after-call work data.

        :param after_call_work: The after_call_work of this ConversationEventTopicMessage.
        :type: ConversationEventTopicAfterCallWork
        """
        

        self._after_call_work = after_call_work

    @property
    def after_call_work_required(self):
        """
        Gets the after_call_work_required of this ConversationEventTopicMessage.
        Indicates if after-call is required for a communication. Only used when the ACW Setting is Agent Requested.

        :return: The after_call_work_required of this ConversationEventTopicMessage.
        :rtype: bool
        """
        return self._after_call_work_required

    @after_call_work_required.setter
    def after_call_work_required(self, after_call_work_required):
        """
        Sets the after_call_work_required of this ConversationEventTopicMessage.
        Indicates if after-call is required for a communication. Only used when the ACW Setting is Agent Requested.

        :param after_call_work_required: The after_call_work_required of this ConversationEventTopicMessage.
        :type: bool
        """
        

        self._after_call_work_required = after_call_work_required

    @property
    def agent_assistant_id(self):
        """
        Gets the agent_assistant_id of this ConversationEventTopicMessage.
        UUID of virtual agent assistant that provide suggestions to the agent participant during the conversation.

        :return: The agent_assistant_id of this ConversationEventTopicMessage.
        :rtype: str
        """
        return self._agent_assistant_id

    @agent_assistant_id.setter
    def agent_assistant_id(self, agent_assistant_id):
        """
        Sets the agent_assistant_id of this ConversationEventTopicMessage.
        UUID of virtual agent assistant that provide suggestions to the agent participant during the conversation.

        :param agent_assistant_id: The agent_assistant_id of this ConversationEventTopicMessage.
        :type: str
        """
        

        self._agent_assistant_id = agent_assistant_id

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

