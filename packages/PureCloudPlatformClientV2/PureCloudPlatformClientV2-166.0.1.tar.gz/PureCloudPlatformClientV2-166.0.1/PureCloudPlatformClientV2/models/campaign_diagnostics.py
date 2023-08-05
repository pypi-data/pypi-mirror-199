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

class CampaignDiagnostics(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CampaignDiagnostics - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'callable_contacts': 'CallableContactsDiagnostic',
            'queue_utilization_diagnostic': 'QueueUtilizationDiagnostic',
            'rule_set_diagnostics': 'list[RuleSetDiagnostic]',
            'outstanding_interactions_count': 'int',
            'scheduled_interactions_count': 'int'
        }

        self.attribute_map = {
            'callable_contacts': 'callableContacts',
            'queue_utilization_diagnostic': 'queueUtilizationDiagnostic',
            'rule_set_diagnostics': 'ruleSetDiagnostics',
            'outstanding_interactions_count': 'outstandingInteractionsCount',
            'scheduled_interactions_count': 'scheduledInteractionsCount'
        }

        self._callable_contacts = None
        self._queue_utilization_diagnostic = None
        self._rule_set_diagnostics = None
        self._outstanding_interactions_count = None
        self._scheduled_interactions_count = None

    @property
    def callable_contacts(self):
        """
        Gets the callable_contacts of this CampaignDiagnostics.
        Campaign properties that can impact which contacts are callable

        :return: The callable_contacts of this CampaignDiagnostics.
        :rtype: CallableContactsDiagnostic
        """
        return self._callable_contacts

    @callable_contacts.setter
    def callable_contacts(self, callable_contacts):
        """
        Sets the callable_contacts of this CampaignDiagnostics.
        Campaign properties that can impact which contacts are callable

        :param callable_contacts: The callable_contacts of this CampaignDiagnostics.
        :type: CallableContactsDiagnostic
        """
        

        self._callable_contacts = callable_contacts

    @property
    def queue_utilization_diagnostic(self):
        """
        Gets the queue_utilization_diagnostic of this CampaignDiagnostics.
        Information regarding the campaign's queue

        :return: The queue_utilization_diagnostic of this CampaignDiagnostics.
        :rtype: QueueUtilizationDiagnostic
        """
        return self._queue_utilization_diagnostic

    @queue_utilization_diagnostic.setter
    def queue_utilization_diagnostic(self, queue_utilization_diagnostic):
        """
        Sets the queue_utilization_diagnostic of this CampaignDiagnostics.
        Information regarding the campaign's queue

        :param queue_utilization_diagnostic: The queue_utilization_diagnostic of this CampaignDiagnostics.
        :type: QueueUtilizationDiagnostic
        """
        

        self._queue_utilization_diagnostic = queue_utilization_diagnostic

    @property
    def rule_set_diagnostics(self):
        """
        Gets the rule_set_diagnostics of this CampaignDiagnostics.
        Information regarding the campaign's rule sets

        :return: The rule_set_diagnostics of this CampaignDiagnostics.
        :rtype: list[RuleSetDiagnostic]
        """
        return self._rule_set_diagnostics

    @rule_set_diagnostics.setter
    def rule_set_diagnostics(self, rule_set_diagnostics):
        """
        Sets the rule_set_diagnostics of this CampaignDiagnostics.
        Information regarding the campaign's rule sets

        :param rule_set_diagnostics: The rule_set_diagnostics of this CampaignDiagnostics.
        :type: list[RuleSetDiagnostic]
        """
        

        self._rule_set_diagnostics = rule_set_diagnostics

    @property
    def outstanding_interactions_count(self):
        """
        Gets the outstanding_interactions_count of this CampaignDiagnostics.
        Current number of outstanding interactions on the campaign

        :return: The outstanding_interactions_count of this CampaignDiagnostics.
        :rtype: int
        """
        return self._outstanding_interactions_count

    @outstanding_interactions_count.setter
    def outstanding_interactions_count(self, outstanding_interactions_count):
        """
        Sets the outstanding_interactions_count of this CampaignDiagnostics.
        Current number of outstanding interactions on the campaign

        :param outstanding_interactions_count: The outstanding_interactions_count of this CampaignDiagnostics.
        :type: int
        """
        

        self._outstanding_interactions_count = outstanding_interactions_count

    @property
    def scheduled_interactions_count(self):
        """
        Gets the scheduled_interactions_count of this CampaignDiagnostics.
        Current number of scheduled interactions on the campaign

        :return: The scheduled_interactions_count of this CampaignDiagnostics.
        :rtype: int
        """
        return self._scheduled_interactions_count

    @scheduled_interactions_count.setter
    def scheduled_interactions_count(self, scheduled_interactions_count):
        """
        Sets the scheduled_interactions_count of this CampaignDiagnostics.
        Current number of scheduled interactions on the campaign

        :param scheduled_interactions_count: The scheduled_interactions_count of this CampaignDiagnostics.
        :type: int
        """
        

        self._scheduled_interactions_count = scheduled_interactions_count

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

