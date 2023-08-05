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

class V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'media_type': 'str',
            'url': 'str',
            'mime': 'str',
            'text': 'str',
            'sha256': 'str',
            'filename': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'media_type': 'mediaType',
            'url': 'url',
            'mime': 'mime',
            'text': 'text',
            'sha256': 'sha256',
            'filename': 'filename'
        }

        self._id = None
        self._media_type = None
        self._url = None
        self._mime = None
        self._text = None
        self._sha256 = None
        self._filename = None

    @property
    def id(self):
        """
        Gets the id of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :return: The id of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :param id: The id of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :type: str
        """
        

        self._id = id

    @property
    def media_type(self):
        """
        Gets the media_type of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :return: The media_type of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :rtype: str
        """
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        """
        Sets the media_type of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :param media_type: The media_type of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :type: str
        """
        allowed_values = ["Image", "Video", "Audio", "File", "Link"]
        if media_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for media_type -> " + media_type)
            self._media_type = "outdated_sdk_version"
        else:
            self._media_type = media_type

    @property
    def url(self):
        """
        Gets the url of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :return: The url of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the url of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :param url: The url of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :type: str
        """
        

        self._url = url

    @property
    def mime(self):
        """
        Gets the mime of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :return: The mime of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :rtype: str
        """
        return self._mime

    @mime.setter
    def mime(self, mime):
        """
        Sets the mime of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :param mime: The mime of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :type: str
        """
        

        self._mime = mime

    @property
    def text(self):
        """
        Gets the text of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :return: The text of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Sets the text of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :param text: The text of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :type: str
        """
        

        self._text = text

    @property
    def sha256(self):
        """
        Gets the sha256 of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :return: The sha256 of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :rtype: str
        """
        return self._sha256

    @sha256.setter
    def sha256(self, sha256):
        """
        Sets the sha256 of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :param sha256: The sha256 of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :type: str
        """
        

        self._sha256 = sha256

    @property
    def filename(self):
        """
        Gets the filename of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :return: The filename of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """
        Sets the filename of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.


        :param filename: The filename of this V2ConversationMessageTypingEventForWorkflowTopicConversationContentAttachment.
        :type: str
        """
        

        self._filename = filename

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

