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

class PatchCtaButtonStyleProperties(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        PatchCtaButtonStyleProperties - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'color': 'str',
            'font': 'str',
            'font_size': 'str',
            'text_align': 'str',
            'background_color': 'str'
        }

        self.attribute_map = {
            'color': 'color',
            'font': 'font',
            'font_size': 'fontSize',
            'text_align': 'textAlign',
            'background_color': 'backgroundColor'
        }

        self._color = None
        self._font = None
        self._font_size = None
        self._text_align = None
        self._background_color = None

    @property
    def color(self):
        """
        Gets the color of this PatchCtaButtonStyleProperties.
        Color of the text. (eg. #FFFFFF)

        :return: The color of this PatchCtaButtonStyleProperties.
        :rtype: str
        """
        return self._color

    @color.setter
    def color(self, color):
        """
        Sets the color of this PatchCtaButtonStyleProperties.
        Color of the text. (eg. #FFFFFF)

        :param color: The color of this PatchCtaButtonStyleProperties.
        :type: str
        """
        

        self._color = color

    @property
    def font(self):
        """
        Gets the font of this PatchCtaButtonStyleProperties.
        Font of the text. (eg. Helvetica)

        :return: The font of this PatchCtaButtonStyleProperties.
        :rtype: str
        """
        return self._font

    @font.setter
    def font(self, font):
        """
        Sets the font of this PatchCtaButtonStyleProperties.
        Font of the text. (eg. Helvetica)

        :param font: The font of this PatchCtaButtonStyleProperties.
        :type: str
        """
        

        self._font = font

    @property
    def font_size(self):
        """
        Gets the font_size of this PatchCtaButtonStyleProperties.
        Font size of the text. (eg. '12')

        :return: The font_size of this PatchCtaButtonStyleProperties.
        :rtype: str
        """
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        """
        Sets the font_size of this PatchCtaButtonStyleProperties.
        Font size of the text. (eg. '12')

        :param font_size: The font_size of this PatchCtaButtonStyleProperties.
        :type: str
        """
        

        self._font_size = font_size

    @property
    def text_align(self):
        """
        Gets the text_align of this PatchCtaButtonStyleProperties.
        Text alignment.

        :return: The text_align of this PatchCtaButtonStyleProperties.
        :rtype: str
        """
        return self._text_align

    @text_align.setter
    def text_align(self, text_align):
        """
        Sets the text_align of this PatchCtaButtonStyleProperties.
        Text alignment.

        :param text_align: The text_align of this PatchCtaButtonStyleProperties.
        :type: str
        """
        allowed_values = ["Left", "Right", "Center"]
        if text_align.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for text_align -> " + text_align)
            self._text_align = "outdated_sdk_version"
        else:
            self._text_align = text_align

    @property
    def background_color(self):
        """
        Gets the background_color of this PatchCtaButtonStyleProperties.
        Background color of the CTA button. (eg. #A04033)

        :return: The background_color of this PatchCtaButtonStyleProperties.
        :rtype: str
        """
        return self._background_color

    @background_color.setter
    def background_color(self, background_color):
        """
        Sets the background_color of this PatchCtaButtonStyleProperties.
        Background color of the CTA button. (eg. #A04033)

        :param background_color: The background_color of this PatchCtaButtonStyleProperties.
        :type: str
        """
        

        self._background_color = background_color

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

