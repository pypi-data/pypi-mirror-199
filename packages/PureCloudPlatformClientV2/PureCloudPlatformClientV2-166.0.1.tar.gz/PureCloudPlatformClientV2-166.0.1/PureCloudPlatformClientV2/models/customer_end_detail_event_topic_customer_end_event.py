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

class CustomerEndDetailEventTopicCustomerEndEvent(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CustomerEndDetailEventTopicCustomerEndEvent - a model defined in Swagger

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
            'disconnect_type': 'str',
            'media_type': 'str',
            'external_organization_id': 'str',
            'external_contact_id': 'str',
            'provider': 'str',
            'direction': 'str',
            'ani': 'str',
            'dnis': 'str',
            'address_to': 'str',
            'address_from': 'str',
            'callback_user_name': 'str',
            'callback_numbers': 'list[str]',
            'callback_scheduled_time': 'int',
            'subject': 'str',
            'message_type': 'str',
            'interacting_duration_ms': 'int'
        }

        self.attribute_map = {
            'event_time': 'eventTime',
            'conversation_id': 'conversationId',
            'participant_id': 'participantId',
            'session_id': 'sessionId',
            'disconnect_type': 'disconnectType',
            'media_type': 'mediaType',
            'external_organization_id': 'externalOrganizationId',
            'external_contact_id': 'externalContactId',
            'provider': 'provider',
            'direction': 'direction',
            'ani': 'ani',
            'dnis': 'dnis',
            'address_to': 'addressTo',
            'address_from': 'addressFrom',
            'callback_user_name': 'callbackUserName',
            'callback_numbers': 'callbackNumbers',
            'callback_scheduled_time': 'callbackScheduledTime',
            'subject': 'subject',
            'message_type': 'messageType',
            'interacting_duration_ms': 'interactingDurationMs'
        }

        self._event_time = None
        self._conversation_id = None
        self._participant_id = None
        self._session_id = None
        self._disconnect_type = None
        self._media_type = None
        self._external_organization_id = None
        self._external_contact_id = None
        self._provider = None
        self._direction = None
        self._ani = None
        self._dnis = None
        self._address_to = None
        self._address_from = None
        self._callback_user_name = None
        self._callback_numbers = None
        self._callback_scheduled_time = None
        self._subject = None
        self._message_type = None
        self._interacting_duration_ms = None

    @property
    def event_time(self):
        """
        Gets the event_time of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The event_time of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: int
        """
        return self._event_time

    @event_time.setter
    def event_time(self, event_time):
        """
        Sets the event_time of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param event_time: The event_time of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: int
        """
        

        self._event_time = event_time

    @property
    def conversation_id(self):
        """
        Gets the conversation_id of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The conversation_id of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._conversation_id

    @conversation_id.setter
    def conversation_id(self, conversation_id):
        """
        Sets the conversation_id of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param conversation_id: The conversation_id of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._conversation_id = conversation_id

    @property
    def participant_id(self):
        """
        Gets the participant_id of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The participant_id of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._participant_id

    @participant_id.setter
    def participant_id(self, participant_id):
        """
        Sets the participant_id of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param participant_id: The participant_id of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._participant_id = participant_id

    @property
    def session_id(self):
        """
        Gets the session_id of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The session_id of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """
        Sets the session_id of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param session_id: The session_id of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._session_id = session_id

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The disconnect_type of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param disconnect_type: The disconnect_type of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        allowed_values = ["UNKNOWN", "ENDPOINT", "CLIENT", "SYSTEM", "TRANSFER", "ERROR", "PEER", "OTHER", "SPAM", "TIMEOUT", "TRANSPORT_FAILURE", "CONFERENCE_TRANSFER", "CONSULT_TRANSFER", "FORWARD_TRANSFER", "NO_ANSWER_TRANSFER", "NOT_AVAILABLE_TRANSFER", "UNCALLABLE"]
        if disconnect_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for disconnect_type -> " + disconnect_type)
            self._disconnect_type = "outdated_sdk_version"
        else:
            self._disconnect_type = disconnect_type

    @property
    def media_type(self):
        """
        Gets the media_type of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The media_type of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        """
        Sets the media_type of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param media_type: The media_type of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        allowed_values = ["UNKNOWN", "VOICE", "CHAT", "EMAIL", "CALLBACK", "COBROWSE", "VIDEO", "SCREENSHARE", "MESSAGE"]
        if media_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for media_type -> " + media_type)
            self._media_type = "outdated_sdk_version"
        else:
            self._media_type = media_type

    @property
    def external_organization_id(self):
        """
        Gets the external_organization_id of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The external_organization_id of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._external_organization_id

    @external_organization_id.setter
    def external_organization_id(self, external_organization_id):
        """
        Sets the external_organization_id of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param external_organization_id: The external_organization_id of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._external_organization_id = external_organization_id

    @property
    def external_contact_id(self):
        """
        Gets the external_contact_id of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The external_contact_id of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._external_contact_id

    @external_contact_id.setter
    def external_contact_id(self, external_contact_id):
        """
        Sets the external_contact_id of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param external_contact_id: The external_contact_id of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._external_contact_id = external_contact_id

    @property
    def provider(self):
        """
        Gets the provider of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The provider of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param provider: The provider of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._provider = provider

    @property
    def direction(self):
        """
        Gets the direction of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The direction of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """
        Sets the direction of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param direction: The direction of this CustomerEndDetailEventTopicCustomerEndEvent.
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
        Gets the ani of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The ani of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._ani

    @ani.setter
    def ani(self, ani):
        """
        Sets the ani of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param ani: The ani of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._ani = ani

    @property
    def dnis(self):
        """
        Gets the dnis of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The dnis of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._dnis

    @dnis.setter
    def dnis(self, dnis):
        """
        Sets the dnis of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param dnis: The dnis of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._dnis = dnis

    @property
    def address_to(self):
        """
        Gets the address_to of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The address_to of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._address_to

    @address_to.setter
    def address_to(self, address_to):
        """
        Sets the address_to of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param address_to: The address_to of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._address_to = address_to

    @property
    def address_from(self):
        """
        Gets the address_from of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The address_from of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._address_from

    @address_from.setter
    def address_from(self, address_from):
        """
        Sets the address_from of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param address_from: The address_from of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._address_from = address_from

    @property
    def callback_user_name(self):
        """
        Gets the callback_user_name of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The callback_user_name of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._callback_user_name

    @callback_user_name.setter
    def callback_user_name(self, callback_user_name):
        """
        Sets the callback_user_name of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param callback_user_name: The callback_user_name of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._callback_user_name = callback_user_name

    @property
    def callback_numbers(self):
        """
        Gets the callback_numbers of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The callback_numbers of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: list[str]
        """
        return self._callback_numbers

    @callback_numbers.setter
    def callback_numbers(self, callback_numbers):
        """
        Sets the callback_numbers of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param callback_numbers: The callback_numbers of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: list[str]
        """
        

        self._callback_numbers = callback_numbers

    @property
    def callback_scheduled_time(self):
        """
        Gets the callback_scheduled_time of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The callback_scheduled_time of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: int
        """
        return self._callback_scheduled_time

    @callback_scheduled_time.setter
    def callback_scheduled_time(self, callback_scheduled_time):
        """
        Sets the callback_scheduled_time of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param callback_scheduled_time: The callback_scheduled_time of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: int
        """
        

        self._callback_scheduled_time = callback_scheduled_time

    @property
    def subject(self):
        """
        Gets the subject of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The subject of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """
        Sets the subject of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param subject: The subject of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        

        self._subject = subject

    @property
    def message_type(self):
        """
        Gets the message_type of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The message_type of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: str
        """
        return self._message_type

    @message_type.setter
    def message_type(self, message_type):
        """
        Sets the message_type of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param message_type: The message_type of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: str
        """
        allowed_values = ["UNKNOWN", "SMS", "TWITTER", "FACEBOOK", "LINE", "WHATSAPP", "WEBMESSAGING", "OPEN", "INSTAGRAM"]
        if message_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for message_type -> " + message_type)
            self._message_type = "outdated_sdk_version"
        else:
            self._message_type = message_type

    @property
    def interacting_duration_ms(self):
        """
        Gets the interacting_duration_ms of this CustomerEndDetailEventTopicCustomerEndEvent.


        :return: The interacting_duration_ms of this CustomerEndDetailEventTopicCustomerEndEvent.
        :rtype: int
        """
        return self._interacting_duration_ms

    @interacting_duration_ms.setter
    def interacting_duration_ms(self, interacting_duration_ms):
        """
        Sets the interacting_duration_ms of this CustomerEndDetailEventTopicCustomerEndEvent.


        :param interacting_duration_ms: The interacting_duration_ms of this CustomerEndDetailEventTopicCustomerEndEvent.
        :type: int
        """
        

        self._interacting_duration_ms = interacting_duration_ms

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

