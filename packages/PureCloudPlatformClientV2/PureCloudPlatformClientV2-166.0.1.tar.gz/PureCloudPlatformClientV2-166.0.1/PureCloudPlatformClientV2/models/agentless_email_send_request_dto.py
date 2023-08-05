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

class AgentlessEmailSendRequestDto(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AgentlessEmailSendRequestDto - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'sender_type': 'str',
            'conversation_id': 'str',
            'from_address': 'EmailAddress',
            'to_addresses': 'list[EmailAddress]',
            'reply_to_address': 'EmailAddress',
            'subject': 'str',
            'text_body': 'str',
            'html_body': 'str'
        }

        self.attribute_map = {
            'sender_type': 'senderType',
            'conversation_id': 'conversationId',
            'from_address': 'fromAddress',
            'to_addresses': 'toAddresses',
            'reply_to_address': 'replyToAddress',
            'subject': 'subject',
            'text_body': 'textBody',
            'html_body': 'htmlBody'
        }

        self._sender_type = None
        self._conversation_id = None
        self._from_address = None
        self._to_addresses = None
        self._reply_to_address = None
        self._subject = None
        self._text_body = None
        self._html_body = None

    @property
    def sender_type(self):
        """
        Gets the sender_type of this AgentlessEmailSendRequestDto.
        The direction of the message.

        :return: The sender_type of this AgentlessEmailSendRequestDto.
        :rtype: str
        """
        return self._sender_type

    @sender_type.setter
    def sender_type(self, sender_type):
        """
        Sets the sender_type of this AgentlessEmailSendRequestDto.
        The direction of the message.

        :param sender_type: The sender_type of this AgentlessEmailSendRequestDto.
        :type: str
        """
        allowed_values = ["Outbound", "Inbound", "Integration"]
        if sender_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for sender_type -> " + sender_type)
            self._sender_type = "outdated_sdk_version"
        else:
            self._sender_type = sender_type

    @property
    def conversation_id(self):
        """
        Gets the conversation_id of this AgentlessEmailSendRequestDto.
        The identifier of the conversation.

        :return: The conversation_id of this AgentlessEmailSendRequestDto.
        :rtype: str
        """
        return self._conversation_id

    @conversation_id.setter
    def conversation_id(self, conversation_id):
        """
        Sets the conversation_id of this AgentlessEmailSendRequestDto.
        The identifier of the conversation.

        :param conversation_id: The conversation_id of this AgentlessEmailSendRequestDto.
        :type: str
        """
        

        self._conversation_id = conversation_id

    @property
    def from_address(self):
        """
        Gets the from_address of this AgentlessEmailSendRequestDto.
        The sender of the message.

        :return: The from_address of this AgentlessEmailSendRequestDto.
        :rtype: EmailAddress
        """
        return self._from_address

    @from_address.setter
    def from_address(self, from_address):
        """
        Sets the from_address of this AgentlessEmailSendRequestDto.
        The sender of the message.

        :param from_address: The from_address of this AgentlessEmailSendRequestDto.
        :type: EmailAddress
        """
        

        self._from_address = from_address

    @property
    def to_addresses(self):
        """
        Gets the to_addresses of this AgentlessEmailSendRequestDto.
        The recipient(s) of the message.

        :return: The to_addresses of this AgentlessEmailSendRequestDto.
        :rtype: list[EmailAddress]
        """
        return self._to_addresses

    @to_addresses.setter
    def to_addresses(self, to_addresses):
        """
        Sets the to_addresses of this AgentlessEmailSendRequestDto.
        The recipient(s) of the message.

        :param to_addresses: The to_addresses of this AgentlessEmailSendRequestDto.
        :type: list[EmailAddress]
        """
        

        self._to_addresses = to_addresses

    @property
    def reply_to_address(self):
        """
        Gets the reply_to_address of this AgentlessEmailSendRequestDto.
        The address to use for reply.

        :return: The reply_to_address of this AgentlessEmailSendRequestDto.
        :rtype: EmailAddress
        """
        return self._reply_to_address

    @reply_to_address.setter
    def reply_to_address(self, reply_to_address):
        """
        Sets the reply_to_address of this AgentlessEmailSendRequestDto.
        The address to use for reply.

        :param reply_to_address: The reply_to_address of this AgentlessEmailSendRequestDto.
        :type: EmailAddress
        """
        

        self._reply_to_address = reply_to_address

    @property
    def subject(self):
        """
        Gets the subject of this AgentlessEmailSendRequestDto.
        The subject of the message.

        :return: The subject of this AgentlessEmailSendRequestDto.
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """
        Sets the subject of this AgentlessEmailSendRequestDto.
        The subject of the message.

        :param subject: The subject of this AgentlessEmailSendRequestDto.
        :type: str
        """
        

        self._subject = subject

    @property
    def text_body(self):
        """
        Gets the text_body of this AgentlessEmailSendRequestDto.
        The Content of the message, in plain text.

        :return: The text_body of this AgentlessEmailSendRequestDto.
        :rtype: str
        """
        return self._text_body

    @text_body.setter
    def text_body(self, text_body):
        """
        Sets the text_body of this AgentlessEmailSendRequestDto.
        The Content of the message, in plain text.

        :param text_body: The text_body of this AgentlessEmailSendRequestDto.
        :type: str
        """
        

        self._text_body = text_body

    @property
    def html_body(self):
        """
        Gets the html_body of this AgentlessEmailSendRequestDto.
        The Content of the message, in HTML. Links, images and styles are allowed

        :return: The html_body of this AgentlessEmailSendRequestDto.
        :rtype: str
        """
        return self._html_body

    @html_body.setter
    def html_body(self, html_body):
        """
        Sets the html_body of this AgentlessEmailSendRequestDto.
        The Content of the message, in HTML. Links, images and styles are allowed

        :param html_body: The html_body of this AgentlessEmailSendRequestDto.
        :type: str
        """
        

        self._html_body = html_body

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

