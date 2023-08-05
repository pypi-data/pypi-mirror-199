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

class DocumentFaq(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DocumentFaq - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'question': 'str',
            'answer': 'str',
            'alternatives': 'list[str]'
        }

        self.attribute_map = {
            'question': 'question',
            'answer': 'answer',
            'alternatives': 'alternatives'
        }

        self._question = None
        self._answer = None
        self._alternatives = None

    @property
    def question(self):
        """
        Gets the question of this DocumentFaq.
        The question for this FAQ

        :return: The question of this DocumentFaq.
        :rtype: str
        """
        return self._question

    @question.setter
    def question(self, question):
        """
        Sets the question of this DocumentFaq.
        The question for this FAQ

        :param question: The question of this DocumentFaq.
        :type: str
        """
        

        self._question = question

    @property
    def answer(self):
        """
        Gets the answer of this DocumentFaq.
        The answer for this FAQ

        :return: The answer of this DocumentFaq.
        :rtype: str
        """
        return self._answer

    @answer.setter
    def answer(self, answer):
        """
        Sets the answer of this DocumentFaq.
        The answer for this FAQ

        :param answer: The answer of this DocumentFaq.
        :type: str
        """
        

        self._answer = answer

    @property
    def alternatives(self):
        """
        Gets the alternatives of this DocumentFaq.
        List of Alternative questions related to the answer which helps in improving the likelihood of a match to user query

        :return: The alternatives of this DocumentFaq.
        :rtype: list[str]
        """
        return self._alternatives

    @alternatives.setter
    def alternatives(self, alternatives):
        """
        Sets the alternatives of this DocumentFaq.
        List of Alternative questions related to the answer which helps in improving the likelihood of a match to user query

        :param alternatives: The alternatives of this DocumentFaq.
        :type: list[str]
        """
        

        self._alternatives = alternatives

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

