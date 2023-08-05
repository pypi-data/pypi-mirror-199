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

class ConversationMetricsTopicConversationProposedAgent(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ConversationMetricsTopicConversationProposedAgent - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'agent_rank': 'int',
            'proposed_agent_id': 'str'
        }

        self.attribute_map = {
            'agent_rank': 'agentRank',
            'proposed_agent_id': 'proposedAgentId'
        }

        self._agent_rank = None
        self._proposed_agent_id = None

    @property
    def agent_rank(self):
        """
        Gets the agent_rank of this ConversationMetricsTopicConversationProposedAgent.
        Proposed agent rank for this conversation from predictive routing (lower is better)

        :return: The agent_rank of this ConversationMetricsTopicConversationProposedAgent.
        :rtype: int
        """
        return self._agent_rank

    @agent_rank.setter
    def agent_rank(self, agent_rank):
        """
        Sets the agent_rank of this ConversationMetricsTopicConversationProposedAgent.
        Proposed agent rank for this conversation from predictive routing (lower is better)

        :param agent_rank: The agent_rank of this ConversationMetricsTopicConversationProposedAgent.
        :type: int
        """
        

        self._agent_rank = agent_rank

    @property
    def proposed_agent_id(self):
        """
        Gets the proposed_agent_id of this ConversationMetricsTopicConversationProposedAgent.
        Unique identifier for the agent that was proposed by predictive routing

        :return: The proposed_agent_id of this ConversationMetricsTopicConversationProposedAgent.
        :rtype: str
        """
        return self._proposed_agent_id

    @proposed_agent_id.setter
    def proposed_agent_id(self, proposed_agent_id):
        """
        Sets the proposed_agent_id of this ConversationMetricsTopicConversationProposedAgent.
        Unique identifier for the agent that was proposed by predictive routing

        :param proposed_agent_id: The proposed_agent_id of this ConversationMetricsTopicConversationProposedAgent.
        :type: str
        """
        

        self._proposed_agent_id = proposed_agent_id

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

