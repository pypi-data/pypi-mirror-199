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

class TrustCreate(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        TrustCreate - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'pairing_id': 'str',
            'enabled': 'bool',
            'users': 'list[TrustMemberCreate]',
            'groups': 'list[TrustMemberCreate]',
            'date_expired': 'datetime'
        }

        self.attribute_map = {
            'pairing_id': 'pairingId',
            'enabled': 'enabled',
            'users': 'users',
            'groups': 'groups',
            'date_expired': 'dateExpired'
        }

        self._pairing_id = None
        self._enabled = None
        self._users = None
        self._groups = None
        self._date_expired = None

    @property
    def pairing_id(self):
        """
        Gets the pairing_id of this TrustCreate.
        The pairing Id created by the trustee. This is required to prove that the trustee agrees to the relationship.  Not required when creating a default pairing with Customer Care.

        :return: The pairing_id of this TrustCreate.
        :rtype: str
        """
        return self._pairing_id

    @pairing_id.setter
    def pairing_id(self, pairing_id):
        """
        Sets the pairing_id of this TrustCreate.
        The pairing Id created by the trustee. This is required to prove that the trustee agrees to the relationship.  Not required when creating a default pairing with Customer Care.

        :param pairing_id: The pairing_id of this TrustCreate.
        :type: str
        """
        

        self._pairing_id = pairing_id

    @property
    def enabled(self):
        """
        Gets the enabled of this TrustCreate.
        If disabled no trustee user will have access, even if they were previously added.

        :return: The enabled of this TrustCreate.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this TrustCreate.
        If disabled no trustee user will have access, even if they were previously added.

        :param enabled: The enabled of this TrustCreate.
        :type: bool
        """
        

        self._enabled = enabled

    @property
    def users(self):
        """
        Gets the users of this TrustCreate.
        The list of users and their roles to which access will be granted. The users are from the trustee and the roles are from the trustor. If no users are specified, at least one group is required.

        :return: The users of this TrustCreate.
        :rtype: list[TrustMemberCreate]
        """
        return self._users

    @users.setter
    def users(self, users):
        """
        Sets the users of this TrustCreate.
        The list of users and their roles to which access will be granted. The users are from the trustee and the roles are from the trustor. If no users are specified, at least one group is required.

        :param users: The users of this TrustCreate.
        :type: list[TrustMemberCreate]
        """
        

        self._users = users

    @property
    def groups(self):
        """
        Gets the groups of this TrustCreate.
        The list of groups and their roles to which access will be granted. The groups are from the trustee and the roles are from the trustor. If no groups are specified, at least one user is required.

        :return: The groups of this TrustCreate.
        :rtype: list[TrustMemberCreate]
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """
        Sets the groups of this TrustCreate.
        The list of groups and their roles to which access will be granted. The groups are from the trustee and the roles are from the trustor. If no groups are specified, at least one user is required.

        :param groups: The groups of this TrustCreate.
        :type: list[TrustMemberCreate]
        """
        

        self._groups = groups

    @property
    def date_expired(self):
        """
        Gets the date_expired of this TrustCreate.
        The expiration date of the trust. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_expired of this TrustCreate.
        :rtype: datetime
        """
        return self._date_expired

    @date_expired.setter
    def date_expired(self, date_expired):
        """
        Sets the date_expired of this TrustCreate.
        The expiration date of the trust. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_expired: The date_expired of this TrustCreate.
        :type: datetime
        """
        

        self._date_expired = date_expired

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

