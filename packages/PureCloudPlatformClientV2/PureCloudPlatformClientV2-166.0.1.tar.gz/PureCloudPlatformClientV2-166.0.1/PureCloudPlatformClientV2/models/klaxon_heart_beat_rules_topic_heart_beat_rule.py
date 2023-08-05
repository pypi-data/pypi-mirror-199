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

class KlaxonHeartBeatRulesTopicHeartBeatRule(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        KlaxonHeartBeatRulesTopicHeartBeatRule - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'sender_id': 'str',
            'heart_beat_timeout_in_minutes': 'float',
            'enabled': 'bool',
            'in_alarm': 'bool',
            'notification_users': 'list[KlaxonHeartBeatRulesTopicNotificationUser]',
            'alert_types': 'list[str]',
            'rule_type': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'sender_id': 'senderId',
            'heart_beat_timeout_in_minutes': 'heartBeatTimeoutInMinutes',
            'enabled': 'enabled',
            'in_alarm': 'inAlarm',
            'notification_users': 'notificationUsers',
            'alert_types': 'alertTypes',
            'rule_type': 'ruleType'
        }

        self._id = None
        self._name = None
        self._sender_id = None
        self._heart_beat_timeout_in_minutes = None
        self._enabled = None
        self._in_alarm = None
        self._notification_users = None
        self._alert_types = None
        self._rule_type = None

    @property
    def id(self):
        """
        Gets the id of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :return: The id of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :param id: The id of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :return: The name of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :param name: The name of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :type: str
        """
        

        self._name = name

    @property
    def sender_id(self):
        """
        Gets the sender_id of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :return: The sender_id of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :rtype: str
        """
        return self._sender_id

    @sender_id.setter
    def sender_id(self, sender_id):
        """
        Sets the sender_id of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :param sender_id: The sender_id of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :type: str
        """
        

        self._sender_id = sender_id

    @property
    def heart_beat_timeout_in_minutes(self):
        """
        Gets the heart_beat_timeout_in_minutes of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :return: The heart_beat_timeout_in_minutes of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :rtype: float
        """
        return self._heart_beat_timeout_in_minutes

    @heart_beat_timeout_in_minutes.setter
    def heart_beat_timeout_in_minutes(self, heart_beat_timeout_in_minutes):
        """
        Sets the heart_beat_timeout_in_minutes of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :param heart_beat_timeout_in_minutes: The heart_beat_timeout_in_minutes of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :type: float
        """
        

        self._heart_beat_timeout_in_minutes = heart_beat_timeout_in_minutes

    @property
    def enabled(self):
        """
        Gets the enabled of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :return: The enabled of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :param enabled: The enabled of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :type: bool
        """
        

        self._enabled = enabled

    @property
    def in_alarm(self):
        """
        Gets the in_alarm of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :return: The in_alarm of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :rtype: bool
        """
        return self._in_alarm

    @in_alarm.setter
    def in_alarm(self, in_alarm):
        """
        Sets the in_alarm of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :param in_alarm: The in_alarm of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :type: bool
        """
        

        self._in_alarm = in_alarm

    @property
    def notification_users(self):
        """
        Gets the notification_users of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :return: The notification_users of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :rtype: list[KlaxonHeartBeatRulesTopicNotificationUser]
        """
        return self._notification_users

    @notification_users.setter
    def notification_users(self, notification_users):
        """
        Sets the notification_users of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :param notification_users: The notification_users of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :type: list[KlaxonHeartBeatRulesTopicNotificationUser]
        """
        

        self._notification_users = notification_users

    @property
    def alert_types(self):
        """
        Gets the alert_types of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :return: The alert_types of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :rtype: list[str]
        """
        return self._alert_types

    @alert_types.setter
    def alert_types(self, alert_types):
        """
        Sets the alert_types of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :param alert_types: The alert_types of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :type: list[str]
        """
        

        self._alert_types = alert_types

    @property
    def rule_type(self):
        """
        Gets the rule_type of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :return: The rule_type of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :rtype: str
        """
        return self._rule_type

    @rule_type.setter
    def rule_type(self, rule_type):
        """
        Sets the rule_type of this KlaxonHeartBeatRulesTopicHeartBeatRule.


        :param rule_type: The rule_type of this KlaxonHeartBeatRulesTopicHeartBeatRule.
        :type: str
        """
        allowed_values = ["EDGE"]
        if rule_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for rule_type -> " + rule_type)
            self._rule_type = "outdated_sdk_version"
        else:
            self._rule_type = rule_type

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

