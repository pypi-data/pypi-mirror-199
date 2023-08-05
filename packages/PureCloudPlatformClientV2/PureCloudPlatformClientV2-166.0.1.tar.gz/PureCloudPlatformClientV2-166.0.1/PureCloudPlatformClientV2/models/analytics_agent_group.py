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

class AnalyticsAgentGroup(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        AnalyticsAgentGroup - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'agent_group_id': 'str',
            'agent_group_type': 'str'
        }

        self.attribute_map = {
            'agent_group_id': 'agentGroupId',
            'agent_group_type': 'agentGroupType'
        }

        self._agent_group_id = None
        self._agent_group_type = None

    @property
    def agent_group_id(self):
        """
        Gets the agent_group_id of this AnalyticsAgentGroup.
        Conditional group routing agent group identifier

        :return: The agent_group_id of this AnalyticsAgentGroup.
        :rtype: str
        """
        return self._agent_group_id

    @agent_group_id.setter
    def agent_group_id(self, agent_group_id):
        """
        Sets the agent_group_id of this AnalyticsAgentGroup.
        Conditional group routing agent group identifier

        :param agent_group_id: The agent_group_id of this AnalyticsAgentGroup.
        :type: str
        """
        

        self._agent_group_id = agent_group_id

    @property
    def agent_group_type(self):
        """
        Gets the agent_group_type of this AnalyticsAgentGroup.
        Conditional group routing agent group type

        :return: The agent_group_type of this AnalyticsAgentGroup.
        :rtype: str
        """
        return self._agent_group_type

    @agent_group_type.setter
    def agent_group_type(self, agent_group_type):
        """
        Sets the agent_group_type of this AnalyticsAgentGroup.
        Conditional group routing agent group type

        :param agent_group_type: The agent_group_type of this AnalyticsAgentGroup.
        :type: str
        """
        allowed_values = ["Group", "SkillGroup", "Team"]
        if agent_group_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for agent_group_type -> " + agent_group_type)
            self._agent_group_type = "outdated_sdk_version"
        else:
            self._agent_group_type = agent_group_type

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

