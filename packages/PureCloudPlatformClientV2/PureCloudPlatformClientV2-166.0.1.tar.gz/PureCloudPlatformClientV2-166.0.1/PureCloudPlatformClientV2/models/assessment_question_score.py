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

class AssessmentQuestionScore(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AssessmentQuestionScore - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'failed_kill_question': 'bool',
            'comments': 'str',
            'question_id': 'str',
            'answer_id': 'str',
            'score': 'int',
            'marked_na': 'bool',
            'free_text_answer': 'str'
        }

        self.attribute_map = {
            'failed_kill_question': 'failedKillQuestion',
            'comments': 'comments',
            'question_id': 'questionId',
            'answer_id': 'answerId',
            'score': 'score',
            'marked_na': 'markedNA',
            'free_text_answer': 'freeTextAnswer'
        }

        self._failed_kill_question = None
        self._comments = None
        self._question_id = None
        self._answer_id = None
        self._score = None
        self._marked_na = None
        self._free_text_answer = None

    @property
    def failed_kill_question(self):
        """
        Gets the failed_kill_question of this AssessmentQuestionScore.
        True if this was a failed Kill question

        :return: The failed_kill_question of this AssessmentQuestionScore.
        :rtype: bool
        """
        return self._failed_kill_question

    @failed_kill_question.setter
    def failed_kill_question(self, failed_kill_question):
        """
        Sets the failed_kill_question of this AssessmentQuestionScore.
        True if this was a failed Kill question

        :param failed_kill_question: The failed_kill_question of this AssessmentQuestionScore.
        :type: bool
        """
        

        self._failed_kill_question = failed_kill_question

    @property
    def comments(self):
        """
        Gets the comments of this AssessmentQuestionScore.
        Comments provided for the answer

        :return: The comments of this AssessmentQuestionScore.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this AssessmentQuestionScore.
        Comments provided for the answer

        :param comments: The comments of this AssessmentQuestionScore.
        :type: str
        """
        

        self._comments = comments

    @property
    def question_id(self):
        """
        Gets the question_id of this AssessmentQuestionScore.
        The ID of the question

        :return: The question_id of this AssessmentQuestionScore.
        :rtype: str
        """
        return self._question_id

    @question_id.setter
    def question_id(self, question_id):
        """
        Sets the question_id of this AssessmentQuestionScore.
        The ID of the question

        :param question_id: The question_id of this AssessmentQuestionScore.
        :type: str
        """
        

        self._question_id = question_id

    @property
    def answer_id(self):
        """
        Gets the answer_id of this AssessmentQuestionScore.
        The ID of the selected answer

        :return: The answer_id of this AssessmentQuestionScore.
        :rtype: str
        """
        return self._answer_id

    @answer_id.setter
    def answer_id(self, answer_id):
        """
        Sets the answer_id of this AssessmentQuestionScore.
        The ID of the selected answer

        :param answer_id: The answer_id of this AssessmentQuestionScore.
        :type: str
        """
        

        self._answer_id = answer_id

    @property
    def score(self):
        """
        Gets the score of this AssessmentQuestionScore.
        The score received for this question

        :return: The score of this AssessmentQuestionScore.
        :rtype: int
        """
        return self._score

    @score.setter
    def score(self, score):
        """
        Sets the score of this AssessmentQuestionScore.
        The score received for this question

        :param score: The score of this AssessmentQuestionScore.
        :type: int
        """
        

        self._score = score

    @property
    def marked_na(self):
        """
        Gets the marked_na of this AssessmentQuestionScore.
        True if this question was marked as NA

        :return: The marked_na of this AssessmentQuestionScore.
        :rtype: bool
        """
        return self._marked_na

    @marked_na.setter
    def marked_na(self, marked_na):
        """
        Sets the marked_na of this AssessmentQuestionScore.
        True if this question was marked as NA

        :param marked_na: The marked_na of this AssessmentQuestionScore.
        :type: bool
        """
        

        self._marked_na = marked_na

    @property
    def free_text_answer(self):
        """
        Gets the free_text_answer of this AssessmentQuestionScore.
        Answer for free text answer type

        :return: The free_text_answer of this AssessmentQuestionScore.
        :rtype: str
        """
        return self._free_text_answer

    @free_text_answer.setter
    def free_text_answer(self, free_text_answer):
        """
        Sets the free_text_answer of this AssessmentQuestionScore.
        Answer for free text answer type

        :param free_text_answer: The free_text_answer of this AssessmentQuestionScore.
        :type: str
        """
        

        self._free_text_answer = free_text_answer

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

