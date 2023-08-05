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

class DigitalAction(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DigitalAction - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'update_contact_column_action_settings': 'UpdateContactColumnActionSettings',
            'do_not_send_action_settings': 'object',
            'append_to_dnc_action_settings': 'AppendToDncActionSettings',
            'mark_contact_uncontactable_action_settings': 'MarkContactUncontactableActionSettings',
            'mark_contact_address_uncontactable_action_settings': 'object',
            'set_content_template_action_settings': 'SetContentTemplateActionSettings'
        }

        self.attribute_map = {
            'update_contact_column_action_settings': 'updateContactColumnActionSettings',
            'do_not_send_action_settings': 'doNotSendActionSettings',
            'append_to_dnc_action_settings': 'appendToDncActionSettings',
            'mark_contact_uncontactable_action_settings': 'markContactUncontactableActionSettings',
            'mark_contact_address_uncontactable_action_settings': 'markContactAddressUncontactableActionSettings',
            'set_content_template_action_settings': 'setContentTemplateActionSettings'
        }

        self._update_contact_column_action_settings = None
        self._do_not_send_action_settings = None
        self._append_to_dnc_action_settings = None
        self._mark_contact_uncontactable_action_settings = None
        self._mark_contact_address_uncontactable_action_settings = None
        self._set_content_template_action_settings = None

    @property
    def update_contact_column_action_settings(self):
        """
        Gets the update_contact_column_action_settings of this DigitalAction.
        The settings for an 'update contact column' action.

        :return: The update_contact_column_action_settings of this DigitalAction.
        :rtype: UpdateContactColumnActionSettings
        """
        return self._update_contact_column_action_settings

    @update_contact_column_action_settings.setter
    def update_contact_column_action_settings(self, update_contact_column_action_settings):
        """
        Sets the update_contact_column_action_settings of this DigitalAction.
        The settings for an 'update contact column' action.

        :param update_contact_column_action_settings: The update_contact_column_action_settings of this DigitalAction.
        :type: UpdateContactColumnActionSettings
        """
        

        self._update_contact_column_action_settings = update_contact_column_action_settings

    @property
    def do_not_send_action_settings(self):
        """
        Gets the do_not_send_action_settings of this DigitalAction.
        The settings for a 'do not send' action.

        :return: The do_not_send_action_settings of this DigitalAction.
        :rtype: object
        """
        return self._do_not_send_action_settings

    @do_not_send_action_settings.setter
    def do_not_send_action_settings(self, do_not_send_action_settings):
        """
        Sets the do_not_send_action_settings of this DigitalAction.
        The settings for a 'do not send' action.

        :param do_not_send_action_settings: The do_not_send_action_settings of this DigitalAction.
        :type: object
        """
        

        self._do_not_send_action_settings = do_not_send_action_settings

    @property
    def append_to_dnc_action_settings(self):
        """
        Gets the append_to_dnc_action_settings of this DigitalAction.
        The settings for an 'Append to DNC' action.

        :return: The append_to_dnc_action_settings of this DigitalAction.
        :rtype: AppendToDncActionSettings
        """
        return self._append_to_dnc_action_settings

    @append_to_dnc_action_settings.setter
    def append_to_dnc_action_settings(self, append_to_dnc_action_settings):
        """
        Sets the append_to_dnc_action_settings of this DigitalAction.
        The settings for an 'Append to DNC' action.

        :param append_to_dnc_action_settings: The append_to_dnc_action_settings of this DigitalAction.
        :type: AppendToDncActionSettings
        """
        

        self._append_to_dnc_action_settings = append_to_dnc_action_settings

    @property
    def mark_contact_uncontactable_action_settings(self):
        """
        Gets the mark_contact_uncontactable_action_settings of this DigitalAction.
        The settings for a 'mark contact uncontactable' action.

        :return: The mark_contact_uncontactable_action_settings of this DigitalAction.
        :rtype: MarkContactUncontactableActionSettings
        """
        return self._mark_contact_uncontactable_action_settings

    @mark_contact_uncontactable_action_settings.setter
    def mark_contact_uncontactable_action_settings(self, mark_contact_uncontactable_action_settings):
        """
        Sets the mark_contact_uncontactable_action_settings of this DigitalAction.
        The settings for a 'mark contact uncontactable' action.

        :param mark_contact_uncontactable_action_settings: The mark_contact_uncontactable_action_settings of this DigitalAction.
        :type: MarkContactUncontactableActionSettings
        """
        

        self._mark_contact_uncontactable_action_settings = mark_contact_uncontactable_action_settings

    @property
    def mark_contact_address_uncontactable_action_settings(self):
        """
        Gets the mark_contact_address_uncontactable_action_settings of this DigitalAction.
        The settings for an 'mark contact address uncontactable' action.

        :return: The mark_contact_address_uncontactable_action_settings of this DigitalAction.
        :rtype: object
        """
        return self._mark_contact_address_uncontactable_action_settings

    @mark_contact_address_uncontactable_action_settings.setter
    def mark_contact_address_uncontactable_action_settings(self, mark_contact_address_uncontactable_action_settings):
        """
        Sets the mark_contact_address_uncontactable_action_settings of this DigitalAction.
        The settings for an 'mark contact address uncontactable' action.

        :param mark_contact_address_uncontactable_action_settings: The mark_contact_address_uncontactable_action_settings of this DigitalAction.
        :type: object
        """
        

        self._mark_contact_address_uncontactable_action_settings = mark_contact_address_uncontactable_action_settings

    @property
    def set_content_template_action_settings(self):
        """
        Gets the set_content_template_action_settings of this DigitalAction.
        The settings for a 'Set content template' action.

        :return: The set_content_template_action_settings of this DigitalAction.
        :rtype: SetContentTemplateActionSettings
        """
        return self._set_content_template_action_settings

    @set_content_template_action_settings.setter
    def set_content_template_action_settings(self, set_content_template_action_settings):
        """
        Sets the set_content_template_action_settings of this DigitalAction.
        The settings for a 'Set content template' action.

        :param set_content_template_action_settings: The set_content_template_action_settings of this DigitalAction.
        :type: SetContentTemplateActionSettings
        """
        

        self._set_content_template_action_settings = set_content_template_action_settings

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

