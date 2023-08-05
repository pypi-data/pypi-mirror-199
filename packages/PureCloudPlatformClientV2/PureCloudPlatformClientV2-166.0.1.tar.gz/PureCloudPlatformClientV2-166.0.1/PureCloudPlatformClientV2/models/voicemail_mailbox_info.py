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

class VoicemailMailboxInfo(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        VoicemailMailboxInfo - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'usage_size_bytes': 'int',
            'total_count': 'int',
            'unread_count': 'int',
            'deleted_count': 'int',
            'created_date': 'datetime',
            'modified_date': 'datetime'
        }

        self.attribute_map = {
            'usage_size_bytes': 'usageSizeBytes',
            'total_count': 'totalCount',
            'unread_count': 'unreadCount',
            'deleted_count': 'deletedCount',
            'created_date': 'createdDate',
            'modified_date': 'modifiedDate'
        }

        self._usage_size_bytes = None
        self._total_count = None
        self._unread_count = None
        self._deleted_count = None
        self._created_date = None
        self._modified_date = None

    @property
    def usage_size_bytes(self):
        """
        Gets the usage_size_bytes of this VoicemailMailboxInfo.
        The total number of bytes for all voicemail message audio recordings

        :return: The usage_size_bytes of this VoicemailMailboxInfo.
        :rtype: int
        """
        return self._usage_size_bytes

    @usage_size_bytes.setter
    def usage_size_bytes(self, usage_size_bytes):
        """
        Sets the usage_size_bytes of this VoicemailMailboxInfo.
        The total number of bytes for all voicemail message audio recordings

        :param usage_size_bytes: The usage_size_bytes of this VoicemailMailboxInfo.
        :type: int
        """
        

        self._usage_size_bytes = usage_size_bytes

    @property
    def total_count(self):
        """
        Gets the total_count of this VoicemailMailboxInfo.
        The total number of voicemail messages

        :return: The total_count of this VoicemailMailboxInfo.
        :rtype: int
        """
        return self._total_count

    @total_count.setter
    def total_count(self, total_count):
        """
        Sets the total_count of this VoicemailMailboxInfo.
        The total number of voicemail messages

        :param total_count: The total_count of this VoicemailMailboxInfo.
        :type: int
        """
        

        self._total_count = total_count

    @property
    def unread_count(self):
        """
        Gets the unread_count of this VoicemailMailboxInfo.
        The total number of voicemail messages marked as unread

        :return: The unread_count of this VoicemailMailboxInfo.
        :rtype: int
        """
        return self._unread_count

    @unread_count.setter
    def unread_count(self, unread_count):
        """
        Sets the unread_count of this VoicemailMailboxInfo.
        The total number of voicemail messages marked as unread

        :param unread_count: The unread_count of this VoicemailMailboxInfo.
        :type: int
        """
        

        self._unread_count = unread_count

    @property
    def deleted_count(self):
        """
        Gets the deleted_count of this VoicemailMailboxInfo.
        The total number of voicemail messages marked as deleted

        :return: The deleted_count of this VoicemailMailboxInfo.
        :rtype: int
        """
        return self._deleted_count

    @deleted_count.setter
    def deleted_count(self, deleted_count):
        """
        Sets the deleted_count of this VoicemailMailboxInfo.
        The total number of voicemail messages marked as deleted

        :param deleted_count: The deleted_count of this VoicemailMailboxInfo.
        :type: int
        """
        

        self._deleted_count = deleted_count

    @property
    def created_date(self):
        """
        Gets the created_date of this VoicemailMailboxInfo.
        The date of the oldest voicemail message. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The created_date of this VoicemailMailboxInfo.
        :rtype: datetime
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """
        Sets the created_date of this VoicemailMailboxInfo.
        The date of the oldest voicemail message. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param created_date: The created_date of this VoicemailMailboxInfo.
        :type: datetime
        """
        

        self._created_date = created_date

    @property
    def modified_date(self):
        """
        Gets the modified_date of this VoicemailMailboxInfo.
        The date of the most recent voicemail message. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The modified_date of this VoicemailMailboxInfo.
        :rtype: datetime
        """
        return self._modified_date

    @modified_date.setter
    def modified_date(self, modified_date):
        """
        Sets the modified_date of this VoicemailMailboxInfo.
        The date of the most recent voicemail message. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param modified_date: The modified_date of this VoicemailMailboxInfo.
        :type: datetime
        """
        

        self._modified_date = modified_date

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

