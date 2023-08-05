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

class CoachingNotification(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CoachingNotification - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'marked_as_read': 'bool',
            'action_type': 'str',
            'relationship': 'str',
            'date_start': 'datetime',
            'length_in_minutes': 'int',
            'status': 'str',
            'user': 'UserReference',
            'appointment': 'CoachingAppointmentResponse',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'marked_as_read': 'markedAsRead',
            'action_type': 'actionType',
            'relationship': 'relationship',
            'date_start': 'dateStart',
            'length_in_minutes': 'lengthInMinutes',
            'status': 'status',
            'user': 'user',
            'appointment': 'appointment',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._marked_as_read = None
        self._action_type = None
        self._relationship = None
        self._date_start = None
        self._length_in_minutes = None
        self._status = None
        self._user = None
        self._appointment = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this CoachingNotification.
        The globally unique identifier for the object.

        :return: The id of this CoachingNotification.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this CoachingNotification.
        The globally unique identifier for the object.

        :param id: The id of this CoachingNotification.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this CoachingNotification.
        The name of the appointment for this notification.

        :return: The name of this CoachingNotification.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CoachingNotification.
        The name of the appointment for this notification.

        :param name: The name of this CoachingNotification.
        :type: str
        """
        

        self._name = name

    @property
    def marked_as_read(self):
        """
        Gets the marked_as_read of this CoachingNotification.
        Indicates if notification is read or unread

        :return: The marked_as_read of this CoachingNotification.
        :rtype: bool
        """
        return self._marked_as_read

    @marked_as_read.setter
    def marked_as_read(self, marked_as_read):
        """
        Sets the marked_as_read of this CoachingNotification.
        Indicates if notification is read or unread

        :param marked_as_read: The marked_as_read of this CoachingNotification.
        :type: bool
        """
        

        self._marked_as_read = marked_as_read

    @property
    def action_type(self):
        """
        Gets the action_type of this CoachingNotification.
        Action causing the notification.

        :return: The action_type of this CoachingNotification.
        :rtype: str
        """
        return self._action_type

    @action_type.setter
    def action_type(self, action_type):
        """
        Sets the action_type of this CoachingNotification.
        Action causing the notification.

        :param action_type: The action_type of this CoachingNotification.
        :type: str
        """
        allowed_values = ["Create", "Update", "Delete", "StatusChange"]
        if action_type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for action_type -> " + action_type)
            self._action_type = "outdated_sdk_version"
        else:
            self._action_type = action_type

    @property
    def relationship(self):
        """
        Gets the relationship of this CoachingNotification.
        The relationship of this user to this notification's appointment

        :return: The relationship of this CoachingNotification.
        :rtype: str
        """
        return self._relationship

    @relationship.setter
    def relationship(self, relationship):
        """
        Sets the relationship of this CoachingNotification.
        The relationship of this user to this notification's appointment

        :param relationship: The relationship of this CoachingNotification.
        :type: str
        """
        allowed_values = ["Attendee", "Creator", "Facilitator"]
        if relationship.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for relationship -> " + relationship)
            self._relationship = "outdated_sdk_version"
        else:
            self._relationship = relationship

    @property
    def date_start(self):
        """
        Gets the date_start of this CoachingNotification.
        The start time of the appointment relating to this notification. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_start of this CoachingNotification.
        :rtype: datetime
        """
        return self._date_start

    @date_start.setter
    def date_start(self, date_start):
        """
        Sets the date_start of this CoachingNotification.
        The start time of the appointment relating to this notification. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_start: The date_start of this CoachingNotification.
        :type: datetime
        """
        

        self._date_start = date_start

    @property
    def length_in_minutes(self):
        """
        Gets the length_in_minutes of this CoachingNotification.
        The duration of the appointment on this notification

        :return: The length_in_minutes of this CoachingNotification.
        :rtype: int
        """
        return self._length_in_minutes

    @length_in_minutes.setter
    def length_in_minutes(self, length_in_minutes):
        """
        Sets the length_in_minutes of this CoachingNotification.
        The duration of the appointment on this notification

        :param length_in_minutes: The length_in_minutes of this CoachingNotification.
        :type: int
        """
        

        self._length_in_minutes = length_in_minutes

    @property
    def status(self):
        """
        Gets the status of this CoachingNotification.
        The status of the appointment for this notification

        :return: The status of this CoachingNotification.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this CoachingNotification.
        The status of the appointment for this notification

        :param status: The status of this CoachingNotification.
        :type: str
        """
        allowed_values = ["Scheduled", "InProgress", "Completed", "InvalidSchedule"]
        if status.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for status -> " + status)
            self._status = "outdated_sdk_version"
        else:
            self._status = status

    @property
    def user(self):
        """
        Gets the user of this CoachingNotification.
        The user of this notification

        :return: The user of this CoachingNotification.
        :rtype: UserReference
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this CoachingNotification.
        The user of this notification

        :param user: The user of this CoachingNotification.
        :type: UserReference
        """
        

        self._user = user

    @property
    def appointment(self):
        """
        Gets the appointment of this CoachingNotification.
        The appointment

        :return: The appointment of this CoachingNotification.
        :rtype: CoachingAppointmentResponse
        """
        return self._appointment

    @appointment.setter
    def appointment(self, appointment):
        """
        Sets the appointment of this CoachingNotification.
        The appointment

        :param appointment: The appointment of this CoachingNotification.
        :type: CoachingAppointmentResponse
        """
        

        self._appointment = appointment

    @property
    def self_uri(self):
        """
        Gets the self_uri of this CoachingNotification.
        The URI for this object

        :return: The self_uri of this CoachingNotification.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this CoachingNotification.
        The URI for this object

        :param self_uri: The self_uri of this CoachingNotification.
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

