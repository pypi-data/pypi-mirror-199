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

class UpdateActivityCodeRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        UpdateActivityCodeRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'category': 'str',
            'length_in_minutes': 'int',
            'counts_as_paid_time': 'bool',
            'counts_as_work_time': 'bool',
            'agent_time_off_selectable': 'bool',
            'counts_toward_shrinkage': 'bool',
            'planned_shrinkage': 'bool',
            'interruptible': 'bool',
            'secondary_presences': 'ListWrapperSecondaryPresence',
            'metadata': 'WfmVersionedEntityMetadata'
        }

        self.attribute_map = {
            'name': 'name',
            'category': 'category',
            'length_in_minutes': 'lengthInMinutes',
            'counts_as_paid_time': 'countsAsPaidTime',
            'counts_as_work_time': 'countsAsWorkTime',
            'agent_time_off_selectable': 'agentTimeOffSelectable',
            'counts_toward_shrinkage': 'countsTowardShrinkage',
            'planned_shrinkage': 'plannedShrinkage',
            'interruptible': 'interruptible',
            'secondary_presences': 'secondaryPresences',
            'metadata': 'metadata'
        }

        self._name = None
        self._category = None
        self._length_in_minutes = None
        self._counts_as_paid_time = None
        self._counts_as_work_time = None
        self._agent_time_off_selectable = None
        self._counts_toward_shrinkage = None
        self._planned_shrinkage = None
        self._interruptible = None
        self._secondary_presences = None
        self._metadata = None

    @property
    def name(self):
        """
        Gets the name of this UpdateActivityCodeRequest.
        The name of the activity code

        :return: The name of this UpdateActivityCodeRequest.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this UpdateActivityCodeRequest.
        The name of the activity code

        :param name: The name of this UpdateActivityCodeRequest.
        :type: str
        """
        

        self._name = name

    @property
    def category(self):
        """
        Gets the category of this UpdateActivityCodeRequest.
        The activity code's category. Attempting to change the category of a default activity code will return an error

        :return: The category of this UpdateActivityCodeRequest.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Sets the category of this UpdateActivityCodeRequest.
        The activity code's category. Attempting to change the category of a default activity code will return an error

        :param category: The category of this UpdateActivityCodeRequest.
        :type: str
        """
        allowed_values = ["OnQueueWork", "Break", "Meal", "Meeting", "OffQueueWork", "TimeOff", "Training", "Unavailable", "Unscheduled"]
        if category.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for category -> " + category)
            self._category = "outdated_sdk_version"
        else:
            self._category = category

    @property
    def length_in_minutes(self):
        """
        Gets the length_in_minutes of this UpdateActivityCodeRequest.
        The default length of the activity in minutes

        :return: The length_in_minutes of this UpdateActivityCodeRequest.
        :rtype: int
        """
        return self._length_in_minutes

    @length_in_minutes.setter
    def length_in_minutes(self, length_in_minutes):
        """
        Sets the length_in_minutes of this UpdateActivityCodeRequest.
        The default length of the activity in minutes

        :param length_in_minutes: The length_in_minutes of this UpdateActivityCodeRequest.
        :type: int
        """
        

        self._length_in_minutes = length_in_minutes

    @property
    def counts_as_paid_time(self):
        """
        Gets the counts_as_paid_time of this UpdateActivityCodeRequest.
        Whether an agent is paid while performing this activity

        :return: The counts_as_paid_time of this UpdateActivityCodeRequest.
        :rtype: bool
        """
        return self._counts_as_paid_time

    @counts_as_paid_time.setter
    def counts_as_paid_time(self, counts_as_paid_time):
        """
        Sets the counts_as_paid_time of this UpdateActivityCodeRequest.
        Whether an agent is paid while performing this activity

        :param counts_as_paid_time: The counts_as_paid_time of this UpdateActivityCodeRequest.
        :type: bool
        """
        

        self._counts_as_paid_time = counts_as_paid_time

    @property
    def counts_as_work_time(self):
        """
        Gets the counts_as_work_time of this UpdateActivityCodeRequest.
        Indicates whether or not the activity should be counted as work time

        :return: The counts_as_work_time of this UpdateActivityCodeRequest.
        :rtype: bool
        """
        return self._counts_as_work_time

    @counts_as_work_time.setter
    def counts_as_work_time(self, counts_as_work_time):
        """
        Sets the counts_as_work_time of this UpdateActivityCodeRequest.
        Indicates whether or not the activity should be counted as work time

        :param counts_as_work_time: The counts_as_work_time of this UpdateActivityCodeRequest.
        :type: bool
        """
        

        self._counts_as_work_time = counts_as_work_time

    @property
    def agent_time_off_selectable(self):
        """
        Gets the agent_time_off_selectable of this UpdateActivityCodeRequest.
        Whether an agent can select this activity code when creating or editing a time off request

        :return: The agent_time_off_selectable of this UpdateActivityCodeRequest.
        :rtype: bool
        """
        return self._agent_time_off_selectable

    @agent_time_off_selectable.setter
    def agent_time_off_selectable(self, agent_time_off_selectable):
        """
        Sets the agent_time_off_selectable of this UpdateActivityCodeRequest.
        Whether an agent can select this activity code when creating or editing a time off request

        :param agent_time_off_selectable: The agent_time_off_selectable of this UpdateActivityCodeRequest.
        :type: bool
        """
        

        self._agent_time_off_selectable = agent_time_off_selectable

    @property
    def counts_toward_shrinkage(self):
        """
        Gets the counts_toward_shrinkage of this UpdateActivityCodeRequest.
        Whether or not this activity code counts toward shrinkage calculations

        :return: The counts_toward_shrinkage of this UpdateActivityCodeRequest.
        :rtype: bool
        """
        return self._counts_toward_shrinkage

    @counts_toward_shrinkage.setter
    def counts_toward_shrinkage(self, counts_toward_shrinkage):
        """
        Sets the counts_toward_shrinkage of this UpdateActivityCodeRequest.
        Whether or not this activity code counts toward shrinkage calculations

        :param counts_toward_shrinkage: The counts_toward_shrinkage of this UpdateActivityCodeRequest.
        :type: bool
        """
        

        self._counts_toward_shrinkage = counts_toward_shrinkage

    @property
    def planned_shrinkage(self):
        """
        Gets the planned_shrinkage of this UpdateActivityCodeRequest.
        Whether this activity code is considered planned or unplanned shrinkage

        :return: The planned_shrinkage of this UpdateActivityCodeRequest.
        :rtype: bool
        """
        return self._planned_shrinkage

    @planned_shrinkage.setter
    def planned_shrinkage(self, planned_shrinkage):
        """
        Sets the planned_shrinkage of this UpdateActivityCodeRequest.
        Whether this activity code is considered planned or unplanned shrinkage

        :param planned_shrinkage: The planned_shrinkage of this UpdateActivityCodeRequest.
        :type: bool
        """
        

        self._planned_shrinkage = planned_shrinkage

    @property
    def interruptible(self):
        """
        Gets the interruptible of this UpdateActivityCodeRequest.
        Whether this activity code is considered interruptible

        :return: The interruptible of this UpdateActivityCodeRequest.
        :rtype: bool
        """
        return self._interruptible

    @interruptible.setter
    def interruptible(self, interruptible):
        """
        Sets the interruptible of this UpdateActivityCodeRequest.
        Whether this activity code is considered interruptible

        :param interruptible: The interruptible of this UpdateActivityCodeRequest.
        :type: bool
        """
        

        self._interruptible = interruptible

    @property
    def secondary_presences(self):
        """
        Gets the secondary_presences of this UpdateActivityCodeRequest.
        The secondary presences of this activity code

        :return: The secondary_presences of this UpdateActivityCodeRequest.
        :rtype: ListWrapperSecondaryPresence
        """
        return self._secondary_presences

    @secondary_presences.setter
    def secondary_presences(self, secondary_presences):
        """
        Sets the secondary_presences of this UpdateActivityCodeRequest.
        The secondary presences of this activity code

        :param secondary_presences: The secondary_presences of this UpdateActivityCodeRequest.
        :type: ListWrapperSecondaryPresence
        """
        

        self._secondary_presences = secondary_presences

    @property
    def metadata(self):
        """
        Gets the metadata of this UpdateActivityCodeRequest.
        Version metadata for the associated business unit's list of activity codes

        :return: The metadata of this UpdateActivityCodeRequest.
        :rtype: WfmVersionedEntityMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this UpdateActivityCodeRequest.
        Version metadata for the associated business unit's list of activity codes

        :param metadata: The metadata of this UpdateActivityCodeRequest.
        :type: WfmVersionedEntityMetadata
        """
        

        self._metadata = metadata

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

