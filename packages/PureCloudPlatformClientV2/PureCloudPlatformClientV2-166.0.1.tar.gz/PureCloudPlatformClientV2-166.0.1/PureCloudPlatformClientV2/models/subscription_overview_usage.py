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

class SubscriptionOverviewUsage(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        SubscriptionOverviewUsage - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'part_number': 'str',
            'grouping': 'str',
            'unit_of_measure_type': 'str',
            'usage_quantity': 'str',
            'overage_price': 'str',
            'prepay_quantity': 'str',
            'prepay_price': 'str',
            'usage_notes': 'str',
            'is_cancellable': 'bool',
            'bundle_quantity': 'str',
            'is_third_party': 'bool'
        }

        self.attribute_map = {
            'name': 'name',
            'part_number': 'partNumber',
            'grouping': 'grouping',
            'unit_of_measure_type': 'unitOfMeasureType',
            'usage_quantity': 'usageQuantity',
            'overage_price': 'overagePrice',
            'prepay_quantity': 'prepayQuantity',
            'prepay_price': 'prepayPrice',
            'usage_notes': 'usageNotes',
            'is_cancellable': 'isCancellable',
            'bundle_quantity': 'bundleQuantity',
            'is_third_party': 'isThirdParty'
        }

        self._name = None
        self._part_number = None
        self._grouping = None
        self._unit_of_measure_type = None
        self._usage_quantity = None
        self._overage_price = None
        self._prepay_quantity = None
        self._prepay_price = None
        self._usage_notes = None
        self._is_cancellable = None
        self._bundle_quantity = None
        self._is_third_party = None

    @property
    def name(self):
        """
        Gets the name of this SubscriptionOverviewUsage.
        Product charge name

        :return: The name of this SubscriptionOverviewUsage.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this SubscriptionOverviewUsage.
        Product charge name

        :param name: The name of this SubscriptionOverviewUsage.
        :type: str
        """
        

        self._name = name

    @property
    def part_number(self):
        """
        Gets the part_number of this SubscriptionOverviewUsage.
        Product part number

        :return: The part_number of this SubscriptionOverviewUsage.
        :rtype: str
        """
        return self._part_number

    @part_number.setter
    def part_number(self, part_number):
        """
        Sets the part_number of this SubscriptionOverviewUsage.
        Product part number

        :param part_number: The part_number of this SubscriptionOverviewUsage.
        :type: str
        """
        

        self._part_number = part_number

    @property
    def grouping(self):
        """
        Gets the grouping of this SubscriptionOverviewUsage.
        UI grouping key

        :return: The grouping of this SubscriptionOverviewUsage.
        :rtype: str
        """
        return self._grouping

    @grouping.setter
    def grouping(self, grouping):
        """
        Sets the grouping of this SubscriptionOverviewUsage.
        UI grouping key

        :param grouping: The grouping of this SubscriptionOverviewUsage.
        :type: str
        """
        

        self._grouping = grouping

    @property
    def unit_of_measure_type(self):
        """
        Gets the unit_of_measure_type of this SubscriptionOverviewUsage.
        UI unit of measure

        :return: The unit_of_measure_type of this SubscriptionOverviewUsage.
        :rtype: str
        """
        return self._unit_of_measure_type

    @unit_of_measure_type.setter
    def unit_of_measure_type(self, unit_of_measure_type):
        """
        Sets the unit_of_measure_type of this SubscriptionOverviewUsage.
        UI unit of measure

        :param unit_of_measure_type: The unit_of_measure_type of this SubscriptionOverviewUsage.
        :type: str
        """
        

        self._unit_of_measure_type = unit_of_measure_type

    @property
    def usage_quantity(self):
        """
        Gets the usage_quantity of this SubscriptionOverviewUsage.
        Usage count for specified period

        :return: The usage_quantity of this SubscriptionOverviewUsage.
        :rtype: str
        """
        return self._usage_quantity

    @usage_quantity.setter
    def usage_quantity(self, usage_quantity):
        """
        Sets the usage_quantity of this SubscriptionOverviewUsage.
        Usage count for specified period

        :param usage_quantity: The usage_quantity of this SubscriptionOverviewUsage.
        :type: str
        """
        

        self._usage_quantity = usage_quantity

    @property
    def overage_price(self):
        """
        Gets the overage_price of this SubscriptionOverviewUsage.
        Price for usage / overage charge

        :return: The overage_price of this SubscriptionOverviewUsage.
        :rtype: str
        """
        return self._overage_price

    @overage_price.setter
    def overage_price(self, overage_price):
        """
        Sets the overage_price of this SubscriptionOverviewUsage.
        Price for usage / overage charge

        :param overage_price: The overage_price of this SubscriptionOverviewUsage.
        :type: str
        """
        

        self._overage_price = overage_price

    @property
    def prepay_quantity(self):
        """
        Gets the prepay_quantity of this SubscriptionOverviewUsage.
        Items prepaid for specified period

        :return: The prepay_quantity of this SubscriptionOverviewUsage.
        :rtype: str
        """
        return self._prepay_quantity

    @prepay_quantity.setter
    def prepay_quantity(self, prepay_quantity):
        """
        Sets the prepay_quantity of this SubscriptionOverviewUsage.
        Items prepaid for specified period

        :param prepay_quantity: The prepay_quantity of this SubscriptionOverviewUsage.
        :type: str
        """
        

        self._prepay_quantity = prepay_quantity

    @property
    def prepay_price(self):
        """
        Gets the prepay_price of this SubscriptionOverviewUsage.
        Price for prepay charge

        :return: The prepay_price of this SubscriptionOverviewUsage.
        :rtype: str
        """
        return self._prepay_price

    @prepay_price.setter
    def prepay_price(self, prepay_price):
        """
        Sets the prepay_price of this SubscriptionOverviewUsage.
        Price for prepay charge

        :param prepay_price: The prepay_price of this SubscriptionOverviewUsage.
        :type: str
        """
        

        self._prepay_price = prepay_price

    @property
    def usage_notes(self):
        """
        Gets the usage_notes of this SubscriptionOverviewUsage.
        Notes about the usage/charge item

        :return: The usage_notes of this SubscriptionOverviewUsage.
        :rtype: str
        """
        return self._usage_notes

    @usage_notes.setter
    def usage_notes(self, usage_notes):
        """
        Sets the usage_notes of this SubscriptionOverviewUsage.
        Notes about the usage/charge item

        :param usage_notes: The usage_notes of this SubscriptionOverviewUsage.
        :type: str
        """
        

        self._usage_notes = usage_notes

    @property
    def is_cancellable(self):
        """
        Gets the is_cancellable of this SubscriptionOverviewUsage.
        Indicates whether the item is cancellable

        :return: The is_cancellable of this SubscriptionOverviewUsage.
        :rtype: bool
        """
        return self._is_cancellable

    @is_cancellable.setter
    def is_cancellable(self, is_cancellable):
        """
        Sets the is_cancellable of this SubscriptionOverviewUsage.
        Indicates whether the item is cancellable

        :param is_cancellable: The is_cancellable of this SubscriptionOverviewUsage.
        :type: bool
        """
        

        self._is_cancellable = is_cancellable

    @property
    def bundle_quantity(self):
        """
        Gets the bundle_quantity of this SubscriptionOverviewUsage.
        Quantity multiplier for this charge

        :return: The bundle_quantity of this SubscriptionOverviewUsage.
        :rtype: str
        """
        return self._bundle_quantity

    @bundle_quantity.setter
    def bundle_quantity(self, bundle_quantity):
        """
        Sets the bundle_quantity of this SubscriptionOverviewUsage.
        Quantity multiplier for this charge

        :param bundle_quantity: The bundle_quantity of this SubscriptionOverviewUsage.
        :type: str
        """
        

        self._bundle_quantity = bundle_quantity

    @property
    def is_third_party(self):
        """
        Gets the is_third_party of this SubscriptionOverviewUsage.
        A charge from a third party entity

        :return: The is_third_party of this SubscriptionOverviewUsage.
        :rtype: bool
        """
        return self._is_third_party

    @is_third_party.setter
    def is_third_party(self, is_third_party):
        """
        Sets the is_third_party of this SubscriptionOverviewUsage.
        A charge from a third party entity

        :param is_third_party: The is_third_party of this SubscriptionOverviewUsage.
        :type: bool
        """
        

        self._is_third_party = is_third_party

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

