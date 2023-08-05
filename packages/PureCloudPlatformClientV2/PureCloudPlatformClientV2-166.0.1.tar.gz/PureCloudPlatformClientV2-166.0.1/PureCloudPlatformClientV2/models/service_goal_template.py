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

class ServiceGoalTemplate(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ServiceGoalTemplate - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'service_level': 'BuServiceLevel',
            'average_speed_of_answer': 'BuAverageSpeedOfAnswer',
            'abandon_rate': 'BuAbandonRate',
            'metadata': 'WfmVersionedEntityMetadata',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'service_level': 'serviceLevel',
            'average_speed_of_answer': 'averageSpeedOfAnswer',
            'abandon_rate': 'abandonRate',
            'metadata': 'metadata',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._service_level = None
        self._average_speed_of_answer = None
        self._abandon_rate = None
        self._metadata = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this ServiceGoalTemplate.
        The globally unique identifier for the object.

        :return: The id of this ServiceGoalTemplate.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ServiceGoalTemplate.
        The globally unique identifier for the object.

        :param id: The id of this ServiceGoalTemplate.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ServiceGoalTemplate.


        :return: The name of this ServiceGoalTemplate.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ServiceGoalTemplate.


        :param name: The name of this ServiceGoalTemplate.
        :type: str
        """
        

        self._name = name

    @property
    def service_level(self):
        """
        Gets the service_level of this ServiceGoalTemplate.
        Service level targets for this service goal template

        :return: The service_level of this ServiceGoalTemplate.
        :rtype: BuServiceLevel
        """
        return self._service_level

    @service_level.setter
    def service_level(self, service_level):
        """
        Sets the service_level of this ServiceGoalTemplate.
        Service level targets for this service goal template

        :param service_level: The service_level of this ServiceGoalTemplate.
        :type: BuServiceLevel
        """
        

        self._service_level = service_level

    @property
    def average_speed_of_answer(self):
        """
        Gets the average_speed_of_answer of this ServiceGoalTemplate.
        Average speed of answer targets for this service goal template

        :return: The average_speed_of_answer of this ServiceGoalTemplate.
        :rtype: BuAverageSpeedOfAnswer
        """
        return self._average_speed_of_answer

    @average_speed_of_answer.setter
    def average_speed_of_answer(self, average_speed_of_answer):
        """
        Sets the average_speed_of_answer of this ServiceGoalTemplate.
        Average speed of answer targets for this service goal template

        :param average_speed_of_answer: The average_speed_of_answer of this ServiceGoalTemplate.
        :type: BuAverageSpeedOfAnswer
        """
        

        self._average_speed_of_answer = average_speed_of_answer

    @property
    def abandon_rate(self):
        """
        Gets the abandon_rate of this ServiceGoalTemplate.
        Abandon rate targets for this service goal template

        :return: The abandon_rate of this ServiceGoalTemplate.
        :rtype: BuAbandonRate
        """
        return self._abandon_rate

    @abandon_rate.setter
    def abandon_rate(self, abandon_rate):
        """
        Sets the abandon_rate of this ServiceGoalTemplate.
        Abandon rate targets for this service goal template

        :param abandon_rate: The abandon_rate of this ServiceGoalTemplate.
        :type: BuAbandonRate
        """
        

        self._abandon_rate = abandon_rate

    @property
    def metadata(self):
        """
        Gets the metadata of this ServiceGoalTemplate.
        Version metadata for the service goal template

        :return: The metadata of this ServiceGoalTemplate.
        :rtype: WfmVersionedEntityMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this ServiceGoalTemplate.
        Version metadata for the service goal template

        :param metadata: The metadata of this ServiceGoalTemplate.
        :type: WfmVersionedEntityMetadata
        """
        

        self._metadata = metadata

    @property
    def self_uri(self):
        """
        Gets the self_uri of this ServiceGoalTemplate.
        The URI for this object

        :return: The self_uri of this ServiceGoalTemplate.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this ServiceGoalTemplate.
        The URI for this object

        :param self_uri: The self_uri of this ServiceGoalTemplate.
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

