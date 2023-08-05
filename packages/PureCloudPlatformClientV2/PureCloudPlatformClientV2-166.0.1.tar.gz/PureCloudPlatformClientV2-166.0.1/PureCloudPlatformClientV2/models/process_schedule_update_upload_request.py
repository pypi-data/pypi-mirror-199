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

class ProcessScheduleUpdateUploadRequest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ProcessScheduleUpdateUploadRequest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'upload_key': 'str',
            'team_ids': 'list[str]',
            'management_unit_ids_for_added_team_users': 'list[str]'
        }

        self.attribute_map = {
            'upload_key': 'uploadKey',
            'team_ids': 'teamIds',
            'management_unit_ids_for_added_team_users': 'managementUnitIdsForAddedTeamUsers'
        }

        self._upload_key = None
        self._team_ids = None
        self._management_unit_ids_for_added_team_users = None

    @property
    def upload_key(self):
        """
        Gets the upload_key of this ProcessScheduleUpdateUploadRequest.
        The uploadKey provided by the request to get an upload URL

        :return: The upload_key of this ProcessScheduleUpdateUploadRequest.
        :rtype: str
        """
        return self._upload_key

    @upload_key.setter
    def upload_key(self, upload_key):
        """
        Sets the upload_key of this ProcessScheduleUpdateUploadRequest.
        The uploadKey provided by the request to get an upload URL

        :param upload_key: The upload_key of this ProcessScheduleUpdateUploadRequest.
        :type: str
        """
        

        self._upload_key = upload_key

    @property
    def team_ids(self):
        """
        Gets the team_ids of this ProcessScheduleUpdateUploadRequest.
        The list of teams to which the users being modified belong. Only required if the requesting user has conditional permission to wfm:schedule:edit

        :return: The team_ids of this ProcessScheduleUpdateUploadRequest.
        :rtype: list[str]
        """
        return self._team_ids

    @team_ids.setter
    def team_ids(self, team_ids):
        """
        Sets the team_ids of this ProcessScheduleUpdateUploadRequest.
        The list of teams to which the users being modified belong. Only required if the requesting user has conditional permission to wfm:schedule:edit

        :param team_ids: The team_ids of this ProcessScheduleUpdateUploadRequest.
        :type: list[str]
        """
        

        self._team_ids = team_ids

    @property
    def management_unit_ids_for_added_team_users(self):
        """
        Gets the management_unit_ids_for_added_team_users of this ProcessScheduleUpdateUploadRequest.
        The set of muIds to which agents belong if agents are being newly added to the schedule, if the requesting user has conditional permission to wfm:schedule:edit

        :return: The management_unit_ids_for_added_team_users of this ProcessScheduleUpdateUploadRequest.
        :rtype: list[str]
        """
        return self._management_unit_ids_for_added_team_users

    @management_unit_ids_for_added_team_users.setter
    def management_unit_ids_for_added_team_users(self, management_unit_ids_for_added_team_users):
        """
        Sets the management_unit_ids_for_added_team_users of this ProcessScheduleUpdateUploadRequest.
        The set of muIds to which agents belong if agents are being newly added to the schedule, if the requesting user has conditional permission to wfm:schedule:edit

        :param management_unit_ids_for_added_team_users: The management_unit_ids_for_added_team_users of this ProcessScheduleUpdateUploadRequest.
        :type: list[str]
        """
        

        self._management_unit_ids_for_added_team_users = management_unit_ids_for_added_team_users

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

