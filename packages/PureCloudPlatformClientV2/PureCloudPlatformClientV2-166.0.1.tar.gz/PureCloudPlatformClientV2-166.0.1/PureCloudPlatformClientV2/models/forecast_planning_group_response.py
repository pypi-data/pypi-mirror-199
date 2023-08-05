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

class ForecastPlanningGroupResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ForecastPlanningGroupResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'route_paths': 'list[RoutePathResponse]',
            'service_goal_template': 'ForecastServiceGoalTemplateResponse'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'route_paths': 'routePaths',
            'service_goal_template': 'serviceGoalTemplate'
        }

        self._id = None
        self._name = None
        self._route_paths = None
        self._service_goal_template = None

    @property
    def id(self):
        """
        Gets the id of this ForecastPlanningGroupResponse.
        The ID of the planning group

        :return: The id of this ForecastPlanningGroupResponse.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ForecastPlanningGroupResponse.
        The ID of the planning group

        :param id: The id of this ForecastPlanningGroupResponse.
        :type: str
        """
        

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ForecastPlanningGroupResponse.
        The name of the planning group

        :return: The name of this ForecastPlanningGroupResponse.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ForecastPlanningGroupResponse.
        The name of the planning group

        :param name: The name of this ForecastPlanningGroupResponse.
        :type: str
        """
        

        self._name = name

    @property
    def route_paths(self):
        """
        Gets the route_paths of this ForecastPlanningGroupResponse.
        Route path configuration for this planning group

        :return: The route_paths of this ForecastPlanningGroupResponse.
        :rtype: list[RoutePathResponse]
        """
        return self._route_paths

    @route_paths.setter
    def route_paths(self, route_paths):
        """
        Sets the route_paths of this ForecastPlanningGroupResponse.
        Route path configuration for this planning group

        :param route_paths: The route_paths of this ForecastPlanningGroupResponse.
        :type: list[RoutePathResponse]
        """
        

        self._route_paths = route_paths

    @property
    def service_goal_template(self):
        """
        Gets the service_goal_template of this ForecastPlanningGroupResponse.
        Service goals for this planning group

        :return: The service_goal_template of this ForecastPlanningGroupResponse.
        :rtype: ForecastServiceGoalTemplateResponse
        """
        return self._service_goal_template

    @service_goal_template.setter
    def service_goal_template(self, service_goal_template):
        """
        Sets the service_goal_template of this ForecastPlanningGroupResponse.
        Service goals for this planning group

        :param service_goal_template: The service_goal_template of this ForecastPlanningGroupResponse.
        :type: ForecastServiceGoalTemplateResponse
        """
        

        self._service_goal_template = service_goal_template

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

