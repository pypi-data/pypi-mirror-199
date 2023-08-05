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

class WfmHistoricalAdherenceBulkResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WfmHistoricalAdherenceBulkResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'job': 'WfmHistoricalAdherenceBulkJobReference',
            'download_urls': 'list[str]',
            'download_result': 'WfmHistoricalAdherenceBulkResult'
        }

        self.attribute_map = {
            'job': 'job',
            'download_urls': 'downloadUrls',
            'download_result': 'downloadResult'
        }

        self._job = None
        self._download_urls = None
        self._download_result = None

    @property
    def job(self):
        """
        Gets the job of this WfmHistoricalAdherenceBulkResponse.
        A reference to the job that was started by the request

        :return: The job of this WfmHistoricalAdherenceBulkResponse.
        :rtype: WfmHistoricalAdherenceBulkJobReference
        """
        return self._job

    @job.setter
    def job(self, job):
        """
        Sets the job of this WfmHistoricalAdherenceBulkResponse.
        A reference to the job that was started by the request

        :param job: The job of this WfmHistoricalAdherenceBulkResponse.
        :type: WfmHistoricalAdherenceBulkJobReference
        """
        

        self._job = job

    @property
    def download_urls(self):
        """
        Gets the download_urls of this WfmHistoricalAdherenceBulkResponse.
        The uri list to GET the results of the Historical Adherence query. This field is populated only if query state is Complete

        :return: The download_urls of this WfmHistoricalAdherenceBulkResponse.
        :rtype: list[str]
        """
        return self._download_urls

    @download_urls.setter
    def download_urls(self, download_urls):
        """
        Sets the download_urls of this WfmHistoricalAdherenceBulkResponse.
        The uri list to GET the results of the Historical Adherence query. This field is populated only if query state is Complete

        :param download_urls: The download_urls of this WfmHistoricalAdherenceBulkResponse.
        :type: list[str]
        """
        

        self._download_urls = download_urls

    @property
    def download_result(self):
        """
        Gets the download_result of this WfmHistoricalAdherenceBulkResponse.
        Results will always come via downloadUrls; however the schema is included for documentation

        :return: The download_result of this WfmHistoricalAdherenceBulkResponse.
        :rtype: WfmHistoricalAdherenceBulkResult
        """
        return self._download_result

    @download_result.setter
    def download_result(self, download_result):
        """
        Sets the download_result of this WfmHistoricalAdherenceBulkResponse.
        Results will always come via downloadUrls; however the schema is included for documentation

        :param download_result: The download_result of this WfmHistoricalAdherenceBulkResponse.
        :type: WfmHistoricalAdherenceBulkResult
        """
        

        self._download_result = download_result

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

