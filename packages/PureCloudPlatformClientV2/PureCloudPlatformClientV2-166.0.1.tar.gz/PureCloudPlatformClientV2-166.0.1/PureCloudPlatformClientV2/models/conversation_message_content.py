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

class ConversationMessageContent(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ConversationMessageContent - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'content_type': 'str',
            'location': 'ConversationContentLocation',
            'attachment': 'ConversationContentAttachment',
            'quick_reply': 'ConversationContentQuickReply',
            'button_response': 'ConversationContentButtonResponse',
            'template': 'ConversationContentNotificationTemplate',
            'story': 'ConversationContentStory',
            'card': 'ConversationContentCard',
            'carousel': 'ConversationContentCarousel',
            'text': 'ConversationContentText',
            'quick_reply_v2': 'ConversationContentQuickReplyV2'
        }

        self.attribute_map = {
            'content_type': 'contentType',
            'location': 'location',
            'attachment': 'attachment',
            'quick_reply': 'quickReply',
            'button_response': 'buttonResponse',
            'template': 'template',
            'story': 'story',
            'card': 'card',
            'carousel': 'carousel',
            'text': 'text',
            'quick_reply_v2': 'quickReplyV2'
        }

        self._content_type = None
        self._location = None
        self._attachment = None
        self._quick_reply = None
        self._button_response = None
        self._template = None
        self._story = None
        self._card = None
        self._carousel = None
        self._text = None
        self._quick_reply_v2 = None

    @property
    def content_type(self):
        """
        Gets the content_type of this ConversationMessageContent.
        Type of this content element.

        :return: The content_type of this ConversationMessageContent.
        :rtype: str
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type):
        """
        Sets the content_type of this ConversationMessageContent.
        Type of this content element.

        :param content_type: The content_type of this ConversationMessageContent.
        :type: str
        """
        allowed_values = ["Attachment", "Location", "QuickReply", "Notification", "ButtonResponse", "Story", "Mention", "Card", "Carousel", "Text", "QuickReplyV2", "Unknown"]
        if content_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for content_type -> " + content_type)
            self._content_type = "outdated_sdk_version"
        else:
            self._content_type = content_type

    @property
    def location(self):
        """
        Gets the location of this ConversationMessageContent.
        Location content.

        :return: The location of this ConversationMessageContent.
        :rtype: ConversationContentLocation
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Sets the location of this ConversationMessageContent.
        Location content.

        :param location: The location of this ConversationMessageContent.
        :type: ConversationContentLocation
        """
        

        self._location = location

    @property
    def attachment(self):
        """
        Gets the attachment of this ConversationMessageContent.
        Attachment content.

        :return: The attachment of this ConversationMessageContent.
        :rtype: ConversationContentAttachment
        """
        return self._attachment

    @attachment.setter
    def attachment(self, attachment):
        """
        Sets the attachment of this ConversationMessageContent.
        Attachment content.

        :param attachment: The attachment of this ConversationMessageContent.
        :type: ConversationContentAttachment
        """
        

        self._attachment = attachment

    @property
    def quick_reply(self):
        """
        Gets the quick_reply of this ConversationMessageContent.
        Quick reply content.

        :return: The quick_reply of this ConversationMessageContent.
        :rtype: ConversationContentQuickReply
        """
        return self._quick_reply

    @quick_reply.setter
    def quick_reply(self, quick_reply):
        """
        Sets the quick_reply of this ConversationMessageContent.
        Quick reply content.

        :param quick_reply: The quick_reply of this ConversationMessageContent.
        :type: ConversationContentQuickReply
        """
        

        self._quick_reply = quick_reply

    @property
    def button_response(self):
        """
        Gets the button_response of this ConversationMessageContent.
        Button response content.

        :return: The button_response of this ConversationMessageContent.
        :rtype: ConversationContentButtonResponse
        """
        return self._button_response

    @button_response.setter
    def button_response(self, button_response):
        """
        Sets the button_response of this ConversationMessageContent.
        Button response content.

        :param button_response: The button_response of this ConversationMessageContent.
        :type: ConversationContentButtonResponse
        """
        

        self._button_response = button_response

    @property
    def template(self):
        """
        Gets the template of this ConversationMessageContent.
        Template notification content.

        :return: The template of this ConversationMessageContent.
        :rtype: ConversationContentNotificationTemplate
        """
        return self._template

    @template.setter
    def template(self, template):
        """
        Sets the template of this ConversationMessageContent.
        Template notification content.

        :param template: The template of this ConversationMessageContent.
        :type: ConversationContentNotificationTemplate
        """
        

        self._template = template

    @property
    def story(self):
        """
        Gets the story of this ConversationMessageContent.
        Ephemeral story content.

        :return: The story of this ConversationMessageContent.
        :rtype: ConversationContentStory
        """
        return self._story

    @story.setter
    def story(self, story):
        """
        Sets the story of this ConversationMessageContent.
        Ephemeral story content.

        :param story: The story of this ConversationMessageContent.
        :type: ConversationContentStory
        """
        

        self._story = story

    @property
    def card(self):
        """
        Gets the card of this ConversationMessageContent.
        Card content

        :return: The card of this ConversationMessageContent.
        :rtype: ConversationContentCard
        """
        return self._card

    @card.setter
    def card(self, card):
        """
        Sets the card of this ConversationMessageContent.
        Card content

        :param card: The card of this ConversationMessageContent.
        :type: ConversationContentCard
        """
        

        self._card = card

    @property
    def carousel(self):
        """
        Gets the carousel of this ConversationMessageContent.
        Carousel content

        :return: The carousel of this ConversationMessageContent.
        :rtype: ConversationContentCarousel
        """
        return self._carousel

    @carousel.setter
    def carousel(self, carousel):
        """
        Sets the carousel of this ConversationMessageContent.
        Carousel content

        :param carousel: The carousel of this ConversationMessageContent.
        :type: ConversationContentCarousel
        """
        

        self._carousel = carousel

    @property
    def text(self):
        """
        Gets the text of this ConversationMessageContent.
        Text content.

        :return: The text of this ConversationMessageContent.
        :rtype: ConversationContentText
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Sets the text of this ConversationMessageContent.
        Text content.

        :param text: The text of this ConversationMessageContent.
        :type: ConversationContentText
        """
        

        self._text = text

    @property
    def quick_reply_v2(self):
        """
        Gets the quick_reply_v2 of this ConversationMessageContent.
        Quick reply V2 content.

        :return: The quick_reply_v2 of this ConversationMessageContent.
        :rtype: ConversationContentQuickReplyV2
        """
        return self._quick_reply_v2

    @quick_reply_v2.setter
    def quick_reply_v2(self, quick_reply_v2):
        """
        Sets the quick_reply_v2 of this ConversationMessageContent.
        Quick reply V2 content.

        :param quick_reply_v2: The quick_reply_v2 of this ConversationMessageContent.
        :type: ConversationContentQuickReplyV2
        """
        

        self._quick_reply_v2 = quick_reply_v2

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

