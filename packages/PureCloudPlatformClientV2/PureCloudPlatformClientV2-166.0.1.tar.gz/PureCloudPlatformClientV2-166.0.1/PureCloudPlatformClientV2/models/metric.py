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

class Metric(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Metric - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'metric_definition_id': 'str',
            'external_metric_definition_id': 'str',
            'objective': 'Objective',
            'performance_profile_id': 'str',
            'linked_metric': 'AddressableEntityRef',
            'date_created': 'datetime',
            'date_unlinked': 'date',
            'precision': 'int',
            'time_display_unit': 'str',
            'source_performance_profile': 'PerformanceProfile',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'metric_definition_id': 'metricDefinitionId',
            'external_metric_definition_id': 'externalMetricDefinitionId',
            'objective': 'objective',
            'performance_profile_id': 'performanceProfileId',
            'linked_metric': 'linkedMetric',
            'date_created': 'dateCreated',
            'date_unlinked': 'dateUnlinked',
            'precision': 'precision',
            'time_display_unit': 'timeDisplayUnit',
            'source_performance_profile': 'sourcePerformanceProfile',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._metric_definition_id = None
        self._external_metric_definition_id = None
        self._objective = None
        self._performance_profile_id = None
        self._linked_metric = None
        self._date_created = None
        self._date_unlinked = None
        self._precision = None
        self._time_display_unit = None
        self._source_performance_profile = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this Metric.
        The globally unique identifier for the object.

        :return: The id of this Metric.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Metric.
        The globally unique identifier for the object.

        :param id: The id of this Metric.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Metric.
        The name of this metric

        :return: The name of this Metric.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Metric.
        The name of this metric

        :param name: The name of this Metric.
        :type: str
        """
        

        self._name = name

    @property
    def metric_definition_id(self):
        """
        Gets the metric_definition_id of this Metric.
        The id of associated metric definition

        :return: The metric_definition_id of this Metric.
        :rtype: str
        """
        return self._metric_definition_id

    @metric_definition_id.setter
    def metric_definition_id(self, metric_definition_id):
        """
        Sets the metric_definition_id of this Metric.
        The id of associated metric definition

        :param metric_definition_id: The metric_definition_id of this Metric.
        :type: str
        """
        

        self._metric_definition_id = metric_definition_id

    @property
    def external_metric_definition_id(self):
        """
        Gets the external_metric_definition_id of this Metric.
        The id of associated external metric definition

        :return: The external_metric_definition_id of this Metric.
        :rtype: str
        """
        return self._external_metric_definition_id

    @external_metric_definition_id.setter
    def external_metric_definition_id(self, external_metric_definition_id):
        """
        Sets the external_metric_definition_id of this Metric.
        The id of associated external metric definition

        :param external_metric_definition_id: The external_metric_definition_id of this Metric.
        :type: str
        """
        

        self._external_metric_definition_id = external_metric_definition_id

    @property
    def objective(self):
        """
        Gets the objective of this Metric.
        Associated objective for this metric

        :return: The objective of this Metric.
        :rtype: Objective
        """
        return self._objective

    @objective.setter
    def objective(self, objective):
        """
        Sets the objective of this Metric.
        Associated objective for this metric

        :param objective: The objective of this Metric.
        :type: Objective
        """
        

        self._objective = objective

    @property
    def performance_profile_id(self):
        """
        Gets the performance_profile_id of this Metric.
        Performance profile id of this metric

        :return: The performance_profile_id of this Metric.
        :rtype: str
        """
        return self._performance_profile_id

    @performance_profile_id.setter
    def performance_profile_id(self, performance_profile_id):
        """
        Sets the performance_profile_id of this Metric.
        Performance profile id of this metric

        :param performance_profile_id: The performance_profile_id of this Metric.
        :type: str
        """
        

        self._performance_profile_id = performance_profile_id

    @property
    def linked_metric(self):
        """
        Gets the linked_metric of this Metric.
        The linked metric entity reference

        :return: The linked_metric of this Metric.
        :rtype: AddressableEntityRef
        """
        return self._linked_metric

    @linked_metric.setter
    def linked_metric(self, linked_metric):
        """
        Sets the linked_metric of this Metric.
        The linked metric entity reference

        :param linked_metric: The linked_metric of this Metric.
        :type: AddressableEntityRef
        """
        

        self._linked_metric = linked_metric

    @property
    def date_created(self):
        """
        Gets the date_created of this Metric.
        The created date of this metric. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_created of this Metric.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this Metric.
        The created date of this metric. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_created: The date_created of this Metric.
        :type: datetime
        """
        

        self._date_created = date_created

    @property
    def date_unlinked(self):
        """
        Gets the date_unlinked of this Metric.
        The unlinked workday for this metric if this metric was ever unlinked. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :return: The date_unlinked of this Metric.
        :rtype: date
        """
        return self._date_unlinked

    @date_unlinked.setter
    def date_unlinked(self, date_unlinked):
        """
        Sets the date_unlinked of this Metric.
        The unlinked workday for this metric if this metric was ever unlinked. Dates are represented as an ISO-8601 string. For example: yyyy-MM-dd

        :param date_unlinked: The date_unlinked of this Metric.
        :type: date
        """
        

        self._date_unlinked = date_unlinked

    @property
    def precision(self):
        """
        Gets the precision of this Metric.
        The precision of the metric, must be between 0 and 5

        :return: The precision of this Metric.
        :rtype: int
        """
        return self._precision

    @precision.setter
    def precision(self, precision):
        """
        Sets the precision of this Metric.
        The precision of the metric, must be between 0 and 5

        :param precision: The precision of this Metric.
        :type: int
        """
        

        self._precision = precision

    @property
    def time_display_unit(self):
        """
        Gets the time_display_unit of this Metric.
        The time unit in which the metric should be displayed -- this parameter is ignored when displaying non-time values

        :return: The time_display_unit of this Metric.
        :rtype: str
        """
        return self._time_display_unit

    @time_display_unit.setter
    def time_display_unit(self, time_display_unit):
        """
        Sets the time_display_unit of this Metric.
        The time unit in which the metric should be displayed -- this parameter is ignored when displaying non-time values

        :param time_display_unit: The time_display_unit of this Metric.
        :type: str
        """
        allowed_values = ["None", "Seconds", "Minutes", "Hours"]
        if time_display_unit.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for time_display_unit -> " + time_display_unit)
            self._time_display_unit = "outdated_sdk_version"
        else:
            self._time_display_unit = time_display_unit

    @property
    def source_performance_profile(self):
        """
        Gets the source_performance_profile of this Metric.
        The source performance profile when this metric is linked

        :return: The source_performance_profile of this Metric.
        :rtype: PerformanceProfile
        """
        return self._source_performance_profile

    @source_performance_profile.setter
    def source_performance_profile(self, source_performance_profile):
        """
        Sets the source_performance_profile of this Metric.
        The source performance profile when this metric is linked

        :param source_performance_profile: The source_performance_profile of this Metric.
        :type: PerformanceProfile
        """
        

        self._source_performance_profile = source_performance_profile

    @property
    def self_uri(self):
        """
        Gets the self_uri of this Metric.
        The URI for this object

        :return: The self_uri of this Metric.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this Metric.
        The URI for this object

        :param self_uri: The self_uri of this Metric.
        :type: str
        """
        

        self._self_uri = self_uri

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

