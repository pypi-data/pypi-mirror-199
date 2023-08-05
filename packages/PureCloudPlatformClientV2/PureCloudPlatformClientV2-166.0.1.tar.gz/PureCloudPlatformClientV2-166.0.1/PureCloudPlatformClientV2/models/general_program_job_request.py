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

class GeneralProgramJobRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        GeneralProgramJobRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'dialect': 'str',
            'mode': 'str'
        }

        self.attribute_map = {
            'dialect': 'dialect',
            'mode': 'mode'
        }

        self._dialect = None
        self._mode = None

    @property
    def dialect(self):
        """
        Gets the dialect of this GeneralProgramJobRequest.
        The dialect of the topics to link with the general program, dialect format is {language}-{country} where language follows ISO 639-1 standard and country follows ISO 3166-1 alpha 2 standard

        :return: The dialect of this GeneralProgramJobRequest.
        :rtype: str
        """
        return self._dialect

    @dialect.setter
    def dialect(self, dialect):
        """
        Sets the dialect of this GeneralProgramJobRequest.
        The dialect of the topics to link with the general program, dialect format is {language}-{country} where language follows ISO 639-1 standard and country follows ISO 3166-1 alpha 2 standard

        :param dialect: The dialect of this GeneralProgramJobRequest.
        :type: str
        """
        allowed_values = ["en-US", "es-US", "en-AU", "en-GB", "en-ZA", "es-ES", "en-IN", "fr-FR", "fr-CA", "it-IT", "de-DE", "pt-BR", "pl-PL", "pt-PT", "nl-NL", "ko-KR", "ja-JP"]
        if dialect.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for dialect -> " + dialect)
            self._dialect = "outdated_sdk_version"
        else:
            self._dialect = dialect

    @property
    def mode(self):
        """
        Gets the mode of this GeneralProgramJobRequest.
        The mode to use for the general program job, default value is Skip

        :return: The mode of this GeneralProgramJobRequest.
        :rtype: str
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """
        Sets the mode of this GeneralProgramJobRequest.
        The mode to use for the general program job, default value is Skip

        :param mode: The mode of this GeneralProgramJobRequest.
        :type: str
        """
        allowed_values = ["Skip", "Merge"]
        if mode.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for mode -> " + mode)
            self._mode = "outdated_sdk_version"
        else:
            self._mode = mode

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

