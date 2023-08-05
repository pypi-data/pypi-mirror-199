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

class TestMessage(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        TestMessage - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'to': 'list[EmailAddress]',
            'pcFrom': 'EmailAddress',
            'subject': 'str',
            'text_body': 'str',
            'html_body': 'str',
            'time': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'to': 'to',
            'pcFrom': 'from',
            'subject': 'subject',
            'text_body': 'textBody',
            'html_body': 'htmlBody',
            'time': 'time'
        }

        self._id = None
        self._to = None
        self._pcFrom = None
        self._subject = None
        self._text_body = None
        self._html_body = None
        self._time = None

    @property
    def id(self):
        """
        Gets the id of this TestMessage.
        After the message has been sent, this is the value of the Message-ID email header.

        :return: The id of this TestMessage.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this TestMessage.
        After the message has been sent, this is the value of the Message-ID email header.

        :param id: The id of this TestMessage.
        :type: str
        """
        

        self._id = id

    @property
    def to(self):
        """
        Gets the to of this TestMessage.
        The recipients of the email message.

        :return: The to of this TestMessage.
        :rtype: list[EmailAddress]
        """
        return self._to

    @to.setter
    def to(self, to):
        """
        Sets the to of this TestMessage.
        The recipients of the email message.

        :param to: The to of this TestMessage.
        :type: list[EmailAddress]
        """
        

        self._to = to

    @property
    def pcFrom(self):
        """
        Gets the pcFrom of this TestMessage.
        The sender of the email message.

        :return: The pcFrom of this TestMessage.
        :rtype: EmailAddress
        """
        return self._pcFrom

    @pcFrom.setter
    def pcFrom(self, pcFrom):
        """
        Sets the pcFrom of this TestMessage.
        The sender of the email message.

        :param pcFrom: The pcFrom of this TestMessage.
        :type: EmailAddress
        """
        

        self._pcFrom = pcFrom

    @property
    def subject(self):
        """
        Gets the subject of this TestMessage.
        The subject of the email message.

        :return: The subject of this TestMessage.
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """
        Sets the subject of this TestMessage.
        The subject of the email message.

        :param subject: The subject of this TestMessage.
        :type: str
        """
        

        self._subject = subject

    @property
    def text_body(self):
        """
        Gets the text_body of this TestMessage.
        The text body of the email message.

        :return: The text_body of this TestMessage.
        :rtype: str
        """
        return self._text_body

    @text_body.setter
    def text_body(self, text_body):
        """
        Sets the text_body of this TestMessage.
        The text body of the email message.

        :param text_body: The text_body of this TestMessage.
        :type: str
        """
        

        self._text_body = text_body

    @property
    def html_body(self):
        """
        Gets the html_body of this TestMessage.
        The html body of the email message

        :return: The html_body of this TestMessage.
        :rtype: str
        """
        return self._html_body

    @html_body.setter
    def html_body(self, html_body):
        """
        Sets the html_body of this TestMessage.
        The html body of the email message

        :param html_body: The html_body of this TestMessage.
        :type: str
        """
        

        self._html_body = html_body

    @property
    def time(self):
        """
        Gets the time of this TestMessage.
        The time when the message was sent. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The time of this TestMessage.
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """
        Sets the time of this TestMessage.
        The time when the message was sent. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param time: The time of this TestMessage.
        :type: datetime
        """
        

        self._time = time

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

