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

class WebDeployment(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        WebDeployment - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'description': 'str',
            'allow_all_domains': 'bool',
            'allowed_domains': 'list[str]',
            'snippet': 'str',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'last_modified_user': 'AddressableEntityRef',
            'flow': 'DomainEntityRef',
            'status': 'str',
            'configuration': 'WebDeploymentConfigurationVersionEntityRef',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'allow_all_domains': 'allowAllDomains',
            'allowed_domains': 'allowedDomains',
            'snippet': 'snippet',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'last_modified_user': 'lastModifiedUser',
            'flow': 'flow',
            'status': 'status',
            'configuration': 'configuration',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._description = None
        self._allow_all_domains = None
        self._allowed_domains = None
        self._snippet = None
        self._date_created = None
        self._date_modified = None
        self._last_modified_user = None
        self._flow = None
        self._status = None
        self._configuration = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this WebDeployment.
        The deployment ID

        :return: The id of this WebDeployment.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this WebDeployment.
        The deployment ID

        :param id: The id of this WebDeployment.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this WebDeployment.
        The deployment name

        :return: The name of this WebDeployment.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this WebDeployment.
        The deployment name

        :param name: The name of this WebDeployment.
        :type: str
        """
        

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this WebDeployment.
        The description of the config

        :return: The description of this WebDeployment.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this WebDeployment.
        The description of the config

        :param description: The description of this WebDeployment.
        :type: str
        """
        

        self._description = description

    @property
    def allow_all_domains(self):
        """
        Gets the allow_all_domains of this WebDeployment.
        Property indicates whether all domains are allowed or not. allowedDomains must be empty when this is set as true.

        :return: The allow_all_domains of this WebDeployment.
        :rtype: bool
        """
        return self._allow_all_domains

    @allow_all_domains.setter
    def allow_all_domains(self, allow_all_domains):
        """
        Sets the allow_all_domains of this WebDeployment.
        Property indicates whether all domains are allowed or not. allowedDomains must be empty when this is set as true.

        :param allow_all_domains: The allow_all_domains of this WebDeployment.
        :type: bool
        """
        

        self._allow_all_domains = allow_all_domains

    @property
    def allowed_domains(self):
        """
        Gets the allowed_domains of this WebDeployment.
        The list of domains that are approved to use this deployment; the list will be added to CORS headers for ease of web use.

        :return: The allowed_domains of this WebDeployment.
        :rtype: list[str]
        """
        return self._allowed_domains

    @allowed_domains.setter
    def allowed_domains(self, allowed_domains):
        """
        Sets the allowed_domains of this WebDeployment.
        The list of domains that are approved to use this deployment; the list will be added to CORS headers for ease of web use.

        :param allowed_domains: The allowed_domains of this WebDeployment.
        :type: list[str]
        """
        

        self._allowed_domains = allowed_domains

    @property
    def snippet(self):
        """
        Gets the snippet of this WebDeployment.
        Javascript snippet used to load the config

        :return: The snippet of this WebDeployment.
        :rtype: str
        """
        return self._snippet

    @snippet.setter
    def snippet(self, snippet):
        """
        Sets the snippet of this WebDeployment.
        Javascript snippet used to load the config

        :param snippet: The snippet of this WebDeployment.
        :type: str
        """
        

        self._snippet = snippet

    @property
    def date_created(self):
        """
        Gets the date_created of this WebDeployment.
        The date the deployment was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_created of this WebDeployment.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this WebDeployment.
        The date the deployment was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_created: The date_created of this WebDeployment.
        :type: datetime
        """
        

        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this WebDeployment.
        The date the deployment was most recently modified. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :return: The date_modified of this WebDeployment.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this WebDeployment.
        The date the deployment was most recently modified. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss[.mmm]Z

        :param date_modified: The date_modified of this WebDeployment.
        :type: datetime
        """
        

        self._date_modified = date_modified

    @property
    def last_modified_user(self):
        """
        Gets the last_modified_user of this WebDeployment.
        A reference to the user who most recently modified the deployment

        :return: The last_modified_user of this WebDeployment.
        :rtype: AddressableEntityRef
        """
        return self._last_modified_user

    @last_modified_user.setter
    def last_modified_user(self, last_modified_user):
        """
        Sets the last_modified_user of this WebDeployment.
        A reference to the user who most recently modified the deployment

        :param last_modified_user: The last_modified_user of this WebDeployment.
        :type: AddressableEntityRef
        """
        

        self._last_modified_user = last_modified_user

    @property
    def flow(self):
        """
        Gets the flow of this WebDeployment.
        A reference to the inboundshortmessage flow used by this deployment

        :return: The flow of this WebDeployment.
        :rtype: DomainEntityRef
        """
        return self._flow

    @flow.setter
    def flow(self, flow):
        """
        Sets the flow of this WebDeployment.
        A reference to the inboundshortmessage flow used by this deployment

        :param flow: The flow of this WebDeployment.
        :type: DomainEntityRef
        """
        

        self._flow = flow

    @property
    def status(self):
        """
        Gets the status of this WebDeployment.
        The current status of the deployment

        :return: The status of this WebDeployment.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this WebDeployment.
        The current status of the deployment

        :param status: The status of this WebDeployment.
        :type: str
        """
        allowed_values = ["Pending", "Active", "Inactive", "Error", "Deleting"]
        if status.lower() not in map(str.lower, allowed_values):
            # print("Invalid value for status -> " + status)
            self._status = "outdated_sdk_version"
        else:
            self._status = status

    @property
    def configuration(self):
        """
        Gets the configuration of this WebDeployment.
        The config version this deployment uses

        :return: The configuration of this WebDeployment.
        :rtype: WebDeploymentConfigurationVersionEntityRef
        """
        return self._configuration

    @configuration.setter
    def configuration(self, configuration):
        """
        Sets the configuration of this WebDeployment.
        The config version this deployment uses

        :param configuration: The configuration of this WebDeployment.
        :type: WebDeploymentConfigurationVersionEntityRef
        """
        

        self._configuration = configuration

    @property
    def self_uri(self):
        """
        Gets the self_uri of this WebDeployment.
        The URI for this object

        :return: The self_uri of this WebDeployment.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this WebDeployment.
        The URI for this object

        :param self_uri: The self_uri of this WebDeployment.
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

