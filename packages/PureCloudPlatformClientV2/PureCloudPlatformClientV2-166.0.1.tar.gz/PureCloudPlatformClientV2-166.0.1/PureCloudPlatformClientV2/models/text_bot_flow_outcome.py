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

class TextBotFlowOutcome(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        TextBotFlowOutcome - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'outcome_id': 'str',
            'outcome_value': 'str',
            'date_start': 'datetime',
            'date_end': 'datetime',
            'milestones': 'list[TextBotFlowMilestone]'
        }

        self.attribute_map = {
            'outcome_id': 'outcomeId',
            'outcome_value': 'outcomeValue',
            'date_start': 'dateStart',
            'date_end': 'dateEnd',
            'milestones': 'milestones'
        }

        self._outcome_id = None
        self._outcome_value = None
        self._date_start = None
        self._date_end = None
        self._milestones = None

    @property
    def outcome_id(self):
        """
        Gets the outcome_id of this TextBotFlowOutcome.
        The Flow Outcome ID.

        :return: The outcome_id of this TextBotFlowOutcome.
        :rtype: str
        """
        return self._outcome_id

    @outcome_id.setter
    def outcome_id(self, outcome_id):
        """
        Sets the outcome_id of this TextBotFlowOutcome.
        The Flow Outcome ID.

        :param outcome_id: The outcome_id of this TextBotFlowOutcome.
        :type: str
        """
        

        self._outcome_id = outcome_id

    @property
    def outcome_value(self):
        """
        Gets the outcome_value of this TextBotFlowOutcome.
        The value of the FlowOutcome.

        :return: The outcome_value of this TextBotFlowOutcome.
        :rtype: str
        """
        return self._outcome_value

    @outcome_value.setter
    def outcome_value(self, outcome_value):
        """
        Sets the outcome_value of this TextBotFlowOutcome.
        The value of the FlowOutcome.

        :param outcome_value: The outcome_value of this TextBotFlowOutcome.
        :type: str
        """
        allowed_values = ["SUCCESS", "FAILURE"]
        if outcome_value.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for outcome_value -> " + outcome_value)
            self._outcome_value = "outdated_sdk_version"
        else:
            self._outcome_value = outcome_value

    @property
    def date_start(self):
        """
        Gets the date_start of this TextBotFlowOutcome.
        The timestamp for when the Flow Outcome began. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_start of this TextBotFlowOutcome.
        :rtype: datetime
        """
        return self._date_start

    @date_start.setter
    def date_start(self, date_start):
        """
        Sets the date_start of this TextBotFlowOutcome.
        The timestamp for when the Flow Outcome began. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_start: The date_start of this TextBotFlowOutcome.
        :type: datetime
        """
        

        self._date_start = date_start

    @property
    def date_end(self):
        """
        Gets the date_end of this TextBotFlowOutcome.
        The timestamp for when the Flow Outcome finished. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_end of this TextBotFlowOutcome.
        :rtype: datetime
        """
        return self._date_end

    @date_end.setter
    def date_end(self, date_end):
        """
        Sets the date_end of this TextBotFlowOutcome.
        The timestamp for when the Flow Outcome finished. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_end: The date_end of this TextBotFlowOutcome.
        :type: datetime
        """
        

        self._date_end = date_end

    @property
    def milestones(self):
        """
        Gets the milestones of this TextBotFlowOutcome.
        The Flow Milestones for the Flow Outcome.

        :return: The milestones of this TextBotFlowOutcome.
        :rtype: list[TextBotFlowMilestone]
        """
        return self._milestones

    @milestones.setter
    def milestones(self, milestones):
        """
        Sets the milestones of this TextBotFlowOutcome.
        The Flow Milestones for the Flow Outcome.

        :param milestones: The milestones of this TextBotFlowOutcome.
        :type: list[TextBotFlowMilestone]
        """
        

        self._milestones = milestones

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

