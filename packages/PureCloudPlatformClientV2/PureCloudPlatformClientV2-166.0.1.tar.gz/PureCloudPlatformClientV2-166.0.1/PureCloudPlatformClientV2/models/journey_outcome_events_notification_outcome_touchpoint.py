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

class JourneyOutcomeEventsNotificationOutcomeTouchpoint(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        JourneyOutcomeEventsNotificationOutcomeTouchpoint - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'channels': 'list[JourneyOutcomeEventsNotificationOutcomeTouchpointChannel]',
            'created_date': 'datetime',
            'action_map': 'JourneyOutcomeEventsNotificationActionMap'
        }

        self.attribute_map = {
            'id': 'id',
            'channels': 'channels',
            'created_date': 'createdDate',
            'action_map': 'actionMap'
        }

        self._id = None
        self._channels = None
        self._created_date = None
        self._action_map = None

    @property
    def id(self):
        """
        Gets the id of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.


        :return: The id of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.


        :param id: The id of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.
        :type: str
        """
        

        self._id = id

    @property
    def channels(self):
        """
        Gets the channels of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.


        :return: The channels of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.
        :rtype: list[JourneyOutcomeEventsNotificationOutcomeTouchpointChannel]
        """
        return self._channels

    @channels.setter
    def channels(self, channels):
        """
        Sets the channels of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.


        :param channels: The channels of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.
        :type: list[JourneyOutcomeEventsNotificationOutcomeTouchpointChannel]
        """
        

        self._channels = channels

    @property
    def created_date(self):
        """
        Gets the created_date of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.


        :return: The created_date of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.
        :rtype: datetime
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """
        Sets the created_date of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.


        :param created_date: The created_date of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.
        :type: datetime
        """
        

        self._created_date = created_date

    @property
    def action_map(self):
        """
        Gets the action_map of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.


        :return: The action_map of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.
        :rtype: JourneyOutcomeEventsNotificationActionMap
        """
        return self._action_map

    @action_map.setter
    def action_map(self, action_map):
        """
        Sets the action_map of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.


        :param action_map: The action_map of this JourneyOutcomeEventsNotificationOutcomeTouchpoint.
        :type: JourneyOutcomeEventsNotificationActionMap
        """
        

        self._action_map = action_map

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

