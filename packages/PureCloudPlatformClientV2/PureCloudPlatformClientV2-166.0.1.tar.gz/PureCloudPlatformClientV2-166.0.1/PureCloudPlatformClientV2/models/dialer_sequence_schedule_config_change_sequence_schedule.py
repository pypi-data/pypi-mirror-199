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

class DialerSequenceScheduleConfigChangeSequenceSchedule(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DialerSequenceScheduleConfigChangeSequenceSchedule - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'intervals': 'list[DialerSequenceScheduleConfigChangeScheduleInterval]',
            'time_zone': 'str',
            'sequence': 'DialerSequenceScheduleConfigChangeUriReference',
            'additional_properties': 'dict(str, object)',
            'id': 'str',
            'name': 'str',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'version': 'int'
        }

        self.attribute_map = {
            'intervals': 'intervals',
            'time_zone': 'timeZone',
            'sequence': 'sequence',
            'additional_properties': 'additionalProperties',
            'id': 'id',
            'name': 'name',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'version': 'version'
        }

        self._intervals = None
        self._time_zone = None
        self._sequence = None
        self._additional_properties = None
        self._id = None
        self._name = None
        self._date_created = None
        self._date_modified = None
        self._version = None

    @property
    def intervals(self):
        """
        Gets the intervals of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        a list of start and end times

        :return: The intervals of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :rtype: list[DialerSequenceScheduleConfigChangeScheduleInterval]
        """
        return self._intervals

    @intervals.setter
    def intervals(self, intervals):
        """
        Sets the intervals of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        a list of start and end times

        :param intervals: The intervals of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :type: list[DialerSequenceScheduleConfigChangeScheduleInterval]
        """
        

        self._intervals = intervals

    @property
    def time_zone(self):
        """
        Gets the time_zone of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        time zone identifier to be applied to the intervals; for example Africa/Abidjan

        :return: The time_zone of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :rtype: str
        """
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        """
        Sets the time_zone of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        time zone identifier to be applied to the intervals; for example Africa/Abidjan

        :param time_zone: The time_zone of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :type: str
        """
        

        self._time_zone = time_zone

    @property
    def sequence(self):
        """
        Gets the sequence of this DialerSequenceScheduleConfigChangeSequenceSchedule.


        :return: The sequence of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :rtype: DialerSequenceScheduleConfigChangeUriReference
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """
        Sets the sequence of this DialerSequenceScheduleConfigChangeSequenceSchedule.


        :param sequence: The sequence of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :type: DialerSequenceScheduleConfigChangeUriReference
        """
        

        self._sequence = sequence

    @property
    def additional_properties(self):
        """
        Gets the additional_properties of this DialerSequenceScheduleConfigChangeSequenceSchedule.


        :return: The additional_properties of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :rtype: dict(str, object)
        """
        return self._additional_properties

    @additional_properties.setter
    def additional_properties(self, additional_properties):
        """
        Sets the additional_properties of this DialerSequenceScheduleConfigChangeSequenceSchedule.


        :param additional_properties: The additional_properties of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :type: dict(str, object)
        """
        

        self._additional_properties = additional_properties

    @property
    def id(self):
        """
        Gets the id of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        The globally unique identifier for the object.

        :return: The id of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        The globally unique identifier for the object.

        :param id: The id of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        The UI-visible name of the object

        :return: The name of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        The UI-visible name of the object

        :param name: The name of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :type: str
        """
        

        self._name = name

    @property
    def date_created(self):
        """
        Gets the date_created of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        Creation time of the entity

        :return: The date_created of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        Creation time of the entity

        :param date_created: The date_created of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :type: datetime
        """
        

        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        Last modified time of the entity

        :return: The date_modified of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        Last modified time of the entity

        :param date_modified: The date_modified of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :type: datetime
        """
        

        self._date_modified = date_modified

    @property
    def version(self):
        """
        Gets the version of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        Required for updates, must match the version number of the most recent update

        :return: The version of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        Required for updates, must match the version number of the most recent update

        :param version: The version of this DialerSequenceScheduleConfigChangeSequenceSchedule.
        :type: int
        """
        

        self._version = version

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

