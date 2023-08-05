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

class WfmBuScheduleTopicBuManagementUnitScheduleSummary(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WfmBuScheduleTopicBuManagementUnitScheduleSummary - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'management_unit': 'WfmBuScheduleTopicManagementUnit',
            'start_date': 'datetime',
            'end_date': 'datetime',
            'agents': 'list[WfmBuScheduleTopicUserReference]',
            'agent_count': 'int'
        }

        self.attribute_map = {
            'management_unit': 'managementUnit',
            'start_date': 'startDate',
            'end_date': 'endDate',
            'agents': 'agents',
            'agent_count': 'agentCount'
        }

        self._management_unit = None
        self._start_date = None
        self._end_date = None
        self._agents = None
        self._agent_count = None

    @property
    def management_unit(self):
        """
        Gets the management_unit of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.


        :return: The management_unit of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.
        :rtype: WfmBuScheduleTopicManagementUnit
        """
        return self._management_unit

    @management_unit.setter
    def management_unit(self, management_unit):
        """
        Sets the management_unit of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.


        :param management_unit: The management_unit of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.
        :type: WfmBuScheduleTopicManagementUnit
        """
        

        self._management_unit = management_unit

    @property
    def start_date(self):
        """
        Gets the start_date of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.


        :return: The start_date of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.


        :param start_date: The start_date of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.
        :type: datetime
        """
        

        self._start_date = start_date

    @property
    def end_date(self):
        """
        Gets the end_date of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.


        :return: The end_date of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Sets the end_date of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.


        :param end_date: The end_date of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.
        :type: datetime
        """
        

        self._end_date = end_date

    @property
    def agents(self):
        """
        Gets the agents of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.


        :return: The agents of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.
        :rtype: list[WfmBuScheduleTopicUserReference]
        """
        return self._agents

    @agents.setter
    def agents(self, agents):
        """
        Sets the agents of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.


        :param agents: The agents of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.
        :type: list[WfmBuScheduleTopicUserReference]
        """
        

        self._agents = agents

    @property
    def agent_count(self):
        """
        Gets the agent_count of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.


        :return: The agent_count of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.
        :rtype: int
        """
        return self._agent_count

    @agent_count.setter
    def agent_count(self, agent_count):
        """
        Sets the agent_count of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.


        :param agent_count: The agent_count of this WfmBuScheduleTopicBuManagementUnitScheduleSummary.
        :type: int
        """
        

        self._agent_count = agent_count

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

