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

class Assignment(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Assignment - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'assigned_members': 'list[UserReference]',
            'removed_members': 'list[UserReference]',
            'assignment_errors': 'list[AssignmentError]'
        }

        self.attribute_map = {
            'assigned_members': 'assignedMembers',
            'removed_members': 'removedMembers',
            'assignment_errors': 'assignmentErrors'
        }

        self._assigned_members = None
        self._removed_members = None
        self._assignment_errors = None

    @property
    def assigned_members(self):
        """
        Gets the assigned_members of this Assignment.
        The list of users successfully assigned to the custom performance profile

        :return: The assigned_members of this Assignment.
        :rtype: list[UserReference]
        """
        return self._assigned_members

    @assigned_members.setter
    def assigned_members(self, assigned_members):
        """
        Sets the assigned_members of this Assignment.
        The list of users successfully assigned to the custom performance profile

        :param assigned_members: The assigned_members of this Assignment.
        :type: list[UserReference]
        """
        

        self._assigned_members = assigned_members

    @property
    def removed_members(self):
        """
        Gets the removed_members of this Assignment.
        The list of users successfully removed from the custom performance profile

        :return: The removed_members of this Assignment.
        :rtype: list[UserReference]
        """
        return self._removed_members

    @removed_members.setter
    def removed_members(self, removed_members):
        """
        Sets the removed_members of this Assignment.
        The list of users successfully removed from the custom performance profile

        :param removed_members: The removed_members of this Assignment.
        :type: list[UserReference]
        """
        

        self._removed_members = removed_members

    @property
    def assignment_errors(self):
        """
        Gets the assignment_errors of this Assignment.
        The list of users failed assignment or removal for the custom performance profile

        :return: The assignment_errors of this Assignment.
        :rtype: list[AssignmentError]
        """
        return self._assignment_errors

    @assignment_errors.setter
    def assignment_errors(self, assignment_errors):
        """
        Sets the assignment_errors of this Assignment.
        The list of users failed assignment or removal for the custom performance profile

        :param assignment_errors: The assignment_errors of this Assignment.
        :type: list[AssignmentError]
        """
        

        self._assignment_errors = assignment_errors

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

