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

class RecordingJob(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        RecordingJob - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'state': 'str',
            'recording_jobs_query': 'RecordingJobsQuery',
            'date_created': 'datetime',
            'total_conversations': 'int',
            'total_recordings': 'int',
            'total_skipped_recordings': 'int',
            'total_failed_recordings': 'int',
            'total_processed_recordings': 'int',
            'percent_progress': 'int',
            'error_message': 'str',
            'failed_recordings': 'str',
            'self_uri': 'str',
            'user': 'AddressableEntityRef'
        }

        self.attribute_map = {
            'id': 'id',
            'state': 'state',
            'recording_jobs_query': 'recordingJobsQuery',
            'date_created': 'dateCreated',
            'total_conversations': 'totalConversations',
            'total_recordings': 'totalRecordings',
            'total_skipped_recordings': 'totalSkippedRecordings',
            'total_failed_recordings': 'totalFailedRecordings',
            'total_processed_recordings': 'totalProcessedRecordings',
            'percent_progress': 'percentProgress',
            'error_message': 'errorMessage',
            'failed_recordings': 'failedRecordings',
            'self_uri': 'selfUri',
            'user': 'user'
        }

        self._id = None
        self._state = None
        self._recording_jobs_query = None
        self._date_created = None
        self._total_conversations = None
        self._total_recordings = None
        self._total_skipped_recordings = None
        self._total_failed_recordings = None
        self._total_processed_recordings = None
        self._percent_progress = None
        self._error_message = None
        self._failed_recordings = None
        self._self_uri = None
        self._user = None

    @property
    def id(self):
        """
        Gets the id of this RecordingJob.
        The globally unique identifier for the object.

        :return: The id of this RecordingJob.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this RecordingJob.
        The globally unique identifier for the object.

        :param id: The id of this RecordingJob.
        :type: str
        """
        

        self._id = id

    @property
    def state(self):
        """
        Gets the state of this RecordingJob.
        The current state of the job.

        :return: The state of this RecordingJob.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this RecordingJob.
        The current state of the job.

        :param state: The state of this RecordingJob.
        :type: str
        """
        allowed_values = ["FULFILLED", "PENDING", "READY", "PROCESSING", "CANCELLED", "FAILED"]
        if state.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for state -> " + state)
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def recording_jobs_query(self):
        """
        Gets the recording_jobs_query of this RecordingJob.
        Original query of the job.

        :return: The recording_jobs_query of this RecordingJob.
        :rtype: RecordingJobsQuery
        """
        return self._recording_jobs_query

    @recording_jobs_query.setter
    def recording_jobs_query(self, recording_jobs_query):
        """
        Sets the recording_jobs_query of this RecordingJob.
        Original query of the job.

        :param recording_jobs_query: The recording_jobs_query of this RecordingJob.
        :type: RecordingJobsQuery
        """
        

        self._recording_jobs_query = recording_jobs_query

    @property
    def date_created(self):
        """
        Gets the date_created of this RecordingJob.
        Date when the job was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_created of this RecordingJob.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this RecordingJob.
        Date when the job was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_created: The date_created of this RecordingJob.
        :type: datetime
        """
        

        self._date_created = date_created

    @property
    def total_conversations(self):
        """
        Gets the total_conversations of this RecordingJob.
        Total number of conversations affected.

        :return: The total_conversations of this RecordingJob.
        :rtype: int
        """
        return self._total_conversations

    @total_conversations.setter
    def total_conversations(self, total_conversations):
        """
        Sets the total_conversations of this RecordingJob.
        Total number of conversations affected.

        :param total_conversations: The total_conversations of this RecordingJob.
        :type: int
        """
        

        self._total_conversations = total_conversations

    @property
    def total_recordings(self):
        """
        Gets the total_recordings of this RecordingJob.
        Total number of recordings affected.

        :return: The total_recordings of this RecordingJob.
        :rtype: int
        """
        return self._total_recordings

    @total_recordings.setter
    def total_recordings(self, total_recordings):
        """
        Sets the total_recordings of this RecordingJob.
        Total number of recordings affected.

        :param total_recordings: The total_recordings of this RecordingJob.
        :type: int
        """
        

        self._total_recordings = total_recordings

    @property
    def total_skipped_recordings(self):
        """
        Gets the total_skipped_recordings of this RecordingJob.
        Total number of recordings that have been skipped.

        :return: The total_skipped_recordings of this RecordingJob.
        :rtype: int
        """
        return self._total_skipped_recordings

    @total_skipped_recordings.setter
    def total_skipped_recordings(self, total_skipped_recordings):
        """
        Sets the total_skipped_recordings of this RecordingJob.
        Total number of recordings that have been skipped.

        :param total_skipped_recordings: The total_skipped_recordings of this RecordingJob.
        :type: int
        """
        

        self._total_skipped_recordings = total_skipped_recordings

    @property
    def total_failed_recordings(self):
        """
        Gets the total_failed_recordings of this RecordingJob.
        Total number of recordings that the bulk job failed to process.

        :return: The total_failed_recordings of this RecordingJob.
        :rtype: int
        """
        return self._total_failed_recordings

    @total_failed_recordings.setter
    def total_failed_recordings(self, total_failed_recordings):
        """
        Sets the total_failed_recordings of this RecordingJob.
        Total number of recordings that the bulk job failed to process.

        :param total_failed_recordings: The total_failed_recordings of this RecordingJob.
        :type: int
        """
        

        self._total_failed_recordings = total_failed_recordings

    @property
    def total_processed_recordings(self):
        """
        Gets the total_processed_recordings of this RecordingJob.
        Total number of recordings have been processed.

        :return: The total_processed_recordings of this RecordingJob.
        :rtype: int
        """
        return self._total_processed_recordings

    @total_processed_recordings.setter
    def total_processed_recordings(self, total_processed_recordings):
        """
        Sets the total_processed_recordings of this RecordingJob.
        Total number of recordings have been processed.

        :param total_processed_recordings: The total_processed_recordings of this RecordingJob.
        :type: int
        """
        

        self._total_processed_recordings = total_processed_recordings

    @property
    def percent_progress(self):
        """
        Gets the percent_progress of this RecordingJob.
        Progress in percentage based on the number of recordings

        :return: The percent_progress of this RecordingJob.
        :rtype: int
        """
        return self._percent_progress

    @percent_progress.setter
    def percent_progress(self, percent_progress):
        """
        Sets the percent_progress of this RecordingJob.
        Progress in percentage based on the number of recordings

        :param percent_progress: The percent_progress of this RecordingJob.
        :type: int
        """
        

        self._percent_progress = percent_progress

    @property
    def error_message(self):
        """
        Gets the error_message of this RecordingJob.
        Error occurred during the job execution

        :return: The error_message of this RecordingJob.
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        """
        Sets the error_message of this RecordingJob.
        Error occurred during the job execution

        :param error_message: The error_message of this RecordingJob.
        :type: str
        """
        

        self._error_message = error_message

    @property
    def failed_recordings(self):
        """
        Gets the failed_recordings of this RecordingJob.
        Get IDs of recordings that the bulk job failed for

        :return: The failed_recordings of this RecordingJob.
        :rtype: str
        """
        return self._failed_recordings

    @failed_recordings.setter
    def failed_recordings(self, failed_recordings):
        """
        Sets the failed_recordings of this RecordingJob.
        Get IDs of recordings that the bulk job failed for

        :param failed_recordings: The failed_recordings of this RecordingJob.
        :type: str
        """
        

        self._failed_recordings = failed_recordings

    @property
    def self_uri(self):
        """
        Gets the self_uri of this RecordingJob.
        The URI for this object

        :return: The self_uri of this RecordingJob.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this RecordingJob.
        The URI for this object

        :param self_uri: The self_uri of this RecordingJob.
        :type: str
        """
        

        self._self_uri = self_uri

    @property
    def user(self):
        """
        Gets the user of this RecordingJob.
        Details of the user created the job

        :return: The user of this RecordingJob.
        :rtype: AddressableEntityRef
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        Sets the user of this RecordingJob.
        Details of the user created the job

        :param user: The user of this RecordingJob.
        :type: AddressableEntityRef
        """
        

        self._user = user

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

