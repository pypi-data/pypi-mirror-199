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

class UserDevice(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        UserDevice - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'device_token': 'str',
            'notification_id': 'str',
            'make': 'str',
            'model': 'str',
            'accept_notifications': 'bool',
            'type': 'str',
            'session_hash': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'device_token': 'deviceToken',
            'notification_id': 'notificationId',
            'make': 'make',
            'model': 'model',
            'accept_notifications': 'acceptNotifications',
            'type': 'type',
            'session_hash': 'sessionHash',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._device_token = None
        self._notification_id = None
        self._make = None
        self._model = None
        self._accept_notifications = None
        self._type = None
        self._session_hash = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this UserDevice.
        The globally unique identifier for the object.

        :return: The id of this UserDevice.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this UserDevice.
        The globally unique identifier for the object.

        :param id: The id of this UserDevice.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this UserDevice.


        :return: The name of this UserDevice.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this UserDevice.


        :param name: The name of this UserDevice.
        :type: str
        """
        

        self._name = name

    @property
    def device_token(self):
        """
        Gets the device_token of this UserDevice.
        device token sent by mobile clients.

        :return: The device_token of this UserDevice.
        :rtype: str
        """
        return self._device_token

    @device_token.setter
    def device_token(self, device_token):
        """
        Sets the device_token of this UserDevice.
        device token sent by mobile clients.

        :param device_token: The device_token of this UserDevice.
        :type: str
        """
        

        self._device_token = device_token

    @property
    def notification_id(self):
        """
        Gets the notification_id of this UserDevice.
        notification id of the device.

        :return: The notification_id of this UserDevice.
        :rtype: str
        """
        return self._notification_id

    @notification_id.setter
    def notification_id(self, notification_id):
        """
        Sets the notification_id of this UserDevice.
        notification id of the device.

        :param notification_id: The notification_id of this UserDevice.
        :type: str
        """
        

        self._notification_id = notification_id

    @property
    def make(self):
        """
        Gets the make of this UserDevice.
        make of the device.

        :return: The make of this UserDevice.
        :rtype: str
        """
        return self._make

    @make.setter
    def make(self, make):
        """
        Sets the make of this UserDevice.
        make of the device.

        :param make: The make of this UserDevice.
        :type: str
        """
        

        self._make = make

    @property
    def model(self):
        """
        Gets the model of this UserDevice.
        Device model

        :return: The model of this UserDevice.
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model):
        """
        Sets the model of this UserDevice.
        Device model

        :param model: The model of this UserDevice.
        :type: str
        """
        

        self._model = model

    @property
    def accept_notifications(self):
        """
        Gets the accept_notifications of this UserDevice.
        if the device accepts notifications

        :return: The accept_notifications of this UserDevice.
        :rtype: bool
        """
        return self._accept_notifications

    @accept_notifications.setter
    def accept_notifications(self, accept_notifications):
        """
        Sets the accept_notifications of this UserDevice.
        if the device accepts notifications

        :param accept_notifications: The accept_notifications of this UserDevice.
        :type: bool
        """
        

        self._accept_notifications = accept_notifications

    @property
    def type(self):
        """
        Gets the type of this UserDevice.
        type of the device; ios or android

        :return: The type of this UserDevice.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this UserDevice.
        type of the device; ios or android

        :param type: The type of this UserDevice.
        :type: str
        """
        allowed_values = ["android", "ios"]
        if type.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for type -> " + type)
            self._type = "outdated_sdk_version"
        else:
            self._type = type

    @property
    def session_hash(self):
        """
        Gets the session_hash of this UserDevice.


        :return: The session_hash of this UserDevice.
        :rtype: str
        """
        return self._session_hash

    @session_hash.setter
    def session_hash(self, session_hash):
        """
        Sets the session_hash of this UserDevice.


        :param session_hash: The session_hash of this UserDevice.
        :type: str
        """
        

        self._session_hash = session_hash

    @property
    def self_uri(self):
        """
        Gets the self_uri of this UserDevice.
        The URI for this object

        :return: The self_uri of this UserDevice.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this UserDevice.
        The URI for this object

        :param self_uri: The self_uri of this UserDevice.
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

