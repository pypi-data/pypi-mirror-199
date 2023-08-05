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

class WorkitemsQueueEventsNotificationWorkitem(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WorkitemsQueueEventsNotificationWorkitem - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'type_id': 'str',
            'description': 'str',
            'language_id': 'str',
            'priority': 'int',
            'date_created': 'str',
            'date_modified': 'str',
            'date_due': 'str',
            'date_expires': 'str',
            'duration_seconds': 'int',
            'ttl': 'int',
            'status_id': 'str',
            'status_category': 'str',
            'date_closed': 'str',
            'workbin_id': 'str',
            'reporter_id': 'str',
            'assignee_id': 'str',
            'external_contact_id': 'str',
            'external_tag': 'str',
            'wrapup_id': 'str',
            'modified_by': 'str',
            'operation': 'str',
            'changes': 'list[WorkitemsQueueEventsNotificationDelta]',
            'assignment_state': 'str',
            'assignment_id': 'str',
            'alert_timeout_seconds': 'int',
            'queue_id': 'str',
            'custom_fields': 'dict(str, WorkitemsQueueEventsNotificationCustomAttribute)',
            'wrapup': 'WorkitemsQueueEventsNotificationWrapup'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'type_id': 'typeId',
            'description': 'description',
            'language_id': 'languageId',
            'priority': 'priority',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'date_due': 'dateDue',
            'date_expires': 'dateExpires',
            'duration_seconds': 'durationSeconds',
            'ttl': 'ttl',
            'status_id': 'statusId',
            'status_category': 'statusCategory',
            'date_closed': 'dateClosed',
            'workbin_id': 'workbinId',
            'reporter_id': 'reporterId',
            'assignee_id': 'assigneeId',
            'external_contact_id': 'externalContactId',
            'external_tag': 'externalTag',
            'wrapup_id': 'wrapupId',
            'modified_by': 'modifiedBy',
            'operation': 'operation',
            'changes': 'changes',
            'assignment_state': 'assignmentState',
            'assignment_id': 'assignmentId',
            'alert_timeout_seconds': 'alertTimeoutSeconds',
            'queue_id': 'queueId',
            'custom_fields': 'customFields',
            'wrapup': 'wrapup'
        }

        self._id = None
        self._name = None
        self._type_id = None
        self._description = None
        self._language_id = None
        self._priority = None
        self._date_created = None
        self._date_modified = None
        self._date_due = None
        self._date_expires = None
        self._duration_seconds = None
        self._ttl = None
        self._status_id = None
        self._status_category = None
        self._date_closed = None
        self._workbin_id = None
        self._reporter_id = None
        self._assignee_id = None
        self._external_contact_id = None
        self._external_tag = None
        self._wrapup_id = None
        self._modified_by = None
        self._operation = None
        self._changes = None
        self._assignment_state = None
        self._assignment_id = None
        self._alert_timeout_seconds = None
        self._queue_id = None
        self._custom_fields = None
        self._wrapup = None

    @property
    def id(self):
        """
        Gets the id of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The id of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WorkitemsQueueEventsNotificationWorkitem.


        :param id: The id of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The name of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this WorkitemsQueueEventsNotificationWorkitem.


        :param name: The name of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._name = name

    @property
    def type_id(self):
        """
        Gets the type_id of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The type_id of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._type_id

    @type_id.setter
    def type_id(self, type_id):
        """
        Sets the type_id of this WorkitemsQueueEventsNotificationWorkitem.


        :param type_id: The type_id of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._type_id = type_id

    @property
    def description(self):
        """
        Gets the description of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The description of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this WorkitemsQueueEventsNotificationWorkitem.


        :param description: The description of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._description = description

    @property
    def language_id(self):
        """
        Gets the language_id of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The language_id of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._language_id

    @language_id.setter
    def language_id(self, language_id):
        """
        Sets the language_id of this WorkitemsQueueEventsNotificationWorkitem.


        :param language_id: The language_id of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._language_id = language_id

    @property
    def priority(self):
        """
        Gets the priority of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The priority of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """
        Sets the priority of this WorkitemsQueueEventsNotificationWorkitem.


        :param priority: The priority of this WorkitemsQueueEventsNotificationWorkitem.
        :type: int
        """
        

        self._priority = priority

    @property
    def date_created(self):
        """
        Gets the date_created of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The date_created of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this WorkitemsQueueEventsNotificationWorkitem.


        :param date_created: The date_created of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The date_modified of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this WorkitemsQueueEventsNotificationWorkitem.


        :param date_modified: The date_modified of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._date_modified = date_modified

    @property
    def date_due(self):
        """
        Gets the date_due of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The date_due of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._date_due

    @date_due.setter
    def date_due(self, date_due):
        """
        Sets the date_due of this WorkitemsQueueEventsNotificationWorkitem.


        :param date_due: The date_due of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._date_due = date_due

    @property
    def date_expires(self):
        """
        Gets the date_expires of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The date_expires of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._date_expires

    @date_expires.setter
    def date_expires(self, date_expires):
        """
        Sets the date_expires of this WorkitemsQueueEventsNotificationWorkitem.


        :param date_expires: The date_expires of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._date_expires = date_expires

    @property
    def duration_seconds(self):
        """
        Gets the duration_seconds of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The duration_seconds of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: int
        """
        return self._duration_seconds

    @duration_seconds.setter
    def duration_seconds(self, duration_seconds):
        """
        Sets the duration_seconds of this WorkitemsQueueEventsNotificationWorkitem.


        :param duration_seconds: The duration_seconds of this WorkitemsQueueEventsNotificationWorkitem.
        :type: int
        """
        

        self._duration_seconds = duration_seconds

    @property
    def ttl(self):
        """
        Gets the ttl of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The ttl of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: int
        """
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        """
        Sets the ttl of this WorkitemsQueueEventsNotificationWorkitem.


        :param ttl: The ttl of this WorkitemsQueueEventsNotificationWorkitem.
        :type: int
        """
        

        self._ttl = ttl

    @property
    def status_id(self):
        """
        Gets the status_id of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The status_id of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._status_id

    @status_id.setter
    def status_id(self, status_id):
        """
        Sets the status_id of this WorkitemsQueueEventsNotificationWorkitem.


        :param status_id: The status_id of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._status_id = status_id

    @property
    def status_category(self):
        """
        Gets the status_category of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The status_category of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._status_category

    @status_category.setter
    def status_category(self, status_category):
        """
        Sets the status_category of this WorkitemsQueueEventsNotificationWorkitem.


        :param status_category: The status_category of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        allowed_values = ["Unknown", "Open", "InProgress", "Waiting", "Closed"]
        if status_category.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for status_category -> " + status_category)
            self._status_category = "outdated_sdk_version"
        else:
            self._status_category = status_category

    @property
    def date_closed(self):
        """
        Gets the date_closed of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The date_closed of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._date_closed

    @date_closed.setter
    def date_closed(self, date_closed):
        """
        Sets the date_closed of this WorkitemsQueueEventsNotificationWorkitem.


        :param date_closed: The date_closed of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._date_closed = date_closed

    @property
    def workbin_id(self):
        """
        Gets the workbin_id of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The workbin_id of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._workbin_id

    @workbin_id.setter
    def workbin_id(self, workbin_id):
        """
        Sets the workbin_id of this WorkitemsQueueEventsNotificationWorkitem.


        :param workbin_id: The workbin_id of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._workbin_id = workbin_id

    @property
    def reporter_id(self):
        """
        Gets the reporter_id of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The reporter_id of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._reporter_id

    @reporter_id.setter
    def reporter_id(self, reporter_id):
        """
        Sets the reporter_id of this WorkitemsQueueEventsNotificationWorkitem.


        :param reporter_id: The reporter_id of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._reporter_id = reporter_id

    @property
    def assignee_id(self):
        """
        Gets the assignee_id of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The assignee_id of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._assignee_id

    @assignee_id.setter
    def assignee_id(self, assignee_id):
        """
        Sets the assignee_id of this WorkitemsQueueEventsNotificationWorkitem.


        :param assignee_id: The assignee_id of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._assignee_id = assignee_id

    @property
    def external_contact_id(self):
        """
        Gets the external_contact_id of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The external_contact_id of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._external_contact_id

    @external_contact_id.setter
    def external_contact_id(self, external_contact_id):
        """
        Sets the external_contact_id of this WorkitemsQueueEventsNotificationWorkitem.


        :param external_contact_id: The external_contact_id of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._external_contact_id = external_contact_id

    @property
    def external_tag(self):
        """
        Gets the external_tag of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The external_tag of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._external_tag

    @external_tag.setter
    def external_tag(self, external_tag):
        """
        Sets the external_tag of this WorkitemsQueueEventsNotificationWorkitem.


        :param external_tag: The external_tag of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._external_tag = external_tag

    @property
    def wrapup_id(self):
        """
        Gets the wrapup_id of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The wrapup_id of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._wrapup_id

    @wrapup_id.setter
    def wrapup_id(self, wrapup_id):
        """
        Sets the wrapup_id of this WorkitemsQueueEventsNotificationWorkitem.


        :param wrapup_id: The wrapup_id of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._wrapup_id = wrapup_id

    @property
    def modified_by(self):
        """
        Gets the modified_by of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The modified_by of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """
        Sets the modified_by of this WorkitemsQueueEventsNotificationWorkitem.


        :param modified_by: The modified_by of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._modified_by = modified_by

    @property
    def operation(self):
        """
        Gets the operation of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The operation of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._operation

    @operation.setter
    def operation(self, operation):
        """
        Sets the operation of this WorkitemsQueueEventsNotificationWorkitem.


        :param operation: The operation of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        allowed_values = ["unknown", "add", "edit", "delete", "view", "upload", "download", "activate", "deactivate", "purge", "processed", "published", "assigned", "unassigned", "reset", "reassigned", "reassign", "archive", "unarchive", "reschedule"]
        if operation.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for operation -> " + operation)
            self._operation = "outdated_sdk_version"
        else:
            self._operation = operation

    @property
    def changes(self):
        """
        Gets the changes of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The changes of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: list[WorkitemsQueueEventsNotificationDelta]
        """
        return self._changes

    @changes.setter
    def changes(self, changes):
        """
        Sets the changes of this WorkitemsQueueEventsNotificationWorkitem.


        :param changes: The changes of this WorkitemsQueueEventsNotificationWorkitem.
        :type: list[WorkitemsQueueEventsNotificationDelta]
        """
        

        self._changes = changes

    @property
    def assignment_state(self):
        """
        Gets the assignment_state of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The assignment_state of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._assignment_state

    @assignment_state.setter
    def assignment_state(self, assignment_state):
        """
        Sets the assignment_state of this WorkitemsQueueEventsNotificationWorkitem.


        :param assignment_state: The assignment_state of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        allowed_values = ["Unknown", "Idle", "AcdStarted", "Alerting", "AlertTimeout", "Declined", "Connected", "Disconnected", "Parked", "Held", "AcdCancelled", "Terminated", "AcdExpired"]
        if assignment_state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for assignment_state -> " + assignment_state)
            self._assignment_state = "outdated_sdk_version"
        else:
            self._assignment_state = assignment_state

    @property
    def assignment_id(self):
        """
        Gets the assignment_id of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The assignment_id of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._assignment_id

    @assignment_id.setter
    def assignment_id(self, assignment_id):
        """
        Sets the assignment_id of this WorkitemsQueueEventsNotificationWorkitem.


        :param assignment_id: The assignment_id of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._assignment_id = assignment_id

    @property
    def alert_timeout_seconds(self):
        """
        Gets the alert_timeout_seconds of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The alert_timeout_seconds of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: int
        """
        return self._alert_timeout_seconds

    @alert_timeout_seconds.setter
    def alert_timeout_seconds(self, alert_timeout_seconds):
        """
        Sets the alert_timeout_seconds of this WorkitemsQueueEventsNotificationWorkitem.


        :param alert_timeout_seconds: The alert_timeout_seconds of this WorkitemsQueueEventsNotificationWorkitem.
        :type: int
        """
        

        self._alert_timeout_seconds = alert_timeout_seconds

    @property
    def queue_id(self):
        """
        Gets the queue_id of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The queue_id of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: str
        """
        return self._queue_id

    @queue_id.setter
    def queue_id(self, queue_id):
        """
        Sets the queue_id of this WorkitemsQueueEventsNotificationWorkitem.


        :param queue_id: The queue_id of this WorkitemsQueueEventsNotificationWorkitem.
        :type: str
        """
        

        self._queue_id = queue_id

    @property
    def custom_fields(self):
        """
        Gets the custom_fields of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The custom_fields of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: dict(str, WorkitemsQueueEventsNotificationCustomAttribute)
        """
        return self._custom_fields

    @custom_fields.setter
    def custom_fields(self, custom_fields):
        """
        Sets the custom_fields of this WorkitemsQueueEventsNotificationWorkitem.


        :param custom_fields: The custom_fields of this WorkitemsQueueEventsNotificationWorkitem.
        :type: dict(str, WorkitemsQueueEventsNotificationCustomAttribute)
        """
        

        self._custom_fields = custom_fields

    @property
    def wrapup(self):
        """
        Gets the wrapup of this WorkitemsQueueEventsNotificationWorkitem.


        :return: The wrapup of this WorkitemsQueueEventsNotificationWorkitem.
        :rtype: WorkitemsQueueEventsNotificationWrapup
        """
        return self._wrapup

    @wrapup.setter
    def wrapup(self, wrapup):
        """
        Sets the wrapup of this WorkitemsQueueEventsNotificationWorkitem.


        :param wrapup: The wrapup of this WorkitemsQueueEventsNotificationWorkitem.
        :type: WorkitemsQueueEventsNotificationWrapup
        """
        

        self._wrapup = wrapup

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

