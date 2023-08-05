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

class LeaderboardItem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        LeaderboardItem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'user': 'UserReference',
            'rank': 'int',
            'points': 'int'
        }

        self.attribute_map = {
            'user': 'user',
            'rank': 'rank',
            'points': 'points'
        }

        self._user = None
        self._rank = None
        self._points = None

    @property
    def user(self):
        """
        Gets the user of this LeaderboardItem.
        The user object for this leaderboard rank

        :return: The user of this LeaderboardItem.
        :rtype: UserReference
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this LeaderboardItem.
        The user object for this leaderboard rank

        :param user: The user of this LeaderboardItem.
        :type: UserReference
        """
        

        self._user = user

    @property
    def rank(self):
        """
        Gets the rank of this LeaderboardItem.
        The rank of the user

        :return: The rank of this LeaderboardItem.
        :rtype: int
        """
        return self._rank

    @rank.setter
    def rank(self, rank):
        """
        Sets the rank of this LeaderboardItem.
        The rank of the user

        :param rank: The rank of this LeaderboardItem.
        :type: int
        """
        

        self._rank = rank

    @property
    def points(self):
        """
        Gets the points of this LeaderboardItem.
        The points collected by the user

        :return: The points of this LeaderboardItem.
        :rtype: int
        """
        return self._points

    @points.setter
    def points(self, points):
        """
        Sets the points of this LeaderboardItem.
        The points collected by the user

        :param points: The points of this LeaderboardItem.
        :type: int
        """
        

        self._points = points

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

