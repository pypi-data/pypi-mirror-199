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

class Email(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Email - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'state': 'str',
            'initial_state': 'str',
            'id': 'str',
            'held': 'bool',
            'subject': 'str',
            'messages_sent': 'int',
            'segments': 'list[Segment]',
            'direction': 'str',
            'recording_id': 'str',
            'error_info': 'ErrorBody',
            'disconnect_type': 'str',
            'start_hold_time': 'datetime',
            'start_alerting_time': 'datetime',
            'connected_time': 'datetime',
            'disconnected_time': 'datetime',
            'auto_generated': 'bool',
            'provider': 'str',
            'script_id': 'str',
            'peer_id': 'str',
            'message_id': 'str',
            'draft_attachments': 'list[Attachment]',
            'spam': 'bool',
            'wrapup': 'Wrapup',
            'after_call_work': 'AfterCallWork',
            'after_call_work_required': 'bool'
        }

        self.attribute_map = {
            'state': 'state',
            'initial_state': 'initialState',
            'id': 'id',
            'held': 'held',
            'subject': 'subject',
            'messages_sent': 'messagesSent',
            'segments': 'segments',
            'direction': 'direction',
            'recording_id': 'recordingId',
            'error_info': 'errorInfo',
            'disconnect_type': 'disconnectType',
            'start_hold_time': 'startHoldTime',
            'start_alerting_time': 'startAlertingTime',
            'connected_time': 'connectedTime',
            'disconnected_time': 'disconnectedTime',
            'auto_generated': 'autoGenerated',
            'provider': 'provider',
            'script_id': 'scriptId',
            'peer_id': 'peerId',
            'message_id': 'messageId',
            'draft_attachments': 'draftAttachments',
            'spam': 'spam',
            'wrapup': 'wrapup',
            'after_call_work': 'afterCallWork',
            'after_call_work_required': 'afterCallWorkRequired'
        }

        self._state = None
        self._initial_state = None
        self._id = None
        self._held = None
        self._subject = None
        self._messages_sent = None
        self._segments = None
        self._direction = None
        self._recording_id = None
        self._error_info = None
        self._disconnect_type = None
        self._start_hold_time = None
        self._start_alerting_time = None
        self._connected_time = None
        self._disconnected_time = None
        self._auto_generated = None
        self._provider = None
        self._script_id = None
        self._peer_id = None
        self._message_id = None
        self._draft_attachments = None
        self._spam = None
        self._wrapup = None
        self._after_call_work = None
        self._after_call_work_required = None

    @property
    def state(self):
        """
        Gets the state of this Email.
        The connection state of this communication.

        :return: The state of this Email.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this Email.
        The connection state of this communication.

        :param state: The state of this Email.
        :type: str
        """
        allowed_values = ["alerting", "connected", "disconnected", "none", "transmitting"]
        if state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for state -> " + state)
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def initial_state(self):
        """
        Gets the initial_state of this Email.
        The initial connection state of this communication.

        :return: The initial_state of this Email.
        :rtype: str
        """
        return self._initial_state

    @initial_state.setter
    def initial_state(self, initial_state):
        """
        Sets the initial_state of this Email.
        The initial connection state of this communication.

        :param initial_state: The initial_state of this Email.
        :type: str
        """
        allowed_values = ["alerting", "connected", "disconnected", "none", "transmitting"]
        if initial_state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for initial_state -> " + initial_state)
            self._initial_state = "outdated_sdk_version"
        else:
            self._initial_state = initial_state

    @property
    def id(self):
        """
        Gets the id of this Email.
        A globally unique identifier for this communication.

        :return: The id of this Email.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Email.
        A globally unique identifier for this communication.

        :param id: The id of this Email.
        :type: str
        """
        

        self._id = id

    @property
    def held(self):
        """
        Gets the held of this Email.
        True if this call is held and the person on this side hears silence.

        :return: The held of this Email.
        :rtype: bool
        """
        return self._held

    @held.setter
    def held(self, held):
        """
        Sets the held of this Email.
        True if this call is held and the person on this side hears silence.

        :param held: The held of this Email.
        :type: bool
        """
        

        self._held = held

    @property
    def subject(self):
        """
        Gets the subject of this Email.
        The subject for the initial email that started this conversation.

        :return: The subject of this Email.
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """
        Sets the subject of this Email.
        The subject for the initial email that started this conversation.

        :param subject: The subject of this Email.
        :type: str
        """
        

        self._subject = subject

    @property
    def messages_sent(self):
        """
        Gets the messages_sent of this Email.
        The number of email messages sent by this participant.

        :return: The messages_sent of this Email.
        :rtype: int
        """
        return self._messages_sent

    @messages_sent.setter
    def messages_sent(self, messages_sent):
        """
        Sets the messages_sent of this Email.
        The number of email messages sent by this participant.

        :param messages_sent: The messages_sent of this Email.
        :type: int
        """
        

        self._messages_sent = messages_sent

    @property
    def segments(self):
        """
        Gets the segments of this Email.
        The time line of the participant's email, divided into activity segments.

        :return: The segments of this Email.
        :rtype: list[Segment]
        """
        return self._segments

    @segments.setter
    def segments(self, segments):
        """
        Sets the segments of this Email.
        The time line of the participant's email, divided into activity segments.

        :param segments: The segments of this Email.
        :type: list[Segment]
        """
        

        self._segments = segments

    @property
    def direction(self):
        """
        Gets the direction of this Email.
        The direction of the email

        :return: The direction of this Email.
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """
        Sets the direction of this Email.
        The direction of the email

        :param direction: The direction of this Email.
        :type: str
        """
        allowed_values = ["inbound", "outbound"]
        if direction.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for direction -> " + direction)
            self._direction = "outdated_sdk_version"
        else:
            self._direction = direction

    @property
    def recording_id(self):
        """
        Gets the recording_id of this Email.
        A globally unique identifier for the recording associated with this call.

        :return: The recording_id of this Email.
        :rtype: str
        """
        return self._recording_id

    @recording_id.setter
    def recording_id(self, recording_id):
        """
        Sets the recording_id of this Email.
        A globally unique identifier for the recording associated with this call.

        :param recording_id: The recording_id of this Email.
        :type: str
        """
        

        self._recording_id = recording_id

    @property
    def error_info(self):
        """
        Gets the error_info of this Email.


        :return: The error_info of this Email.
        :rtype: ErrorBody
        """
        return self._error_info

    @error_info.setter
    def error_info(self, error_info):
        """
        Sets the error_info of this Email.


        :param error_info: The error_info of this Email.
        :type: ErrorBody
        """
        

        self._error_info = error_info

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this Email.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :return: The disconnect_type of this Email.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this Email.
        System defined string indicating what caused the communication to disconnect. Will be null until the communication disconnects.

        :param disconnect_type: The disconnect_type of this Email.
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
        Gets the start_hold_time of this Email.
        The timestamp the email was placed on hold in the cloud clock if the email is currently on hold. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The start_hold_time of this Email.
        :rtype: datetime
        """
        return self._start_hold_time

    @start_hold_time.setter
    def start_hold_time(self, start_hold_time):
        """
        Sets the start_hold_time of this Email.
        The timestamp the email was placed on hold in the cloud clock if the email is currently on hold. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param start_hold_time: The start_hold_time of this Email.
        :type: datetime
        """
        

        self._start_hold_time = start_hold_time

    @property
    def start_alerting_time(self):
        """
        Gets the start_alerting_time of this Email.
        The timestamp the communication has when it is first put into an alerting state. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The start_alerting_time of this Email.
        :rtype: datetime
        """
        return self._start_alerting_time

    @start_alerting_time.setter
    def start_alerting_time(self, start_alerting_time):
        """
        Sets the start_alerting_time of this Email.
        The timestamp the communication has when it is first put into an alerting state. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param start_alerting_time: The start_alerting_time of this Email.
        :type: datetime
        """
        

        self._start_alerting_time = start_alerting_time

    @property
    def connected_time(self):
        """
        Gets the connected_time of this Email.
        The timestamp when this communication was connected in the cloud clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The connected_time of this Email.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this Email.
        The timestamp when this communication was connected in the cloud clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param connected_time: The connected_time of this Email.
        :type: datetime
        """
        

        self._connected_time = connected_time

    @property
    def disconnected_time(self):
        """
        Gets the disconnected_time of this Email.
        The timestamp when this communication disconnected from the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The disconnected_time of this Email.
        :rtype: datetime
        """
        return self._disconnected_time

    @disconnected_time.setter
    def disconnected_time(self, disconnected_time):
        """
        Sets the disconnected_time of this Email.
        The timestamp when this communication disconnected from the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param disconnected_time: The disconnected_time of this Email.
        :type: datetime
        """
        

        self._disconnected_time = disconnected_time

    @property
    def auto_generated(self):
        """
        Gets the auto_generated of this Email.
        Indicates that the email was auto-generated like an Out of Office reply.

        :return: The auto_generated of this Email.
        :rtype: bool
        """
        return self._auto_generated

    @auto_generated.setter
    def auto_generated(self, auto_generated):
        """
        Sets the auto_generated of this Email.
        Indicates that the email was auto-generated like an Out of Office reply.

        :param auto_generated: The auto_generated of this Email.
        :type: bool
        """
        

        self._auto_generated = auto_generated

    @property
    def provider(self):
        """
        Gets the provider of this Email.
        The source provider for the email.

        :return: The provider of this Email.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this Email.
        The source provider for the email.

        :param provider: The provider of this Email.
        :type: str
        """
        

        self._provider = provider

    @property
    def script_id(self):
        """
        Gets the script_id of this Email.
        The UUID of the script to use.

        :return: The script_id of this Email.
        :rtype: str
        """
        return self._script_id

    @script_id.setter
    def script_id(self, script_id):
        """
        Sets the script_id of this Email.
        The UUID of the script to use.

        :param script_id: The script_id of this Email.
        :type: str
        """
        

        self._script_id = script_id

    @property
    def peer_id(self):
        """
        Gets the peer_id of this Email.
        The id of the peer communication corresponding to a matching leg for this communication.

        :return: The peer_id of this Email.
        :rtype: str
        """
        return self._peer_id

    @peer_id.setter
    def peer_id(self, peer_id):
        """
        Sets the peer_id of this Email.
        The id of the peer communication corresponding to a matching leg for this communication.

        :param peer_id: The peer_id of this Email.
        :type: str
        """
        

        self._peer_id = peer_id

    @property
    def message_id(self):
        """
        Gets the message_id of this Email.
        A globally unique identifier for the stored content of this communication.

        :return: The message_id of this Email.
        :rtype: str
        """
        return self._message_id

    @message_id.setter
    def message_id(self, message_id):
        """
        Sets the message_id of this Email.
        A globally unique identifier for the stored content of this communication.

        :param message_id: The message_id of this Email.
        :type: str
        """
        

        self._message_id = message_id

    @property
    def draft_attachments(self):
        """
        Gets the draft_attachments of this Email.
        A list of uploaded attachments on the email draft.

        :return: The draft_attachments of this Email.
        :rtype: list[Attachment]
        """
        return self._draft_attachments

    @draft_attachments.setter
    def draft_attachments(self, draft_attachments):
        """
        Sets the draft_attachments of this Email.
        A list of uploaded attachments on the email draft.

        :param draft_attachments: The draft_attachments of this Email.
        :type: list[Attachment]
        """
        

        self._draft_attachments = draft_attachments

    @property
    def spam(self):
        """
        Gets the spam of this Email.
        Indicates if the inbound email was marked as spam.

        :return: The spam of this Email.
        :rtype: bool
        """
        return self._spam

    @spam.setter
    def spam(self, spam):
        """
        Sets the spam of this Email.
        Indicates if the inbound email was marked as spam.

        :param spam: The spam of this Email.
        :type: bool
        """
        

        self._spam = spam

    @property
    def wrapup(self):
        """
        Gets the wrapup of this Email.
        Call wrap up or disposition data.

        :return: The wrapup of this Email.
        :rtype: Wrapup
        """
        return self._wrapup

    @wrapup.setter
    def wrapup(self, wrapup):
        """
        Sets the wrapup of this Email.
        Call wrap up or disposition data.

        :param wrapup: The wrapup of this Email.
        :type: Wrapup
        """
        

        self._wrapup = wrapup

    @property
    def after_call_work(self):
        """
        Gets the after_call_work of this Email.
        After-call work for the communication.

        :return: The after_call_work of this Email.
        :rtype: AfterCallWork
        """
        return self._after_call_work

    @after_call_work.setter
    def after_call_work(self, after_call_work):
        """
        Sets the after_call_work of this Email.
        After-call work for the communication.

        :param after_call_work: The after_call_work of this Email.
        :type: AfterCallWork
        """
        

        self._after_call_work = after_call_work

    @property
    def after_call_work_required(self):
        """
        Gets the after_call_work_required of this Email.
        Indicates if after-call work is required for a communication. Only used when the ACW Setting is Agent Requested.

        :return: The after_call_work_required of this Email.
        :rtype: bool
        """
        return self._after_call_work_required

    @after_call_work_required.setter
    def after_call_work_required(self, after_call_work_required):
        """
        Sets the after_call_work_required of this Email.
        Indicates if after-call work is required for a communication. Only used when the ACW Setting is Agent Requested.

        :param after_call_work_required: The after_call_work_required of this Email.
        :type: bool
        """
        

        self._after_call_work_required = after_call_work_required

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

