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

class WebMessagingEvent(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WebMessagingEvent - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'event_type': 'str',
            'co_browse': 'WebMessagingEventCoBrowse',
            'presence': 'WebMessagingEventPresence'
        }

        self.attribute_map = {
            'event_type': 'eventType',
            'co_browse': 'coBrowse',
            'presence': 'presence'
        }

        self._event_type = None
        self._co_browse = None
        self._presence = None

    @property
    def event_type(self):
        """
        Gets the event_type of this WebMessagingEvent.
        Type of this event element

        :return: The event_type of this WebMessagingEvent.
        :rtype: str
        """
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        """
        Sets the event_type of this WebMessagingEvent.
        Type of this event element

        :param event_type: The event_type of this WebMessagingEvent.
        :type: str
        """
        allowed_values = ["CoBrowse", "Presence"]
        if event_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for event_type -> " + event_type)
            self._event_type = "outdated_sdk_version"
        else:
            self._event_type = event_type

    @property
    def co_browse(self):
        """
        Gets the co_browse of this WebMessagingEvent.
        Cobrowse event.

        :return: The co_browse of this WebMessagingEvent.
        :rtype: WebMessagingEventCoBrowse
        """
        return self._co_browse

    @co_browse.setter
    def co_browse(self, co_browse):
        """
        Sets the co_browse of this WebMessagingEvent.
        Cobrowse event.

        :param co_browse: The co_browse of this WebMessagingEvent.
        :type: WebMessagingEventCoBrowse
        """
        

        self._co_browse = co_browse

    @property
    def presence(self):
        """
        Gets the presence of this WebMessagingEvent.
        Presence event.

        :return: The presence of this WebMessagingEvent.
        :rtype: WebMessagingEventPresence
        """
        return self._presence

    @presence.setter
    def presence(self, presence):
        """
        Sets the presence of this WebMessagingEvent.
        Presence event.

        :param presence: The presence of this WebMessagingEvent.
        :type: WebMessagingEventPresence
        """
        

        self._presence = presence

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

