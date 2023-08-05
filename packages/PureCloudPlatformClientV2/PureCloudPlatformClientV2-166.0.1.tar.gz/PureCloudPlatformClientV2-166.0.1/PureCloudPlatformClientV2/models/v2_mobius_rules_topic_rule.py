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

class V2MobiusRulesTopicRule(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        V2MobiusRulesTopicRule - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'user_id': 'str',
            'name': 'str',
            'type': 'str',
            'notifications': 'list[V2MobiusRulesTopicAlertNotification]',
            'conditions': 'V2MobiusRulesTopicCondition',
            'enabled': 'bool',
            'in_alarm': 'bool',
            'action': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'user_id': 'userId',
            'name': 'name',
            'type': 'type',
            'notifications': 'notifications',
            'conditions': 'conditions',
            'enabled': 'enabled',
            'in_alarm': 'inAlarm',
            'action': 'action'
        }

        self._id = None
        self._user_id = None
        self._name = None
        self._type = None
        self._notifications = None
        self._conditions = None
        self._enabled = None
        self._in_alarm = None
        self._action = None

    @property
    def id(self):
        """
        Gets the id of this V2MobiusRulesTopicRule.


        :return: The id of this V2MobiusRulesTopicRule.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this V2MobiusRulesTopicRule.


        :param id: The id of this V2MobiusRulesTopicRule.
        :type: str
        """
        

        self._id = id

    @property
    def user_id(self):
        """
        Gets the user_id of this V2MobiusRulesTopicRule.


        :return: The user_id of this V2MobiusRulesTopicRule.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this V2MobiusRulesTopicRule.


        :param user_id: The user_id of this V2MobiusRulesTopicRule.
        :type: str
        """
        

        self._user_id = user_id

    @property
    def name(self):
        """
        Gets the name of this V2MobiusRulesTopicRule.


        :return: The name of this V2MobiusRulesTopicRule.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this V2MobiusRulesTopicRule.


        :param name: The name of this V2MobiusRulesTopicRule.
        :type: str
        """
        

        self._name = name

    @property
    def type(self):
        """
        Gets the type of this V2MobiusRulesTopicRule.


        :return: The type of this V2MobiusRulesTopicRule.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this V2MobiusRulesTopicRule.


        :param type: The type of this V2MobiusRulesTopicRule.
        :type: str
        """
        allowed_values = ["ConversationMetrics", "UserPresence", "Unknown"]
        if type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for type -> " + type)
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def notifications(self):
        """
        Gets the notifications of this V2MobiusRulesTopicRule.


        :return: The notifications of this V2MobiusRulesTopicRule.
        :rtype: list[V2MobiusRulesTopicAlertNotification]
        """
        return self._notifications

    @notifications.setter
    def notifications(self, notifications):
        """
        Sets the notifications of this V2MobiusRulesTopicRule.


        :param notifications: The notifications of this V2MobiusRulesTopicRule.
        :type: list[V2MobiusRulesTopicAlertNotification]
        """
        

        self._notifications = notifications

    @property
    def conditions(self):
        """
        Gets the conditions of this V2MobiusRulesTopicRule.


        :return: The conditions of this V2MobiusRulesTopicRule.
        :rtype: V2MobiusRulesTopicCondition
        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        """
        Sets the conditions of this V2MobiusRulesTopicRule.


        :param conditions: The conditions of this V2MobiusRulesTopicRule.
        :type: V2MobiusRulesTopicCondition
        """
        

        self._conditions = conditions

    @property
    def enabled(self):
        """
        Gets the enabled of this V2MobiusRulesTopicRule.


        :return: The enabled of this V2MobiusRulesTopicRule.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this V2MobiusRulesTopicRule.


        :param enabled: The enabled of this V2MobiusRulesTopicRule.
        :type: bool
        """
        

        self._enabled = enabled

    @property
    def in_alarm(self):
        """
        Gets the in_alarm of this V2MobiusRulesTopicRule.


        :return: The in_alarm of this V2MobiusRulesTopicRule.
        :rtype: bool
        """
        return self._in_alarm

    @in_alarm.setter
    def in_alarm(self, in_alarm):
        """
        Sets the in_alarm of this V2MobiusRulesTopicRule.


        :param in_alarm: The in_alarm of this V2MobiusRulesTopicRule.
        :type: bool
        """
        

        self._in_alarm = in_alarm

    @property
    def action(self):
        """
        Gets the action of this V2MobiusRulesTopicRule.


        :return: The action of this V2MobiusRulesTopicRule.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this V2MobiusRulesTopicRule.


        :param action: The action of this V2MobiusRulesTopicRule.
        :type: str
        """
        allowed_values = ["UNKNOWN", "CREATE", "UPDATE", "DELETE"]
        if action.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for action -> " + action)
            self._action = "outdated_sdk_version"
        else:
            self._action = action

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

